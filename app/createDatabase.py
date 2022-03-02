import sqlite3

def createDb():
   connectionDatabase = sqlite3.connect('db/users.db')

   cursor = connectionDatabase.cursor()

   try:
      cursor.execute('''create table users (
         username text,
         email text,
         password text,
         id text,
         apiKey text
      )''')

      connectionDatabase.commit()
      cursor.close()
      connectionDatabase.close()
   except:
      pass