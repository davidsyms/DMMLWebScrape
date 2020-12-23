from bs4 import BeautifulSoup
import requests
import cvs

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
