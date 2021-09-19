library(rvest)

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

browseURL(search_url)

search_url |>
  read_html() |>
  html_elements('h3')

