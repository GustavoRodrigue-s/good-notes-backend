from services import jwtService

from dotenv import load_dotenv
import os

from database.connection import connectionDB

from app.models.User import User
from app.models.App import App

load_dotenv()

sessionIdBlackList = []

# auth (todo momento do usuário autenticado ou que vai autenticar)

# o authenticate foi projetao para funcionar apenas no login...
class UseAuthController():
   def authenticate(self, requestData):
      user = User(requestData)

      print(user)

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

      # currentUser = User(requestData)
      # currentUser.id = User.getCurrentUserId(currentUser)

      if user.id in sessionIdBlackList:
         sessionIdBlackList.remove(user.id)

      apiKey = User.getApiKeyHandler(user.id)

      accessToken = jwtService.generateToken(user.id, os.environ.get('ACCESS_TOKEN_KEY'), 5)

      if requestData['keepConnected'] == True: refreshTokenExpirationTime = 43200
      else: refreshTokenExpirationTime = 1440

      refreshToken = jwtService.generateToken(user.id, os.environ.get('REFRESH_TOKEN_KEY'), refreshTokenExpirationTime)

      return { 'accessToken': accessToken, 'refreshToken': refreshToken, 'apiKey': apiKey  }

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