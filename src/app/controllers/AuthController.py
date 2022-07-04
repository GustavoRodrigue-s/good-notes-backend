from flask import request, json, jsonify

from services.JwtService import JwtService
from services.EmailService import EmailService

from random import randint

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

         accountActivated = userExists[8]

         user.id = userExists[0]
         user.username = userExists[1]
         user.email = userExists[2]

         if not accountActivated:
            code = randint(10000, 99999) 
         
            user.update('verification_code = %s', 'id = %s', code, user.id)

            emailConfirmationToken = JwtService.createToken(
               { 'auth': 'active account', 'id': user.id },
               os.environ.get('EMAIL_CONFIRMATION_TOKEN_KEY'), 15
            )

            emailData = EmailService.createActivationMailData(user, code)

            EmailService.sendMail(emailData)
         
            return jsonify({
               'state': 'error',
               'reason': 'account not activated',
               'userData': {
                  'emailConfirmationToken': emailConfirmationToken,
                  'sessionEmail': user.email
               } 
            }, 301)

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
         return jsonify({ "state": "error", "reason": f'{e}' }, 401)

   def createAuthentication(self, user):
      try:
         if user.id in sessionIdBlackList:
            sessionIdBlackList.remove(user.id)

         refreshTokenTime = 43200 if user.keepConnected else 1440

         accessToken = JwtService.createToken({ 'id': user.id }, os.environ.get('ACCESS_TOKEN_KEY'), 10)
         refreshToken = JwtService.createToken({ 'id': user.id }, os.environ.get('REFRESH_TOKEN_KEY'), refreshTokenTime)

         return accessToken, refreshToken

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def restoreAuthentication(self, refreshToken):
      try:
         userId = JwtService.readToken(refreshToken, os.environ.get('REFRESH_TOKEN_KEY'))['id']

         if userId in sessionIdBlackList:
            raise Exception('the session is not valid')

         newAccessToken = JwtService.createToken({ 'id': userId }, os.environ.get('ACCESS_TOKEN_KEY'), 10)

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