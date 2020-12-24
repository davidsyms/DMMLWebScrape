from bs4 import BeautifulSoup
import requests
import csv

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]


#Skim Articles
def read_articles(urls):
    j = 0
    for url in urls:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        if (url[1] == "Ceasefire"):
            date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
            date = date_unstripped[14: date_unstripped[2:].find("-")+1]

            headline = soup.find("h1", {"itemprop": "name headline"}).get_text()
            
            #Removes all children div's this included the extra links at bottom of article 
            textdiv = soup.find("div", {"id": "entry"})
            for remove in textdiv.find_all("div"):
                remove.decompose()
            text = textdiv.find_all("p")
            
            author = text[0].get_text()[3:]

            article = ""
            for i in text[1:]:
                article += i.get_text()
    
        if (url[1] == "Canadian Dimension"):
            null = 0

        csv_values = ["".join(headline), "".join(article), "".join(author), url[2], "".join(url[0]), "".join(date)]
        filename = "ScrappedArticles/{}{}.csv".format(url[1], j)


        with open(filename, 'w') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(headers) 
            csvwriter.writerow(csv_values)

        j += 1

for keyword in keywords:
    urls = []

    #############################################################################################
    #                                  Ceasefire                                                #
    #############################################################################################

    #open searche url and create soup
    r = requests.get("https://ceasefiremagazine.co.uk/?s={}".format(keyword.replace(" ", "+")))
    soup = BeautifulSoup(r.content, "html.parser")

    #finds all URLs from year 2020 
    article_containers = soup.find_all("div", {"id": "featured_w"})
    
    for i in article_containers:
        if ("2020" in i.find("h2").find("i").contents[0]):
            print()
            #urls.append([i.find("h1").find("a").get("href"), "Ceasefire", keyword])

    #############################################################################################
    #                                  Canadian Dimension                                       #
    #   Notes:  Since this news sites has multiple pages ("next" button) per result I use a     #
    #           loop to iteratively search each "next" page until no articles from 2020 are     #
    #           found                                                                           #
    #############################################################################################
    
    search_string = ""
    page_string = "" #will hold what page # scraper is at.
    changed = 1
    while (changed == 1):
        print("Looped")    
        changed = 0
        if (keyword == "Climate Change"):
            search_string = "70dec0af9355c68c34ec5e27e957b6d8{}".format(page_string)
        if (keyword == "COVID 19"):
            search_string = "2cc0ddf8f7107fdaef2509b0e785876f{}".format(page_string)
        if (keyword == "Military Ground Vehicles"):
            search_string = "973c007b780e3452f8d8b15a63648590{}".format(page_string)
        
        r = requests.get("https://canadiandimension.com/search/{}".format(search_string))
        soup = BeautifulSoup(r.content, "html.parser")

        try:
            article_containers = soup.find("ol", {"class": "search-results"}).find_all("li")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                urls.append([i.find("small").find("a").get("href"), "Canadian Dimension", keyword])
                changed = 1

        

    read_articles(urls)



