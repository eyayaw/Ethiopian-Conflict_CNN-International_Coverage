from requests_html import HTML
from requests_html import HTMLSession

url = "https://edition.cnn.com/search?size=100&q=Ethiopia%20AND%20Tigray"
css_selector = '.cnn-search__result-headline a'

# Google search query
param = (
'site:https://cnn.com+'    # website of CNN
'after:2020-11-02+'        # since Nov 03, 2020, the war started
'"Ethiopia"+AND+"Tigray"+' # query terms
'-"Covid"+-"Nile"+'        # exclude covid and Nile
"&tbm=nws+"                # search on News tab
'&lr=lang_en+'             # search in English
'tbs=sbd:1+'               # sort by date
)

search_url = f"https://google.com/search?q={param}"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0"}

session = HTMLSession() 
response = session.get(url, headers=headers)

print(response.html.absolute_links)


