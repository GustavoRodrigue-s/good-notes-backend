import sqlite3

def connectionDB(functionToExecute, connectionConfig):
   try:
      connectionDatabase = sqlite3.connect('../db/users.db')
      cursor = connectionDatabase.cursor()

      print('barbearia home')

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
   except sqlite3.Error as e:
      print(e)