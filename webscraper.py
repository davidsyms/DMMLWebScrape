from bs4 import BeautifulSoup
import requests
import csv

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]


#open searche url and create soup
r = requests.get("https://ceasefiremagazine.co.uk/?s=coronavirus")
soup = BeautifulSoup(r.content, "html.parser")


#finds all URLs from year 2020 
article_containers = soup.find_all("div", {"id": "featured_w"})
urls = []

for i in article_containers:
    if ("2020" in i.find("h2").find("i").contents[0]):
        urls.append(i.find("h1").find("a").get("href"))

print(urls)

j = 0

#Skim Articles
for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
    date_stripped = date_unstripped[14: date_unstripped[2:].find("-")+1]
    #print("\n\nDate: {}\n\n".format(date_stripped))

    headline = soup.find("h1", {"itemprop": "name headline"}).get_text()
    #print("Headline: {}\n\n".format(headline))
    
    textdiv = soup.find("div", {"id": "entry"})
    for remove in textdiv.find_all("div"):
        remove.decompose()
    text = textdiv.find_all("p")
    
    author = text[0].get_text()[3:]
    #print("Author: {}\n\n".format(author))

    article = ""
    for i in text[1:]:
        article += i.get_text()
    #print(article)


    print("\n\n")

    filename = "ScrappedArticles/Ceasefire{}.csv".format(j)
    csv_values = ["".join(headline), "".join(article), "".join(author), "Coronavirus", "".join(url), "".join(date_stripped)]
    print(csv_values)

    with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 
        csvwriter.writerow(csv_values)

    j += 1