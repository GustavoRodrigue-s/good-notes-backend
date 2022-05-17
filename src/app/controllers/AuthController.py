from flask import request, json, jsonify

from services import jwtService

from dotenv import load_dotenv
import os

from app.models.User import User

load_dotenv()

sessionIdBlackList = []

# auth (todo momento do usuário autenticado ou que vai autenticar) 

class UseAuthController():
   def authenticate(self):

      data = json.loads(request.data)

      user = User(data)

      userExists = user.findOneUser('email = %s OR username = %s', user.email, user.email)

      hasSomeError = user.validateSignIn(userExists)

      if hasSomeError:
         return jsonify({"errors": hasSomeError, "state": "error"}, 401)

      user.id = userExists[0]

      accessToken, refreshToken = self.createAuthentication(user)

      return jsonify({
         "state": "success",
         "reason": "all right",
         "userData": { 
            'accessToken': accessToken,
            'refreshToken': refreshToken
         }
      }, 200)

   def createAuthentication(self, user):

      if user.id in sessionIdBlackList:
         sessionIdBlackList.remove(user.id)

      accessToken = jwtService.generateToken(user.id, os.environ.get('ACCESS_TOKEN_KEY'), 5)

      refreshToken = jwtService.generateToken(
         user.id, os.environ.get('REFRESH_TOKEN_KEY'), 43200 if user.keepConnected else 1440
      )

      return accessToken, refreshToken

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