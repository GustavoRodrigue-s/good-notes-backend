from services.jwtToken import generateToken, decodeToken

from dotenv import load_dotenv

import jwt, os

from controllers.apiKeyController import getApiKeyHandler
from app.updateUser.update import updateUser

from app.models.User import User
from app.models.App import App

load_dotenv()

sessionIdBlackList = []

# inicia uma sessão
def createSessionHandler(user, keepConnected):
   
   if user.id in sessionIdBlackList:
      sessionIdBlackList.remove(user.id)

   apiKey = getApiKeyHandler(user.id)

   accessToken = generateToken(user.id, os.environ.get('ACCESS_TOKEN_KEY'), 5)

   if keepConnected == True: refreshTokenExpirationTime = 43200
   else: refreshTokenExpirationTime = 1440

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


def getSessionCredentialsHandler(userId):
   userCredentials = User.getUserCredentials(userId)

   return userCredentials


def updateSessionCredentialsHandler(userId, newDatas):
   newUserCredentials = updateUser(userId, newDatas)

   return { 'email': newUserCredentials[0], 'username': newUserCredentials[1] }


# invalida o id do usuário
def disableSessionHandler(userId):
   sessionIdBlackList.append(userId)


def deleteSessionHandler(userId):
   User.deleteAccount(userId)