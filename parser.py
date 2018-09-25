import requests
import os
from bs4 import BeautifulSoup
#import re
import sqlite3

def base_write(name, description):
	connection = sqlite3.connect('D:\\moychay\\base\\products.db')
	cursor = connection.cursor()
	cursor.execute('''INSERT INTO tea (name, description) VALUES (?,?)''', (name, description))
	connection.commit()
	connection.close()

def catalog_page_parser(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	items_list = soup.find_all('a', class_ = 'o_p_name')
	refs = {}
	for item in items_list:
		s = 'http://rostovondon.moychay.ru' + item.get('href')
		refs[item.get_text()] = s
	return refs

def item_parser(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	item_name = soup.find_all('h1', itemprop = 'name')[0].get_text()
	item_description = soup.find('article', class_ = 'item-description').find('div', class_ = 'description').find_all('p')
	#f = open('D:\\moychay\\base\\result.txt', 'a', encoding = 'utf-8')
	#f.write('\n' + item_name + '\n')
	s = ''
	for item in item_description:
		s += item.text.replace('\n', '')
	#result = re.split(r'(?<=\w[.!?]) ', s)        #Разбивает текст по точкам на предложения, не учитывает г. итд
	#f.write(s)
	#f.close()
	base_write(item_name, s)
	



	'''item_images = soup.find_all('a', class_ = 'popup')
	for img in item_images:
		u = 'http://rostovondon.moychay.ru' + img.get('href')
		f = u[u.rfind('/'):u.find('?')]
		get_item_images(u, f)


def get_item_images(url, filename):
	r = requests.get(url)
	out = open('D:\\moychay\\img\\' + filename, 'wb')
	out.write(r.content)
	out.close()'''

'''Кусок сверху добавляет функционал скачивания картинок в общую папку, оно работает, но:
1) Это большие картинки, для миниатюр другие ссылки надо выдёргивать
2) Именование оригинальное, для хранения в БД нужно придумать систему, в которой картинки
будут связаны с исходным итемом, сейчас таких ассоциаций нет.'''


adr = 'https://rostovondon.moychay.ru/catalog/ulun/yuzhnofudzyanskij_ulun'
i = catalog_page_parser(adr)
for key in i.keys():
	item_parser(i[key])