# -*- coding: utf-8 -*-
#dlya russkogo nujno sohranyat .py v UTF-8
import requests
import urllib.request
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
import csv
import pdb
import re
import xlsxwriter

num = [1,2,3,4,5,6,7,8,9,0]
#all_products  <class 'list'>
all_products = []
all_products.append(['Артикул','Название (RU)','Цена','Описание товара (RU)'])
all_products.append([num[0],num[1],num[2],num[3]])
all_products.append([num[4],num[5],num[6],num[7]])

"""
#expenses:  <class 'tuple'>  
expenses = (
     ['Rent', '2013-01-13', 1000],
     ['Gas',  '2013-01-14',  100],
     ['Food', '2013-01-16',  300],
	)
"""
print("all_products: ",type(all_products))
#print("expenses: ",type(expenses))

workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()
for row_num, row_data in enumerate(all_products):
    print("row_num, row_data: ",row_num,row_data)
    for col_num, col_data in enumerate(row_data):
        print(">>>row_num, col_num, col_data: ",row_num,col_num,col_data)
        worksheet.write(row_num, col_num, col_data)
        
workbook.close()