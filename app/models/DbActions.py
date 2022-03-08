class DbActions:
   def __init__(self, cursor):
      self.cursor = cursor

   def createTable(self, none):
      self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
         id          VARCHAR(5) PRIMARY KEY NOT NULL,
         username    VARCHAR(255) NOT NULL,
         email       VARCHAR(255) NOT NULL,
         password    VARCHAR(50)  NOT NULL,
         apiKey      VARCHAR(21)  NOT NULL,
         date        VARCHAR(19)  NOT NULL
      ) ''')
   
   def insertUser(self, data):
      self.cursor.execute(
         "INSERT INTO users(id, username, email, password, apiKey, date) VALUES(%s,%s,%s,%s,%s,%s)",
         (data['id'], data['username'], data['email'], data['password'], data['apiKey'], data['currentDate'])
      )

   def getOneUser(self, data):
      self.cursor.execute(f'''SELECT {data['item']} FROM users WHERE {data['condition']}''', data['datas'])
      response = self.cursor.fetchone()

      return response

   def getAllUsers(self, data):
      self.cursor.execute(f"SELECT {data['item']} FROM users")
      response = self.cursor.fetchall()

      return response

   # Make treatment of sql injection
   def updateUser(self, data):
      self.cursor.execute(
         f'''UPDATE users SET {data['column']} = '{data['newValue']}' WHERE id = '{data['id']}'
         RETURNING * '''
      )
      response = self.cursor.fetchone()

      return response
   
   def deleteUser(self, data):
      self.cursor.execute(f"DELETE FROM users WHERE id = '{data['id']}'")