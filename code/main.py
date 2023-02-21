import requests
from bs4 import BeautifulSoup

for i in range(1,51):
    # Modify URL each iteration to go across all pages
    URL = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"

    # Get the html from the page and parse it using beautifulsoup
    page = requests.get(URL) 
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract all different product sections
    products = soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

    # Extract the different information from each product
    for p in products:
        title = p.h3.a["title"]
        star_rating = p.find('p', {'class':'star-rating'})['class'][1]
        price = p.find('p', {'class':'price_color'}).text.strip()
        picture_url = p.find('img')['src']
        print(title, star_rating, price, picture_url)