import sqlite3
connection = sqlite3.connect('D:\\moychay\\base\\products.db')
cursor = connection.cursor()
connection.close()
print('Woow!')