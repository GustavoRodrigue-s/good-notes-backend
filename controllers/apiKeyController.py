from functools import wraps
from random import sample

from db.connection import connectionDB
from flask import request, jsonify

def createApiKeyHandler(userId):

   letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

   randomKey = ''.join(sample(letters, 15))

   apiKey = randomKey + "-" + userId

   return apiKey


def getApiKeyHandler(userId):

   try:
      functionToExecute = f'SELECT * from users where id = "{userId}"'

      apiKey = connectionDB(functionToExecute, { 'toAddUser': False, 'getAllUsers': False })

      return apiKey[4]
   except:
      raise Exception('the api key is wrong')

   
# Decorator.
def apiKey_required(f):
   @wraps(f)
   def wrapper(*args, **kwargs):

      try:
         userApiKey = request.args.get('key')

         if userApiKey == '' or userApiKey == None:
            return jsonify({ 'state': 'unauthorized', 'reason': 'no api key' }, 403)

         userId = userApiKey.split('-')[1]

         apiKeyOfThisUser = getApiKeyHandler(userId)

         if userApiKey != apiKeyOfThisUser:
            return jsonify({ 'state': "unauthorized", 'reason': 'the api key is wrong' }, 401)
            
      except:
         return jsonify({ 'state': "unauthorized" }, 403)

      return f(*args, *kwargs)

   return wrapper