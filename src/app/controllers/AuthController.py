from services import jwtService

from dotenv import load_dotenv
import os

from database.Database import connectionDB

from app.models.User import User
from app.models.App import App

load_dotenv()

sessionIdBlackList = []

# auth (todo momento do usuário autenticado ou que vai autenticar)

class UseAuthController():
   def authenticate(self, requestData):
      user = User(requestData)

      userDB = connectionDB('getOneUser', {
         'item': '*',
         'condition': "email = %s OR username = %s",
         'datas': (user.email, user.email)
      })

      hasUserInDB = list(userDB) if userDB else userDB

      if hasUserInDB:
         hasUserInDB[3] = User.decryptHashPassword(hasUserInDB[3])

      App.checkLoginErrors(user, hasUserInDB)

      user.id = hasUserInDB[0]

      accessToken, refreshToken, apiKey = self.createAuthentication(user, requestData['keepConnected'])

      return { 
         'accessToken': accessToken,
         'refreshToken': refreshToken,
         'apiKey': apiKey 
      }

   def createAuthentication(self, user, keepConnected):

      if user.id in sessionIdBlackList:
         sessionIdBlackList.remove(user.id)

      apiKey = User.getApiKeyHandler(user.id)

      accessToken = jwtService.generateToken(user.id, os.environ.get('ACCESS_TOKEN_KEY'), 5)

      refreshTokenExpirationTime = 43200 if keepConnected else 1440

      refreshToken = jwtService.generateToken(user.id, os.environ.get('REFRESH_TOKEN_KEY'), refreshTokenExpirationTime)

      return accessToken, refreshToken, apiKey

# talvez colocar esse restore no middleware auth
   def restoreAuthentication(self, refreshToken):
      
      userId = jwtService.decodeRefreshToken(refreshToken, os.environ.get('REFRESH_TOKEN_KEY'))

      if userId in sessionIdBlackList:
         raise Exception('the session is not valid')

      newAccessToken = jwtService.generateToken(userId, os.environ.get('ACCESS_TOKEN_KEY'), 5)

      return newAccessToken

   def exitAuthentication(self, userId):

      sessionIdBlackList.append(userId)


AuthController = UseAuthController()