import uuid
import requests
from googletrans import Translator


'''
Class to generate a unique id by saving them in a dictionary to compare if they are already in use
'''
class UniqueIDGenerator:
    def __init__(self):
        self.ids_dic = []

    def unique_id(self):
        new_id = uuid.uuid4()
        if new_id in self.ids_dic:
            return self.unique_id()
        else:
            self.ids_dic.append(new_id)
            return new_id

'''
Class for each product scraped from the website
'''
class Product:
    def __init__(self, title, star_rating, price, picture_url, lang1, lang2):
        self.title = title
        self.star_rating = star_rating
        self.price = price
        self.picture_url = picture_url
        self.id = str(UniqueIDGenerator().unique_id())
        self.text = self.generate_text()
        self.translation1, self.translation2 = self.translate_text(lang1, lang2)
        self.price_eu = self.pounds_to_euros()

    '''
    Generate a unique text for the book using a text-generator API.
    The input has the structure of: 'The text of {title} is:'
    The status generated by the API is used as the text because the account is out of credits
    '''
    def generate_text(self):
        # Request the text for the book using a specific input
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={'text': 'The text of ' + str(self.title) + ' is:'},
            headers={'api-key': '9d719753-86bb-41d9-a1c9-59884821b0ee'}
        )

        # Taking status as a text because the account is out of API credits
        return str(r.json()['status'])

    '''
    Translate the text into spanish and italian 
    '''
    def translate_text(self, l1, l2):
        translator = Translator()
        translation1 = translator.translate(self.text, dest=l1)
        translation2 = translator.translate(self.text, dest=l2)
        return translation1.text, translation2.text

    '''
    Convert the price from pounds to euros using an API to know the latest conversion rates, if not,
    use a simple conversion rate
    '''
    def pounds_to_euros(self):
        response = requests.get("https://api.exchangeratesapi.io/latest?symbols=GBP")
        data = response.json()

        if data['success'] == True:
            euro_conversion = data['rates']['EUR']
        else:
            euro_conversion = 1.14
        return str(round(float(self.price[1:]) * euro_conversion, 2))+'€'
    
    '''
    Generate a dictionary with all the information of the product
    '''
    def generate_dict(self):
        return {
            "title": self.title,
            "star_rating": self.star_rating,
            "price": self.price,
            "price_eu": self.price_eu,
            "picture_url": self.picture_url,
            "text": self.text,
            "translation1": self.translation1,
            "translation2": self.translation2,
            "id": self.id
        }