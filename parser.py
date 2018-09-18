import requests
import os
from bs4 import BeautifulSoup
#import re

adr = 'https://rostovondon.moychay.ru/catalog/ulun/yuzhnofudzyanskij_ulun'
def item_parser(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	item_name = soup.find_all('h1', itemprop = 'name')[0].get_text()
	item_description = soup.find('article', class_ = 'item-description').find('div', class_ = 'description').find_all('p')
	f = open('D:\\moychay\\base\\result.txt', 'a', encoding = 'utf-8')
	f.write('\n' + item_name + '\n')
	s = ''
	for item in item_description:
		s += item.text.replace('\n', '')
	#result = re.split(r'(?<=\w[.!?]) ', s)
	f.write(s)
	f.close()

def catalog_page_parser(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	items_list = soup.find_all('a', class_ = 'o_p_name')
	refs = {}
	for item in items_list:
		s = 'http://rostovondon.moychay.ru' + item.get('href')
		refs[item.get_text()] = s
	return refs

i = catalog_page_parser(adr)
for key in i.keys():
	item_parser(i[key])