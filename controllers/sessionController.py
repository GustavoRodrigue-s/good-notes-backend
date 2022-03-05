from services.jwtToken import generateToken, decodeToken

from dotenv import load_dotenv

import jwt, os

from controllers.apiKeyController import getApiKeyHandler

# load_dotenv()

sessionIdBlackList = []

# inicia uma sessão
def createSessionHandler(user, keepConnected):
   
   if user.id in sessionIdBlackList:
      sessionIdBlackList.remove(user.id)

   apiKey = getApiKeyHandler(user.id)

   print(user.id, os.environ.get('ACCESS_TOKEN_KEY'))

   accessToken = generateToken(user.id, os.environ.get('ACCESS_TOKEN_KEY'), 5)

   if keepConnected == True: refreshTokenExpirationTime = 43200
   else: refreshTokenExpirationTime = 1440

   print(keepConnected, refreshTokenExpirationTime)

   refreshToken = generateToken(user.id, os.environ.get('REFRESH_TOKEN_KEY'), refreshTokenExpirationTime)

   return { 'accessToken': accessToken, 'refreshToken': refreshToken  }, apiKey

   
# cria um novo accessToken
def restoreSessionHandler(refreshToken):
   try:
      decoded = decodeToken(refreshToken, os.environ.get('REFRESH_TOKEN_KEY'))
      userId = decoded['id']

      if userId in sessionIdBlackList:
         raise Exception('the session is not valid')

      newAccessToken = generateToken(userId, os.environ.get('ACCESS_TOKEN_KEY'), 5)

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