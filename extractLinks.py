import requests
import urllib.request
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import csv
import pdb

all_products = []
all_links = []
req = Request('https://brig-motors.com/product-category/vodnolyzhnoje-snaryazhenije/zhilety/', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

file = open('links.txt', 'w')
webpageLinks = soup.select('div.stm-product-inner')
for links in webpageLinks:
	for link1 in links.findAll('a'):
		all_links.append(link1['href'])
		file.write(str(link1['href'])+"\n")
file.close()

"""
#read file
f = open("links.txt", "r")
for x in f:
  print(x)
"""
for link in all_links:
	print(link)
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	products = soup.select('div.col-md-9.col-md-push-3.col-sm-12')
	for product in products:
		##product-9773 > div.row > div.col-lg-7.col-md-7.col-sm-12.col-xs-12 > div > h1
	    name = product.select('h1.product_title.entry-title')[0].text.strip()
	    print(name)
	    #breakpoint()
	    #true_value if condition else false_value
	    d = product.select('div.woocommerce-product-details__short-description > p')
	    description = (d[0].text.strip() if len(d) else "empty")
	    print(description)
	    price = product.select('span.woocommerce-Price-amount.amount > bdi')[0].text.strip()
	    print(price)
	    artikul = product.select('span.sku')[0].text.strip()
	    print(artikul)
	    image = product.select('img')[0].get('src')
	    print(image)
	    
	    all_products.append({
	        "name": name,
	        "description": description,
	        "price": price,
	        "artikul": artikul,
	        "image": image
	    })

keys = all_products[0].keys()

with open('products.csv', 'a', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_products)