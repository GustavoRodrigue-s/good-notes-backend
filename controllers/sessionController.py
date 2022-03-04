from services.jwtToken import generateToken, decodeToken

import jwt

from services.tokenKey import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
from controllers.apiKeyController import getApiKeyHandler

sessionIdBlackList = []

# inicia uma sessão
def createSessionHandler(user, keepConnected):
   
   if user.id in sessionIdBlackList:
      sessionIdBlackList.remove(user.id)

   apiKey = getApiKeyHandler(user.id)

   accessToken = generateToken(user.id, ACCESS_TOKEN_KEY, 5)

   if keepConnected: refreshTokenExpirationTime = 43200
   else: refreshTokenExpirationTime = 1440

   print(refreshTokenExpirationTime)

   refreshToken = generateToken(user.id, REFRESH_TOKEN_KEY, refreshTokenExpirationTime)

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