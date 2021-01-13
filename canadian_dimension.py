from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "Canadian Dimension.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []
waste_url = []

for keyword in keywords:
    """ Notes:   Since this news sites has multiple pages ("next" button) per result I use a    
                 loop to iteratively search each "next" page until no articles from 2020 are   
                 found """
    print("Scanning Canadian Dimension for {}".format(keyword))

    #There are multiple pages on this site, these variables are used to iterate through the pages
    web_address = ""
    page = -1
    changed = 1

    while (changed):
        changed = 0
        page += 1

        #Canadian Dimension has certain pages for environment and COVID. It does not for MGV. Therefore,
        #Uses CD's default search tool to locate articles.
        # *****NOTE: after a sizeable amount of requests CD search will switch to a custom google search*******
        if (keyword == "Climate Change"):
            web_address = "https://canadiandimension.com/articles/category/environment/P{}0".format(page)
        elif (keyword == "COVID 19"):
            web_address = "https://canadiandimension.com/articles/category/covid-19/P{}0".format(page)
        elif (keyword == "Military Ground Vehicles"):
            web_address = "https://canadiandimension.com/search/973c007b780e3452f8d8b15a63648590/P{}0".format(page)

        print(web_address)

        r = requests.get(web_address)
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find_all("li")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                urls.append([i.find("a").get("href"), "Canadian Dimension", keyword, "canadiandimension.com"])
                changed = 1
            elif ("2021" in i.text):
                url_text = i.find("a").get("href")
                if url_text not in waste_url:
                    waste_url.append(url_text)
                    changed = 1

for url in urls:
    print("Scrapping: {}".format(url[0]))

    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        headline = soup.find("h1", {"class": "article-title"}).get_text()

        #author and date stored in same <p> tag, seperated by a "/". This seperates date and author
        author_date_line = soup.find("p", {"class", "byline"}).get_text().split("/")

        author = author_date_line[0]

        textdiv = soup.find("div", {"class": "content"})

        #Removes all children div's this included the extra links at bottom of article 
        for remove in textdiv.find_all("div"):
            remove.decompose()
        text = textdiv.find_all("p")

        article = ""
        for i in text:
            article += i.get_text()

        date = author_date_line[1]

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue