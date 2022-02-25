import sqlite3

connectionDatabase = sqlite3.connect('users.db')
cursor = connectionDatabase.cursor()

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