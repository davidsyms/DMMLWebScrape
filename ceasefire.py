from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "Ceasefire.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []

for keyword in keywords:
    print("Scanning Ceasefire for {}".format(keyword))

    #open searche url and create soup
    print("https://ceasefiremagazine.co.uk/?s={}".format(keyword.replace(" ", "+")))
    r = requests.get("https://ceasefiremagazine.co.uk/?s={}".format(keyword.replace(" ", "+")))
    soup = BeautifulSoup(r.content, "html.parser")

    #finds all URLs from year 2020 
    article_containers = soup.find_all("div", {"id": "featured_w"})
    
    for i in article_containers:
        if ("2020" in i.find("h2").find("i").contents[0]):
            urls.append([i.find("h1").find("a").get("href"), "Ceasefire", keyword, "ceasefiremagazine.co.uk"])

for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        headline = soup.find("h1", {"itemprop": "name headline"}).get_text() #Gets headline

        #Removes all children div's this included the extra links at bottom of article 
        textdiv = soup.find("div", {"id": "entry"})
        for remove in textdiv.find_all("div"):
            remove.decompose()
    
        #Gets Article
        text = textdiv.find_all("p")
        article = ""
        for i in text[1:]:
            article += i.get_text()

        author = text[0].get_text()[3:]

        #Date was nestled among other things within same "i" tag. This isolates the date.
        date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
        date = date_unstripped[14: date_unstripped[2:].find("-")+1] 

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue