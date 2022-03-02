import sqlite3

def connectionDB(functionToExecute, connectionConfig):
   connectionDatabase = sqlite3.connect('db/users.db')
   cursor = connectionDatabase.cursor()

   if connectionConfig['toAddUser']:
      cursor.execute(functionToExecute[0], functionToExecute[1])
   else:
      cursor.execute(functionToExecute)

   if connectionConfig['getAllUsers']:
      data = cursor.fetchall()
   else:
      data = cursor.fetchone()

   connectionDatabase.commit()
   cursor.close()
   connectionDatabase.close()

   return data