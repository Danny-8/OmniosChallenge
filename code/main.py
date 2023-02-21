import requests
from bs4 import BeautifulSoup
import uuid
from googletrans import Translator

'''
Generate a unique id by saving them in a dictionary to compare if they are already in use
'''
ids_dic = []
def unique_id():
    new_id = uuid.uuid4()
    if new_id in ids_dic:
        return unique_id()
    else:
        ids_dic.append(new_id)
        return new_id

'''
Generate a unique text for the book using a text-generator API.
The input has the structure of: 'The text of {title} is:'
The status generated by the API is used as the text because the account is out of credits
'''
def generate_text(title):
    # Request the text for the book using a specific input
    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={'text': 'The text of ' + str(title) + ' is:'},
        headers={'api-key': '9d719753-86bb-41d9-a1c9-59884821b0ee'}
    )

    # Taking status as a text because the account is out of API credits
    return str(r.json()['status'])

'''
Translate the text into spanish and italian 
'''
translator = Translator()
def translate_text(text):
    translation1 = translator.translate(text, dest='es')
    translation2 = translator.translate(text, dest='it')
    return translation1.text, translation2.text

'''
Modify the url to go across all pages and extract all products and information from each one
'''
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

            # Generate the text for the book using an API
            text = generate_text(title)

            # Translate the text into two popular languages
            translation1, translation2 = translate_text(text)

            print(title, star_rating, price, picture_url, id, text, translation1, translation2)


if __name__ == '__main__':
    main()