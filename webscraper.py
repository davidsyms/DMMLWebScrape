from bs4 import BeautifulSoup
import requests
import csv

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID-19", "Military Ground Vehicles"]


#Skim Articles
def read_articles(urls):
    j = 0
    for url in urls:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")

        date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
        date_stripped = date_unstripped[14: date_unstripped[2:].find("-")+1]

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

        csv_values = ["".join(headline), "".join(article), "".join(author), url[2], "".join(url), "".join(date_stripped)]


        filename = "ScrappedArticles/{}{}.csv".format(url[1], j)


        with open(filename, 'w') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(headers) 
            csvwriter.writerow(csv_values)

        j += 1

for keyword in keywords:
    urls = []
    print("\n\n\nKey word: {}".format(keyword))
    #open searche url and create soup
    r = requests.get("https://ceasefiremagazine.co.uk/?s={}".format(keyword.replace(" ", "+")))
    soup = BeautifulSoup(r.content, "html.parser")


    #finds all URLs from year 2020 
    article_containers = soup.find_all("div", {"id": "featured_w"})
    

    for i in article_containers:
        if ("2020" in i.find("h2").find("i").contents[0]):
            urls.append([i.find("h1").find("a").get("href"), "Ceasefire", keyword])

    read_articles(urls)



