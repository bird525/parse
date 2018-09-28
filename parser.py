import requests
import os
from bs4 import BeautifulSoup
#import re
import sqlite3

def item_write(name, description):
	connection = sqlite3.connect('D:\\moychay\\base\\products.db')
	cursor = connection.cursor()
	cursor.execute('''INSERT INTO tea (name, description) VALUES (?,?)''', (name, description))
	connection.commit()
	cursor.execute('''SELECT id FROM tea WHERE name = (?)''', (name,))
	item_id = str(cursor.fetchall()[0][0])
	connection.close()
	return item_id

def get_item_images(url, dirname, filename):
	r = requests.get(url)
	file_full_name = 'D:\\moychay\\img\\' + dirname + '\\' + filename
	out = open(file_full_name, 'wb')
	out.write(r.content)
	out.close()
	connection = sqlite3.connect('D:\\moychay\\base\\products.db')
	cursor = connection.cursor()
	cursor.execute('''INSERT INTO tea_photos (name, ref, item_id) 
					  VALUES (?,?,?)''', (filename, file_full_name, dirname))
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
	item_name = soup.find_all('h1', itemprop = 'name')[0].get_text().replace('\n', '')
	item_description = soup.find('article', class_ = 'item-description').find('div', class_ = 'description').find_all('p')
#сгенерили супчик, нашли имя итема и описание
	s = ''
	for item in item_description:
		s += item.text.replace('\n', '')
	item_id = item_write(item_name, s)
#вытащили описание в текст, записали имя и описание в базу
	try:
		os.mkdir('D:\\moychay\\img\\' + item_id)
	except FileExistsError:
		pass
#создаём папку для изображений данного итема
	item_images = soup.find_all('a', class_ = 'popup')
	for img in item_images:
		u = 'http://rostovondon.moychay.ru' + img.get('href')
		f = u[1 + u.rfind('/'):u.find('?')]
		get_item_images(u, item_id, f)
#ищем в супе изображения, качаем их и записываем в файлы. Это большие картинки, для миниатюр другие ссылки надо выдёргивать


adr = 'https://rostovondon.moychay.ru/catalog/ulun/yuzhnofudzyanskij_ulun'
i = catalog_page_parser(adr)
for key in i.keys():
	item_parser(i[key])