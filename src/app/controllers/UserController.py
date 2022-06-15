from flask import request, json, jsonify

import smtplib, os, sys

from app.models.User import User

from app.controllers.AuthController import AuthController
from services.JwtProvider import JwtProvider

sys.path.insert(1, './')

from emailTemplates.activeCode import createEmailActiveCodeTemplate

from email.message import EmailMessage
from random import randint

from dotenv import load_dotenv

load_dotenv()

class UseUserController():
   def store(self):
      try:

         data = json.loads(request.data)
      
         user = User(data)

         hasSomeError = user.validateSignUp()

         if hasSomeError:
            return jsonify({ "errors": hasSomeError, "state": "error" }, 401)

         activateCode = user.create()

         activationToken = JwtProvider.createToken(user.id, os.environ.get('ACTIVATION_TOKEN_KEY'), 15)

         self.sendActivationCode(user.email, user.username, activateCode)

         return jsonify (
            {
               "state": "success",
               "reason": "all right",
               "userData": {
                  'activationToken': activationToken
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

         userEmailExists = user.findOne('email = %s AND id <> %s', user.email, user.id)
         userUsernameExists = user.findOne('username = %s AND id <> %s', user.username, user.id)

         hasSomeError = user.validateUsernameAndEmail(userEmailExists, userUsernameExists)

         if hasSomeError:
            return jsonify({ 'state': 'error', 'errors': hasSomeError }, 403)

         user.updateUsernameAndEmail()

         return jsonify({
            'state': 'success',
            'newDatas': {
               'email': user.email,
               'username': user.username 
            }
         }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def updatePassword(self, userId):
      try:

         requestData = json.loads(request.data)

         user = User({ 'password': requestData['oldPassword'] })
         user.id = userId

         hasSomeError = user.validateUpdatePassword(requestData['newPassword'])

         if hasSomeError:
            return jsonify({ 'errors': hasSomeError, 'state': 'error' }, 401)

         user.password = requestData['newPassword']
         user.hashPassword()

         user.updatePassword()

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

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

   # mandar para o models
   def sendActivationCode(self, userEmail, userNickname, randomCode):

      msg = EmailMessage()
      msg['Subject'] = "Código de Ativação - Good Notes"
      msg['From'] = os.environ.get('EMAIL_ADDRESS')
      msg['To'] = userEmail

      msg.add_alternative(createEmailActiveCodeTemplate(userNickname, randomCode), subtype='html')

      smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      smtp.login(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD'))
      smtp.send_message(msg)

   def resendingActivationCode(self):
      try:

         if not 'Authorization' in request.headers:
            raise Exception('no activation token')

         activationToken = JwtProvider.createToken(user.id, os.environ.get('ACTIVATION_TOKEN_KEY'), 15)

         self.sendActivationCode(user.email, user.username, activateCode)

         return jsonify(
            { 
            'state': 'success',
            'userData': { 
               'activationToken': activationToken 
               } 
            }, 200
         )

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def checkActivationCode(self):
      try:

         if not 'Authorization' in request.headers:
            raise Exception('no activation token')

         activationToken = request.headers['Authorization']
         activationCode = json.loads(request.data)['activationCode']

         id = JwtProvider.readToken(activationToken, os.environ.get('ACTIVATION_TOKEN_KEY'))['id']

         user = User({})
         user.id = id

         user.validateActivationCode(activationCode)

         user.update('active = %s', 'id = %s', 'TRUE', id)

         accessToken, refreshToken = AuthController.createAuthentication(user)

         return jsonify(
            { 
               'state': 'success',
               "userData": { 
                  'accessToken': accessToken,
                  'refreshToken': refreshToken
               }
            }, 200
         )

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)
      

UserController = UseUserController()