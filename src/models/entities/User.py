from models.db.connection import connectionDB
from random import sample

class User:
   def __init__(self, user):
      try:
         self.username = user['username'] 
      except:
         self.username = ""

      self.email = user['email']
      self.password = user['password']

   @staticmethod
   def setNewIdForCurrentUser(currentUser):
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

      currentUser.id = randomId

      return randomId

   @staticmethod
   def getCurrentUserId(currentUser):
      currentId = connectionDB('getOneUser', {
         'item': 'id',
         'condition': "email = %s OR username = %s",
         'datas': (currentUser.email, currentUser.email)
      })[0]

      return currentId

   @staticmethod
   def getApiKeyHandler(currentUserId):
      
      apiKey = connectionDB('getOneUser', {
         'item': 'apiKey',
         'condition': "id = %s",
         'datas': (currentUserId,)
      })[0]

      return apiKey

   @staticmethod
   def setNewApiKeyForCurrentUser(currentUserId):
      letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

      randomKey = ''.join(sample(letters, 15))

      apiKey = randomKey + "-" + currentUserId

      return apiKey