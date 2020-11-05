from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np
import unicodecsv as csv
from time import sleep
from random import randint
from os.path import basename

#empty list for storing data
product_name = []
prices = []
price_per_kg = []
weights = []
images = []

pages = np.arange(1, 4, 1) #iterate through pages (start at 1, stop at page 4 and step by 1)

for source in pages:
    #loop that iterates through pages 1-4, finds product divs
    source = requests.get("https://nakup.itesco.cz/groceries/cs-CZ/shop/pecivo/all?shelf=4294966651%2C4294962246%2C4294962166%2C4294962199%2C4294966645%2C4294962340%2C4294963905%2C4294962125&viewAll=shelf&sortBy=priceAscending&page=" + str(source))
    soup = BeautifulSoup(source.text, 'lxml')
    sleep(randint(2,7)) #timer to avoid script detection

    for container in soup.find_all('a', class_='ui__StyledLink-sc-18aswmp-0 hgdSSe'):  #find all product names
        name = container.text
        product_name.append(name)

    for container in soup.find_all('div', class_='price-per-sellable-unit'):    #find all product prices
        price = container.text
        prices.append(price)

    for container in soup.find_all('div', class_='price-per-quantity-weight'):  #find all product weight per kg
        price_per_weight = container.text
        price_per_kg.append(price_per_weight)

    for container in soup.find_all('a', class_='ui__StyledLink-sc-18aswmp-0 hgdSSe'):  #find all product weight in grams
        weight_src = container.text
        weight = weight_src.split(' ')[-1]  #splits weight from product name
        weights.append(weight)
    
    for container in soup.find_all('img'): #find all product images
        img_src = container.get('src')
        images.append(img_src)

information = pd.DataFrame({
    'name': product_name,
    'price': prices,
    'weight': weights,
    'price per kg': price_per_kg,
    'image url': images
})

information.to_csv('Information.csv')


