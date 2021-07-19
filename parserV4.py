# -*- coding: utf-8 -*-
import requests
import urllib.request
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import csv
import re
import xlsxwriter
import pdb
import sys

startPage = 'https://brig-motors.com/product-category/vodnolyzhnoje-snaryazhenije/zhilety/'

headers1='User-Agent'
headers2 = 'Mozilla/5.0'
all_products = []
all_products.append(["Артикул","Название (RU)","Цена","Описание товара (RU)"])

def soup2(link):
	req = Request(link, headers={headers1: headers2})
	webpage = urlopen(req).read()
	return BeautifulSoup(webpage, 'html.parser')
	#soup = BeautifulSoup(webpage, 'html.parser')

def getImgUrl(imageName):
	rightName = ''
	imageName = imageName[:-1]
	for y in imageName:
		rightName += y+"-"
	return rightName[:-1]+".jpg"

def glueURL(url0):
	urlBack = ''
	url0 = url0[:-1]
	for y in url0:
		urlBack += y+"/"
	return str(urlBack)

def mainParser(mainLink):
	all_links = []
	artikul = "000"
	indexOfImg = 1
	
	#ischem i zapisyvaem v file linki vseh tovarov, mojet zapis ne nujna?
	file = open('links.txt', 'a')
	webpageLinks = soup2(mainLink).select('div.stm-product-inner')
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
		indexOfImg = 1
		req = Request(link, headers={headers1: headers2})
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		products = soup.select('div.col-md-9.col-md-push-3.col-sm-12')
		for product in products:
		    name = product.select('h1.product_title.entry-title')[0].text.strip()
		    print(name)
		    #true_value if condition else false_value
		    d = product.select('div.woocommerce-product-details__short-description > p')
		    description = (d[0].text.strip() if len(d) else "empty")
		    print(description)
		    price = product.select('span.woocommerce-Price-amount.amount > bdi')[0].text.strip()
		    print(price)
		    artikul = product.select('span.sku')[0].text.strip()
		    print(artikul)
		    all_products.append([artikul, name, price, description])
		
		img_tags = soup.find_all('img')
		urls = [img['src'] for img in img_tags]
		print("found img: ",len(urls))
		for url in urls:
			filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
			if not filename:
			    continue
			x = url.split("/")
			x1 = x[len(x)-1]
			if artikul in x1:
			    #imya sohranyaemogo fila
			    imgName = artikul+"@"+str(indexOfImg)+".jpg"
			    #delaem pravilnyi webadres kartinki
			    xName0 = x1.split("-")
			    xName = getImgUrl(xName0)
			    urlWithoutIMG = glueURL(x)
			    #udalyaem imya img i zamenyaem vernym xName
			    url = urlWithoutIMG+str(xName)
			    print("url: ",url)
			    try:
				    opener = urllib.request.build_opener()
				    opener.addheaders = [(headers1, headers2)]
				    urllib.request.install_opener(opener)
				    urllib.request.urlretrieve(url, "IMG\\"+imgName)
			    except:
			    	print("!!! ERROR: Ne mogu skachat kartinky! >>>> ", url)
			    indexOfImg +=1
	#poisk sleduuschei page i est li ona voobsche
	#<div class="stm-prev-next stm-next-btn">
	nextPage = ''
	nextPageZone = soup2(mainLink).select('div.stm-prev-next.stm-next-btn')
	for links in nextPageZone:
		#print("len: ",len(links.findAll('a')))
		if len(links.findAll('a')) == 0:
			nextPage = 'empty'
			break
		else:
			for link1 in links.findAll('a'):
				nextPage = link1['href']
				break

	if nextPage == 'empty':
		#https://xlsxwriter.readthedocs.io/working_with_data.html
		workbook = xlsxwriter.Workbook('brig-motors.xlsx')
		worksheet = workbook.add_worksheet()
		for row_num, row_data in enumerate(all_products):
		    for col_num, col_data in enumerate(row_data):
		        worksheet.write(row_num, col_num, col_data)
		# Write a total using a formula.
		#worksheet.write(row, 0, 'Total')
		#worksheet.write(row, 1, '=SUM(B1:B4)')
		workbook.close()
		print("DONE! NO MORE PAGES!")
		input("Press Enter to exit...")
		sys.exit()
	else:
		print("START NEXT PAGE: ",nextPage)
		mainParser(nextPage)
	#breakpoint()

mainParser(startPage)
