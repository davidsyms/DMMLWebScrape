from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "Al Jazeera.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []
waste_url = []

for keyword in keywords:
    print("Scanning Al Jazeera for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        print("https://www.aljazeera.com/search/{}?page={}".format(keyword, page).replace(" ", "%20"))

        r = requests.get("https://www.aljazeera.com/search/{}?page={}".format(keyword, page).replace(" ", "%20"))        
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find_all("article")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                url = [i.find("a").get("href"), "Al Jazeera", keyword, "aljazeera.com"]
                if url not in urls:
                    changed = 1
                    urls.append(url)
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

        headline = soup.find("h1").get_text()

        author = "No Author"

        textdiv = soup.find("div", {"class": "wysiwyg wysiwyg--all-content"})
        
        #Removes all children div's this included the extra links at bottom of article 
        try:
            for remove in textdiv.find_all("div"):
                remove.decompose()
            text = textdiv.find_all("p")
        except:
            continue #if ths runs there is an error textdiv doesn't exit
            

        article = ""
        for i in text:
            article += i.get_text()

        date = soup.find("div", {"class" : "date-simple"}).get_text()

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue