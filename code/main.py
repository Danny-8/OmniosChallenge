import googletrans
import requests
from bs4 import BeautifulSoup
import json
from classes import Product

'''
Ask an input for the languages to translate, and verify it exists
'''
def language_input(text):
    l = input(f'Enter {text} language to translate: ')
    
    if l not in googletrans.LANGUAGES.keys():
        print('Language/Abbreviation not found. \n')
        return language_input(text)
    print('The selected language is: ', googletrans.LANGUAGES[l], '\n')
    return l

'''
Modify the url to go across all pages and extract all products and information from each one
'''
def main():
    # Ask for the two languages to translate the text
    lang1 = language_input('First')
    lang2 = language_input('Second')

    j = 1
    books = []
    print ('Starting Process...')

    for i in range(1,51):
        # Modify URL each iteration to go across all pages
        URL = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"

        # Get the html from the page and parse it using beautifulsoup
        soup = BeautifulSoup(requests.get(URL).content, 'html.parser')

        # Extract all different product sections
        products = soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

        # Extract the different information from each product
        for p in products:
            title = p.h3.a["title"]
            star_rating = p.find('p', {'class':'star-rating'})['class'][1]
            price = p.find('p', {'class':'price_color'}).text.strip()
            picture_url = p.find('img')['src']

            # Call the class product to fill all the variables of the book
            product = Product(title, star_rating, price, picture_url, lang1, lang2)

            # Fill a list will a dictionary of each product
            books.append(product.generate_dict())
            print('(', j, '/', len(products)*50, ')')
            j+=1

    # Generate a json with all products
    with open('output/products.json', 'w') as f:
        json.dump(books, f, indent=9)
    print("Done!")

if __name__ == '__main__':
    main()