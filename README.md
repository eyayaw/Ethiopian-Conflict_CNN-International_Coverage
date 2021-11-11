
# **Ethiopian Conflict: CNN-International (CNNI)’s Coverage**

Triggered by a thought-provoking
[thread](https://twitter.com/mekdes_asefa/status/1439266110679965708) by
[Mekdes Asefa](https://twitter.com/mekdes_asefa)

## The start of the conflict

> **November 03, 2021**

## How has cnni covered the conflict?

> See it for yourself on [Google
> News](https://google.com/search?q=site:https://cnn.com+after:2020-11-02+%22Ethiopia%22+AND+%22Tigray%22+-%22Covid%22+-%22Nile%22+&tbm=nws+&lr=lang_en+tbs=sbd:1+)

## Goal of this repo

-   Produce a list of CNN’s stories ever since the conflict broke out,
    November 4, 2020.

## So far

-   [x] **Articles**: I have managed to scrape news articles that CNN
    published ever since. You can find the details about these news
    articles in this [csv file](articles-meta.csv), in the same
    directory.

``` r
articles = read.csv("articles-meta.csv")
articles$url = with(articles, sprintf("<a href=\"%s\">%s</a>", url, basename(sub("/index.html",
    "", url))))
# DT::datatable(articles, options = list(pageLength=5), filter = 'top', escape
# = F)

knitr::kable(head(articles), format = "markdown", booktab = T)
```

| headline                                                                                          | url                                                                                                                                                                          | date       | author                                                            | contributors                                                                                          | editorial_source | update_time                                  | intro                                                                                                                                                                                                                                                                                        |
|:--------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------|:-----------------|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Young mother and elderly priest among Tigrayans arrested in Addis Ababa, witnesses say            | <a href="https://www.cnn.com/2021/11/08/africa/ethiopia-detentions-ethnicity-rights-commission-intl/index.html">ethiopia-detentions-ethnicity-rights-commission-intl</a>     | 2021-11-08 | Katie Polglase, Gianluca Mezzofiore and Richard Allen Greene, CNN |                                                                                                       | (CNN)            | Updated 2247 GMT (0647 HKT) November 8, 2021 | Witnesses say Tigrayans are being arrested in Addis Ababa in a wave of alleged ethnic targeting by authorities, after a year-long conflict in Ethiopia’s northern Tigray region.                                                                                                             |
| Ethiopia’s military calls on former members to rejoin army as rebels advance on capital           | <a href="https://www.cnn.com/2021/11/06/africa/ethiopia-military-volunteers-rebel-advance-intl/index.html">ethiopia-military-volunteers-rebel-advance-intl</a>               | 2021-11-06 | David McKenzie, CNN                                               | CNN’s Eliza Mackintosh and Kara Fox contributed to this report.                                       | (CNN)            | Updated 1407 GMT (2207 HKT) November 6, 2021 | Ethiopia’s military is calling on veterans to rejoin the army as two aligned rebel groups threaten the capital, marking the latest sign the government is marshaling its power to defend Addis Ababa.                                                                                        |
| Armed groups join forces in Ethiopia in biggest threat yet to embattled Prime Minister Abiy Ahmed | <a href="https://www.cnn.com/2021/11/05/africa/ethiopia-conflict-opposition-coalition-abiy-ahmed-intl/index.html">ethiopia-conflict-opposition-coalition-abiy-ahmed-intl</a> | 2021-11-05 | Eliza Mackintosh, CNN                                             | CNN’s David McKenzie and Jennifer Hansler contributed to this report.                                 | (CNN)            | Updated 2235 GMT (0635 HKT) November 5, 2021 | Armed groups fighting Ethiopia’s central government are swelling in numbers as they advance on the capital, Addis Ababa, posing the biggest threat to embattled Prime Minister Abiy Ahmed’s rule since a bloody year-long conflict began in the country’s northern Tigray region a year ago. |
| State Department establishes task force on Ethiopia as conflict rages                             | <a href="https://www.cnn.com/2021/11/05/politics/state-department-ethiopia-task-force/index.html">state-department-ethiopia-task-force</a>                                   | 2021-11-05 | Jennifer Hansler, CNN                                             |                                                                                                       | (CNN)            | Updated 2215 GMT (0615 HKT) November 5, 2021 | The State Department has established a new task force to oversee its “planning, management and logistics related to events in Ethiopia,” a spokesperson confirmed Friday.                                                                                                                    |
| Ethiopia crisis deepens as nine groups form anti-government alliance                              | <a href="https://www.cnn.com/africa/live-news/ethiopia-conflict-updates-11-5-intl/index.html">ethiopia-conflict-updates-11-5-intl</a>                                        | 2021-11-09 |                                                                   |                                                                                                       |                  |                                              |                                                                                                                                                                                                                                                                                              |
| Ethiopia is at war with itself. Here’s what you need to know about the conflict                   | <a href="https://www.cnn.com/2021/11/03/africa/ethiopia-tigray-explainer-2-intl/index.html">ethiopia-tigray-explainer-2-intl</a>                                             | 2021-11-03 | Eliza Mackintosh, CNN                                             | CNN’s Bethlehem Feleke in Nairobi and Jennifer Hansler in Washington, DC, contributed to this report. | (CNN)            | Updated 1627 GMT (0027 HKT) November 5, 2021 | When Ethiopian Prime Minister Abiy Ahmed received the Nobel Peace Prize in 2019, he was lauded as a regional peacemaker. Now, he is presiding over a protracted civil war that by many accounts bears the hallmarks of genocide.                                                             |

<br> <br>

CNN does not produce news only in an article form. There are live news
coverages with a collection of short “posts”
(e.g. [here](https://edition.cnn.com/africa/live-news/ethiopia-conflict-updates-11-5-intl/index.html)),
and video reporting
(e.g. [here](https://edition.cnn.com/videos/world/2021/06/13/ethiopia-famine-thousands-facing-starvation-busari-lklv-nr-intl-vpx.cnn))
as well. This repo contains details about such coverage too.

-   [x] **Live-news coverage** [here](live-news-articles.csv)

-   [x] **Video reports** [here](video-reports.csv)

## To-Do

-   [ ] Automate with `github actions`
-   [ ] Do an exploratory analysis
-   [ ] Download full body of the articles and do some text analysis
-   [ ] Download images and videos
-   [ ] Do the same for Reuters, BBC, and the likes
