import webbrowser
from requests_html import HTMLSession
import re
import pandas as pd
from datetime import date
from functools import reduce
import __main__ as main
interactive = hasattr(main, '__file__')

# like R's `paste`
def paste(ls, collapse=" "):
    return reduce(lambda x, y: str(x) + collapse + str(y), ls)

# Google search query
params = (
    'site:https://cnn.com+'    # website of CNN
    'after:2020-11-02+'        # since Nov 03, 2020, the war started
    '"Ethiopia"+AND+"Tigray"+' # query terms
    '-"Covid"+-"Nile"+'        # exclude covid and Nile
    "&tbm=nws+"                # search on News tab
    '&lr=lang_en+'             # search in English
    'tbs=sbd:1+'               # sort by date
)

search_url = f"https://google.com/search?q={params}"
if (interactive):
    webbrowser.open(search_url)

# scrape CNN's coverage of the conflict
query = "Ethiopia, Tigray"
size = 20
url = f"https://edition.cnn.com/search?size={size}&q={query}&category=us,politics,world,opinion&sort=newest"
#url = f'https://search.api.cnn.io/content?q=Ethiopia+AND+Tigray&sort=newest&size={size}&category=politics,world'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0"}
conflict_breakout_date = date(2020, 11, 3)

session = HTMLSession()
r = session.get(url, headers=headers)
r.html.render(sleep=1, scrolldown=5, timeout=1000)

# "Displaying results 1-{size} out of ... for {query}"
count = r.html.find(".cnn-search__results-count", first=True).text
regex = r"(\d{1,}-\d{1,}) out of (\d{1,})"
# results displayed per page, num of results
displays, out_of = re.findall(regex, count)[0]
pages = int(out_of) % size

search_results_page1 = r.html.find('.cnn-search__result-headline')
search_results = []
for article in search_results_page1:
    headline = article.find("h3", first=True).text
    link = "https:" + article.find("h3 > a[href]", first=True).attrs["href"]
    search_results.append(dict(headline=headline, url=link))

# from the second page onwards
for page in range(2, pages+1):
    page_url = url + f"&page={page}&from={size * (page-1)}"
    res = session.get(page_url, headers=headers)
    res.html.render(sleep=1, scrolldown=5, timeout=1000)
    articles = res.html.find('.cnn-search__result-headline')
    for article in articles:
        headline = article.find("h3", first=True).text
        link = "https:" + \
            article.find("h3 > a[href]", first=True).attrs["href"]
        search_results.append(dict(headline=headline, url=link))

search_results_df = pd.DataFrame(search_results)
Date = []
for u in search_results_df.url:
    try: 
        d = re.search("(\d{4}/\d{2}/\d{2})", u).group(1) 
        d = date.fromisoformat(d.replace("/", "-"))
    except AttributeError: 
        d = "" # date.today() # assign today's date if the url does not contain date
    Date.append(d)
        
search_results_df['date'] = Date
cond = [d >= conflict_breakout_date if d != "" else True for d in search_results_df.date]
search_results_df = search_results_df[cond]
search_results_df.to_csv('search-results.csv', index=False)

# open each article and then scrape headline, author, contributors,
## release date, modified date ...
articles_search_results = \
    search_results_df[['live-news' not in u and 'videos' not in u for u in search_results_df.url]].reset_index()
# subset = ["ethiopia" in u or 'tigray' in u for u in articles_search_results.url]
Articles = []
for arturl in articles_search_results.url:
    r = session.get(arturl, headers=headers)
    try:
        author = r.html.find('.metadata__byline__author',
                                first=True).text.replace("By ", "")
    except AttributeError:
        author = ""
    try:
        update_time = r.html.find(".update-time", first=True).text
    except AttributeError:
        update_time = ""
    try:
        editorial_source = r.html.find(".el-editorial-source", first=True).text
    except AttributeError:
        editorial_source = ""
    try:
        contributors = r.html.find(".zn-body__footer", first=True).text
    except AttributeError:
        contributors = ""
    try:
        intro = r.html.find(".zn-body__paragraph[class*=speakable]",
                                first=True).text.strip(editorial_source)
    except AttributeError:
        intro = ""
    Articles.append(dict(
        url=arturl,
        author=author,
        contributors=contributors,
        editorial_source=editorial_source,
        update_time=update_time,
        intro=intro))
 

Articles = pd.DataFrame(Articles)
article_news = articles_search_results.merge(Articles, on='url')
article_news.to_csv("articles-meta.csv", index=False)

# scrape video reports
videos = []
for arturl in search_results_df[['videos' in u for u in search_results_df.url]].url:
    r = session.get(arturl, headers=headers)
    try:
        author = r.html.find('.media__video-description', first=True).text
        author = str(re.findall(
                r"CNN'?s? [A-Z][a-z]+ [A-Z][a-z]+", author)).strip('"[]"')
    except AttributeError:
        author = ""
    try:
        editorial_source = r.html.find(
                '.video__metadata__source-name', first=True).text
    except AttributeError:
        editorial_source = ""
    try:
        intro = r.html.find('.media__video-description', first=True).text
    except AttributeError:
        intro = ""
    videos.append(dict(
        url=arturl,
        author=author,
        contributors=contributors,
        editorial_source=editorial_source,
        update_time=update_time,
        intro=intro))

video_news = pd.DataFrame(videos)
video_news = search_results_df[[ 'videos' in u for u in search_results_df.url]].\
    merge(video_news, on='url')
video_news = video_news.loc[:, video_news.columns!='contributors']
video_news.to_csv("video-reports.csv", index=False)

# scrape posts under live-news
live_news = search_results_df[['live-news' in u for u in search_results_df.url]]
live_news_out = []
live_news = live_news[['Ethiopia' in u or 'Tigray' in u
                       for u in live_news.headline]]
for url in live_news.url:
    r = session.get(url, headers=headers)
    r.html.render(sleep=1, scrolldown=20, timeout=2000)

    headline = r.html.find(".headline > h1", first=True).text
    author = r.html.find(".headline > div > p[data-type*=byline-area]", first=True).\
        text.replace("By ", "")
    nposts = r.html.find("#posts > div > div:nth-child(1)", first=True).\
        text.replace(" Posts", "")
    subarticles = r.html.find('article > header')
    header = []
    for h in subarticles[1:]:
        header.append(h.text)
    live_news_out.append(dict(
        url=url,
        headline=headline,
        main_author=author,
        posts=paste(header, collapse="\n\n"),
        nposts=nposts)
        )

live_news_out = pd.DataFrame(live_news_out)
live_news_out.to_csv("live-news-articles.csv", index=False)
