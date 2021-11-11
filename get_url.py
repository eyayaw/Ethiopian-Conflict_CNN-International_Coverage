from requests_html import HTMLSession
import re
from datetime import date

query = "Ethiopia,Tigray"
size = 20
url = f"https://edition.cnn.com/search?size={size}&q={query}&category=us,politics,world,opinion&sort=newest"
#url = f'https://search.api.cnn.io/content?q=Ethiopia+AND+Tigray&sort=newest&size={size}&category=politics,world'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0"}
conflict_breakout_date = date(2020, 11, 3)

session = HTMLSession()
# scrape CNN's coverage of the conflict
r = session.get(url, headers=headers)
r.html.render(sleep=1, scrolldown=5, timeout=1000)

def get_metadata():
    """ get the `url` and `headline` of the article
    """

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
            d = date.today() # assign today's date if the url does not contain date
        Date.append(d)
            
    search_results_df['date'] = Date
    search_results_df = search_results_df[search_results_df.date >= conflict_breakout_date]
    search_results_df.to_csv('search-results.csv', index=False)