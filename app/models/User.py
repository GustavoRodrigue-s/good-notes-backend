from db.connection import connectionDB
from random import sample

class User:
   def __init__(self, user):
      try:
         self.username = user['username'] 
      except:
         self.username = ""

      self.email = user['email']
      self.password = user['password']

   def generateId(self):
      letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

      functionToExecute = "SELECT * FROM users"
      allUsersOfDB = connectionDB(functionToExecute, { 'toAddUser': False, 'getAllUsers': True })

      while True:
         randomId = ''.join(sample(letters, 5))

         repeatedId = False

         for userId in allUsersOfDB:
            if userId[3] == randomId:
               repeatedId = True
                  
         if repeatedId == False:
            break                

      return randomId

   def getId(self):
      functionToExecute = f'select * from users where email = "{self.email}" OR username = "{self.email}"'

      userDatabase = connectionDB(functionToExecute, { 'toAddUser': False, 'getAllUsers': False })

      id = userDatabase[3]

      return id

