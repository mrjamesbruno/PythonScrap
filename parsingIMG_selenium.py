from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import urllib.request
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import csv
import pdb
import re

site = 'https://brig-motors.com/shop/universal-vest-red/'
dr = webdriver.Chrome()

dr.get(site)
try:
    element = WebDriverWait(dr, 20, 0.5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "pswp__zoom-wrap"))
    )
except:
    print("Wait a bit more")
    time.sleep(5)

text = dr.page_source
soup = BeautifulSoup(text,'html.parser')
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]
	
for url in urls:
	print(url)
	filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
	if not filename:
	    print("Regex didn't match with the url: {}".format(url))
	    continue
	with open(filename.group(1), 'wb') as f:
	    if 'http' not in url:
		    # sometimes an image source can be relative 
		    # if it is provide the base url which also happens 
		    # to be the site variable atm. 
		    url = '{}{}'.format(site, url)
#imgs = soup.find_all('img')
#print(imgs)

dr.close()