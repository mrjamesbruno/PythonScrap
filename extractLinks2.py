# -*- coding: utf-8 -*-
import requests
import urllib.request
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import csv
import pdb
import re

all_products = []
all_links = []
artikul = "000"
indexOfImg = 1
req = Request('https://brig-motors.com/product-category/vodnolyzhnoje-snaryazhenije/zhilety/page/2/', headers={'User-Agent': 'Mozilla/5.0'})
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
def getImgUrl(imageName):
	#print("getImgUrl: ", len(imageName),imageName[0])
	rightName = ''
	imageName = imageName[:-1]
	#print("getImgUrl2: ", len(imageName),imageName[0])
	for y in imageName:
		#print(y)
		rightName += y+"-"
	return rightName[:-1]+".jpg"

def glueURL(url0):
	urlBack = ''
	#print("glueURL: ", len(url0),url0[0])
	url0 = url0[:-1]
	#del record[-1]
	#print("glueURL2: ", len(url0),url0[0])
	for y in url0:
		urlBack += y+"/"
	#print("glueURL: urlBack: ", urlBack)
	return str(urlBack)

for link in all_links:
	indexOfImg = 1
	#print(link)
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
	    
	    all_products.append({
	        "Артикул": artikul,
	        "Название (RU)": name,
	        "Цена": price,
	        "Описание товара (RU)": description
	        #"image": image
	    })
	
	img_tags = soup.find_all('img')
	urls = [img['src'] for img in img_tags]
	print("found img: ",len(urls))
	for url in urls:
		#print(url)
		filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
		if not filename:
		    #print("Regex didn't match with the url: {}".format(url))
		    continue
		#print(filename.group(1))
		#with open(filename.group(1), 'wb') as f:
		x = url.split("/")
		x1 = x[len(x)-1]
		#print("artikul i x1: ", artikul, x1)
		if artikul in x1:
		    #print("artikul in x1 >>>>>>>>>>>>>>")
		    urlWithoutIMG = glueURL(x)
		    #imya sohranyaemogo fila
		    imgName = artikul+"@"+str(indexOfImg)+".jpg"
		    #print("imgName: ",imgName)
		    #sdelat pravilnyi webadres kartinki
		    xName0 = x1.split("-")
		    #print("xName0: ",xName0[0])
		    xName = getImgUrl(xName0)
		    #print("xName: ",xName)
		    #udalyaem imya img i zamenyaem vernym xName
		    url = urlWithoutIMG+str(xName)
		    print("url: ",url)
		    try:
			    opener = urllib.request.build_opener()
			    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			    urllib.request.install_opener(opener)
			    urllib.request.urlretrieve(url, "IMG\\"+imgName)
		    except:
		    	print("!!! ERROR: Ne mogu skachat kartinky! >>>> ", url)
		    indexOfImg +=1
	
	#breakpoint()

keys = all_products[0].keys()

with open('products.csv', 'a', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_products)