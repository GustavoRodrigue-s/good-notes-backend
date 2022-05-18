from flask import request, json, jsonify

from services.jwtService import decodeToken, generateToken

from dotenv import load_dotenv
import os

from app.models.User import User

load_dotenv()

sessionIdBlackList = []

class UseAuthController():
   def authenticate(self):
      try:
         data = json.loads(request.data)

         user = User(data)

         userExists = user.findOne('email = %s OR username = %s', user.email, user.email)

         hasSomeError = user.validateSignIn(userExists)

         if hasSomeError:
            return jsonify({ "errors": hasSomeError, "state": "error" }, 401)

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

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def createAuthentication(self, user):
      try:

         if user.id in sessionIdBlackList:
            sessionIdBlackList.remove(user.id)

         accessToken = generateToken(user.id, os.environ.get('ACCESS_TOKEN_KEY'), 10)

         refreshToken = generateToken(
            user.id, os.environ.get('REFRESH_TOKEN_KEY'), 43200 if user.keepConnected else 1440
         )

         return accessToken, refreshToken

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def restoreAuthentication(self, refreshToken):
      try:

         userId = decodeToken(refreshToken, os.environ.get('REFRESH_TOKEN_KEY'))['id']

         if userId in sessionIdBlackList:
            raise Exception('the session is not valid')

         newAccessToken = generateToken(userId, os.environ.get('ACCESS_TOKEN_KEY'), 10)

         return newAccessToken

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def exitAuthentication(self, userId):
      try:

         sessionIdBlackList.append(userId)

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)


AuthController = UseAuthController()