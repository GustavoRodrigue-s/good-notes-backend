from flask import jsonify
from services.token import generateToken, decodeToken

import jwt

from services.tokenKey import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
from controllers.apiKeyController import getApiKeyHandler

sessionIdBlackList = []

# inicia uma sessão
def createSessionHandler(user):

   userId = user.getId()

   if userId in sessionIdBlackList:
      sessionIdBlackList.remove(userId)

   apiKey = getApiKeyHandler(userId)

   accessToken = generateToken(userId, ACCESS_TOKEN_KEY, 5)
   refreshToken = generateToken(userId, REFRESH_TOKEN_KEY, 10)

   return { 'accessToken': accessToken, 'refreshToken': refreshToken  }, apiKey

   
# cria um novo accessToken
def restoreSessionHandler(refreshToken):

   try:
      decoded = decodeToken(refreshToken, REFRESH_TOKEN_KEY)
      userId = decoded['id']

      if userId in sessionIdBlackList:
         raise Exception('the session is not valid')

      newAccessToken = generateToken(userId, ACCESS_TOKEN_KEY, 5)

      return newAccessToken

   except jwt.ExpiredSignatureError:
      raise Exception('expired refreshToken')
   except jwt.InvalidTokenError:
      raise Exception('invalid refreshToken')
   except Exception as e:
      raise Exception(e)


# invalida o id do usuário
def deleteSessionHandler(userId):
   
   sessionIdBlackList.append(userId)
