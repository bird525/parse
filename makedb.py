import sqlite3
connection = sqlite3.connect('D:\\moychay\\base\\products.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE tea
				  (id integer primary key autoincrement, name text, description text)
			   ''')
cursor.execute('''CREATE TABLE tea_photos
				  (name text, ref text, item_id integer, FOREIGN KEY(item_id) REFERENCES tea(id))''')
connection.commit()
connection.close()
print('Woow!')