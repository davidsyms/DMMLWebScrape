# DMMLWebScrape

-----------------------------Current Issues-----------------------------


I am currently having difficulty in the implimentation for:

Taipei Times: https://www.taipeitimes.com

Straits Times: https://www.straitstimes.com/global

Egypt Today: https://www.egypttoday.com

TRT World: https://www.trtworld.com

Russia Today: https://www.rt.com

Global Times: http://www.globaltimes.cn

21st Century Wire: https://21stcenturywire.com


Due to the fact that these pages use javascript to update pages with the next new articles instead of loading a new page.

In other words instead of going to newssite.com/search/page1 to newssite.com/search/page2 it just updates newssite.com/search/.

I do not know how to crawl these pages to find all relevant news articles.


-----------------------------Implimentation-----------------------------


To complete this task my program is split into two portions:

1. Scrape the URLs

2. Scrape the articles and write CSV files


The URL Scraping occurs in the "for keyword in keywords" portion of the program.

The article scraping and csv writing occur in the read_articles method.



-----------------------------Add Additional Sites-----------------------------


To add additional sites that follow the newssite.com/search/page1 to newssite.com/search/page2 format:

1. Identify what in the URL changes for each new page. 

2. Identify the container that has all the articles

3. Filter articles for dates in 2020 and scrape the assosiated URL

For a good example of implimentation of a new site see the implimentation for Canadian Dimension. 

-----------------------------TO ADD-----------------------------

American Free Press: https://americanfreepress.net
