###————————————————————————导入库————————————————————————————####
import requests
from pyquery import PyQuery as pq
import re
import time
import sys
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
options = Options()
options.add_argument('-headless') # 不打开浏览器

###————————————————————————获取网页源代码————————————————————————————####
def get_html(url):
    browser = webdriver.Chrome()
    browser.get(url)
    html=browser.page_source
    return html.encode("utf8")

###————————————————————————在原代码中选择表格数据————————————————————————————####
def parsePage(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.select('table') #选择表格数据
    df_list = []
    for table in tables:
        df_list.append(pd.concat(pd.read_html(table.prettify()))) #pd.read_html()
    df = pd.concat(df_list)
    return df
###————————————————————————获取所有的大类食物————————————————————————————####
url_list=[]
soup = BeautifulSoup(get_html('https://fq.chinafcd.org/'), 'lxml')
for li in soup.find_all('a'):
    li=li.get('href')
    if re.search(r'foodlist',li):
        new_url_str='https://fq.chinafcd.org/'+li
        url_list.append(new_url_str)

len(url_list)
url_list=set(url_list)

###————————————————————————获取所有食物的网页链接———————————————————————####
food_list=[]
for i in range(259,1615):
    new_url='https://fq.chinafcd.org/foodinfo/'+str(i)+'.html'
    food_list.append(new_url)

###————————————————————————进行数据抓取—————————————————————————————————————####
i=0
for url_str in food_list:
    csv_filename=str(i)+'.csv'
    df=parsePage(get_html(url_str))
    df.to_csv(csv_filename)
    i+=1
