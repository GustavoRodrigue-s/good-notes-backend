import sqlite3

try:
   connectionDatabase = sqlite3.connect('users.db')
   cursor = connectionDatabase.cursor()

   cursor.execute('''create table users (
      username text,
      email text,
      password text,
      id text,
      apiKey text
   )''')

   print('criou o barato')

   connectionDatabase.commit()
   cursor.close()
   connectionDatabase.close()
except sqlite3.Error as e:
   print(e)