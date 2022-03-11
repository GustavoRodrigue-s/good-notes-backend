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

      while True:
         randomId = ''.join(sample(letters, 5))

         userOfdb = connectionDB('getOneUser', {
            'item': '*',
            'condition': "id = %s",
            'datas': (randomId,)
         })

         if userOfdb == None:
            break                

      self.id = randomId

      return randomId

   def getId(self):
      userId = connectionDB('getOneUser', {
         'item': 'id',
         'condition': "email = %s OR username = %s",
         'datas': (self.email, self.email)
      })

      return userId[0]

   @staticmethod
   def getUserCredentials(userId):
      response = connectionDB('getOneUser', {
         'item': '*',
         'condition': "id = %s",
         'datas': (userId, )
      })

      return response

   @staticmethod
   def updateUserCredentials(userId, newDatas):
      newDatas['id'] = userId

      response = connectionDB('updateUser', newDatas)

      return response

   @staticmethod
   def deleteAccount(userId):
      connectionDB('deleteUser', {"datas": (userId, )})
