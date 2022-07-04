from dotenv import load_dotenv
import os

from random import randint

from flask import request, json, jsonify

from functools import reduce

from app.models.User import User

from app.controllers.AuthController import AuthController

from services.JwtService import JwtService
from services.EmailService import EmailService

load_dotenv()

class UseUserController():
   def store(self):
      try:
         data = json.loads(request.data)

         user = User(data)

         hasSomeError = user.validateSignUp()

         if hasSomeError:
            return jsonify({ "errors": hasSomeError, "state": "error" }, 401)

         code = randint(10000, 99999) 
         
         user.create(code)

         emailConfirmationToken = JwtService.createToken(
            { 'auth': 'active account', 'id': user.id },
            os.environ.get('EMAIL_CONFIRMATION_TOKEN_KEY'), 15
         )

         emailData = EmailService.createActivationMailData(user, code)

         EmailService.sendMail(emailData)

         return jsonify (
            {
               "state": "success",
               "reason": "all right",
               "userData": {
                  'emailConfirmationToken': emailConfirmationToken,
                  'sessionEmail': user.email 
               }
            }, 200
         )

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def destore(self, userId):
      try:
         user = User({})
         user.id = userId
         
         user.delete()

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def getStore(self, userId):
      try:

         user = User({})

         credentials = user.findOne('id = %s', userId)

         return jsonify(
            { 
               'state': 'success',
               'username': credentials[1],
               'email': credentials[2],
               'photo': credentials[4]
            }, 200
         )

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def updateStore(self, userId):
      try:
         requestData = json.loads(request.data)

         user = User(requestData)
         user.id = userId

         class AcceptedFields:
            def email(self):
               def validate():
                  userExists = user.findOne('email = %s AND id <> %s', user.email, user.id)
                  field['errors'] = user.validateEmail(userExists)

               def update():
                  userExists = user.findOne('id = %s', user.id)

                  user.username = user.username if user.username else userExists[1]

                  if user.email != userExists[2]:
                     code = randint(10000, 99999) 

                     user.update('verification_code = %s', 'id = %s', code, user.id)

                     token = JwtService.createToken(
                        { 'auth': 'update email', 'id': user.id, 'email': user.email },
                        os.environ.get('EMAIL_CONFIRMATION_TOKEN_KEY'), 15
                     )

                     emailData = EmailService.createConfirmationMailData(user, code)

                     EmailService.sendMail(emailData)

                     resp['userData'] =  { 'emailConfirmationToken': token } 

               field = { 'errors': [], 'validate': validate, 'update': update }

               return field

            def username(self):
               def validate():
                  userExists = user.findOne('username = %s AND id <> %s', user.username, user.id)
                  field['errors'] = user.validateUsername(userExists)

               def update():
                  user.update('username = %s', 'id = %s', user.username, user.id)

               field = { 'errors': [], 'validate': validate, 'update': update }    

               return field       

            def password(self):
               def validate():
                  field['errors'] = user.validatePassword(requestData['newPassword'])

               def update():
                  user.password = requestData['newPassword']
                  user.hashPassword()

                  user.update('password = %s', 'id = %s', user.password, user.id)

               field = { 'errors': [], 'validate': validate , 'update': update }

               return field

         acceptedFields = AcceptedFields()
         
         def getField(fieldName):
            return getattr(acceptedFields, fieldName)()

         fields = list(map(getField, requestData['changedFields']))

         for field in fields:
            field['validate']()

         hasSomeError = reduce(lambda acc, field: acc + field['errors'], fields, [])

         if hasSomeError:
            return jsonify({ 'state': 'error', 'errors': hasSomeError }, 403)

         resp = { 'state': 'success' }

         for field in fields:
            field['update']()

         return jsonify(resp, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def uploadPhoto(self, userId):
      try:
         photoDatas = json.loads(request.data)

         user = User({})
         user.id = userId

         user.validatePhotoUpload(photoDatas)

         photoUrl = user.uploadPhoto(photoDatas['photo'])

         return jsonify({ 'state': 'success', 'photoData': photoUrl }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def confirmEmailToUpdate(self, token):
      try:
         if token['auth'] != 'update email':
            raise Exception('token not authorized')

         requestData = json.loads(request.data)

         emailConfirmationCode = requestData['emailConfirmationCode']
         
         user = User(token)
         user.id = token['id']

         user.validateEmailConfirmationCode(emailConfirmationCode)

         user.update('email = %s', 'id = %s', user.email, user.id)

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def sendEmailToActivateAccount(self):
      try:
         requestData = json.loads(request.data)

         user = User(requestData)
         
         userExists = user.findOne('email = %s', user.email)

         if not userExists:
            raise Exception('user not found')

         user.id = userExists[0]
         user.username = userExists[1]

         code = randint(10000, 99999) 

         user.update('verification_code = %s', 'id = %s', code, user.id)

         token = JwtService.createToken(
            { 'auth': 'active account', 'id': user.id },
            os.environ.get('EMAIL_CONFIRMATION_TOKEN_KEY'), 15
         )

         emailData = EmailService.createActivationMailData(user, code)

         EmailService.sendMail(emailData)

         return jsonify(
            { 
               'state': 'success',
               'userData': { 
                  'emailConfirmationToken': token 
               } 
            }, 200
         )

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def activateAccount(self, token):
      try:
         if token['auth'] != 'active account':
            raise Exception('token not authorized')

         requestData = json.loads(request.data)

         emailConfirmationCode = requestData['emailConfirmationCode']
         sessionConnected = requestData['keepConnected']

         user = User({ 'keepConnected': sessionConnected })
         user.id = token['id']

         user.validateEmailConfirmationCode(emailConfirmationCode)

         user.update('active = %s', 'id = %s', 'TRUE', user.id)

         accessToken, refreshToken = AuthController.createAuthentication(user)

         return jsonify(
            {
               'state': 'success',
               'userData': { 
                  'accessToken': accessToken,
                  'refreshToken': refreshToken
               }
            }, 200
         )

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def forgotPassword(self):
      try:
         credentials = json.loads(request.data)

         user = User(credentials)

         userExists = user.findOne('email = %s', user.email)

         hasSomeError = user.validateForgotPassword(userExists)

         if hasSomeError:
            return jsonify({ "errors": hasSomeError, "state": "error" }, 401)

         user.id = userExists[0]
         user.username = userExists[1]

         user.hashPassword()

         code = randint(10000, 99999) 

         user.update('verification_code = %s', 'id = %s', code, user.id)

         token = JwtService.createToken(
            { 'auth': 'reset password', 'id': user.id, 'password': user.password },
            os.environ.get('EMAIL_CONFIRMATION_TOKEN_KEY'), 15
         )

         emailData = EmailService.createPasswordResetMailData(user, code)

         EmailService.sendMail(emailData)

         return jsonify({
            'state': 'success',
            'userData': {
               'emailConfirmationToken': token
            } 
         }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def resetPassword(self, token):
      try:
         if token['auth'] != 'reset password':
            raise Exception('token not authorized')

         emailConfirmationCode = json.loads(request.data)['emailConfirmationCode']

         user = User(token)
         user.id = token['id']

         user.validateEmailConfirmationCode(emailConfirmationCode)

         user.update('password = %s', 'id = %s', user.password, user.id)

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)
      

UserController = UseUserController()