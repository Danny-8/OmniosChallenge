import requests
from bs4 import BeautifulSoup
import uuid

# Generate a unique id by saving them in a dictionary to compare if they are already in use
ids_dic = []
def unique_id():
    new_id = uuid.uuid4()
    if new_id in ids_dic:
        return unique_id()
    else:
        ids_dic.append(new_id)
        return new_id

def main():
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

            # Generate a unique id for the book
            id = unique_id()

            print(title, star_rating, price, picture_url, id)

if __name__ == '__main__':
    main()