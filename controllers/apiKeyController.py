from random import sample

from db.connection import connectionDB

def createApiKeyHandler(userId):

   letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

   randomKey = ''.join(sample(letters, 15))

   apiKey = randomKey + "-" + userId

   return apiKey


def getApiKeyHandler(userId):

   try:
      apiKey = connectionDB('getOneUser', {
         'item': 'apiKey',
         'condition': "id = %s",
         'datas': (userId,)
      })[0]

      return apiKey
   except:
      raise Exception('the api key is wrong')