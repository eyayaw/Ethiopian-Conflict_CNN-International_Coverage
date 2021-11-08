library(data.table)

# Google search query
param = paste(
  'site:https://cnn.com',# website of CNN
  'after:2020-11-02',# since Nov 03, 2020, the war started
  '"Ethiopia"+AND+"Tigray"+-"Covid"+-"Nile"',# exclude covid and Nile
  "&tbm=nws",#search on News tab
  '&lr=lang_en',# search in English
  'tbs=sbd:1', #sort by date
  sep = "+"
)

search_url = paste0("https://google.com/news?q=", param)
if (interactive) browseURL(search_url)

query = "Ethiopia+AND+Tigray"
size = 20
search_url_cnni = sprintf("https://edition.cnn.com/search?q=%s&size=%s&category=us,politics,world,opinion&sort=newest",
                          query, size)
if (interactive()) browseURL(search_url_cnni)

##  -----
articles = fread('articles-meta.csv')
vids = fread('video-reports.csv')
livenews = fread('live-news-articles.csv')

