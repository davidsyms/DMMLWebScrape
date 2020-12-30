from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

#Used to create number on file name
number_of_news_sites = 2
file_counter = [0] * number_of_news_sites


#Skim Articles
def read_articles(urls):
    file_index = -1

    for url in urls:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        if (url[1] == "Ceasefire"):
            file_index = 0
            file_counter[file_index] += 1
            
            headline = soup.find("h1", {"itemprop": "name headline"}).get_text()

            #Removes all children div's this included the extra links at bottom of article 
            textdiv = soup.find("div", {"id": "entry"})
            for remove in textdiv.find_all("div"):
                remove.decompose()
            text = textdiv.find_all("p")

            article = ""
            for i in text[1:]:
                article += i.get_text()

            author = text[0].get_text()[3:]

            #Date was nestled among other things within same "i" tag. This isolates the date.
            date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
            date = date_unstripped[14: date_unstripped[2:].find("-")+1]    

    
        elif (url[1] == "Canadian Dimension"):
            file_index = 1
            file_counter[file_index] += 1

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

        csv_values = ["".join(headline), "".join(article).replace("\n", ""), "".join(author), url[2], "".join(url[0]), "".join(date)]
        filename = "ScrappedArticles/{}{}.csv".format(url[1], file_counter[file_index])

        print("Writing: {}".format(filename))

        with open(filename, 'w') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(headers) 
            csvwriter.writerow(csv_values)


for keyword in keywords:
    urls = []

    """#############################################################################################
    #                                  Ceasefire                                                #
    #############################################################################################
    print("Scanning Ceasefire for {}".format(keyword))

    #open searche url and create soup
    r = requests.get("https://ceasefiremagazine.co.uk/?s={}".format(keyword.replace(" ", "+")))
    soup = BeautifulSoup(r.content, "html.parser")

    #finds all URLs from year 2020 
    article_containers = soup.find_all("div", {"id": "featured_w"})
    
    for i in article_containers:
        if ("2020" in i.find("h2").find("i").contents[0]):
            urls.append([i.find("h1").find("a").get("href"), "Ceasefire", keyword])"""

    #############################################################################################
    #                                  Canadian Dimension                                       #
    #   Notes:  Since this news sites has multiple pages ("next" button) per result I use a     #
    #           loop to iteratively search each "next" page until no articles from 2020 are     #
    #           found                                                                           #
    #############################################################################################
    """print("Scanning Canadian Dimension for {}".format(keyword))

    web_address = ""
    page = 0
    changed = 1
    while (changed):
        changed = 0

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
                urls.append([i.find("a").get("href"), "Canadian Dimension", keyword])
                changed = 1
                page += 1
    """

    #############################################################################################
    #                                  Al Jazeera                                               #
    #############################################################################################
    print("Scanning Al Jazeera for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        r = requests.get("https://www.aljazeera.com/search/{}?page={}".format(keyword, page).replace(" ", "%20"))        
        soup = BeautifulSoup(r.content, "html.parser")

        print("https://www.aljazeera.com/search/{}?page={}".format(keyword, page).replace(" ", "%20"))

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find_all("article")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                url = [i.find("a").get("href"), "Al Jazeera", keyword]
                if url not in urls:
                    changed = 1
                if (changed):
                    urls.append(url)
                print(i.find("a").get("href"))

        

    #read_articles(urls)



