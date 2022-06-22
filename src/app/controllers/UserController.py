from flask import request, json, jsonify

from app.models.User import User

from app.controllers.AuthController import AuthController

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

         emailConfirmationToken = user.sendEmailCode(activateCode)

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

         userEmailExists = user.findOne('email = %s AND id <> %s', user.email, user.id)
         userUsernameExists = user.findOne('username = %s AND id <> %s', user.username, user.id)

         hasSomeError = user.validateUsernameAndEmail(userEmailExists, userUsernameExists)

         if hasSomeError:
            return jsonify({ 'state': 'error', 'errors': hasSomeError }, 403)

         user.update('username = %s', 'id = %s', user.username, user.id)

         userExists = user.findOne('id = %s', user.id)

         resp = { 'state': 'success' }
         
         if user.email != userExists[2]:
            resp['emailConfirmationToken'] = user.sendEmailCode()

         return jsonify(resp, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def updateEmail(self, userId):
      try:
         requestData = json.loads(request.data)

         emailConfirmationCode = requestData['emailConfirmationCode']
         newEmail = requestData['newEmail']
         
         user = User({ 'email': newEmail })
         user.id = userId

         user.validateEmailConfirmationCode(emailConfirmationCode)

         user.update('email = %s', 'id = %s', user.email, user.id)

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

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

         user.update('password = %s', 'id = %s', user.password, user.id)

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

   def sendEmailConfirmation(self):
      try:
         requestData = json.loads(request.data)

         email = requestData['email'] 

         user = User({ 'email': email })
         
         userExists = user.findOne('email = %s', user.email)

         if not userExists:
            raise Exception('user not found')

         user.id = userExists[0]
         user.username = userExists[1]
         user.email = requestData['emailToUpdate'] if 'emailToUpdate' in requestData else user.email

         emailConfirmationToken = user.sendEmailCode()

         return jsonify(
            { 
               'state': 'success',
               'userData': { 
                  'emailConfirmationToken': emailConfirmationToken 
               } 
            }, 200
         )

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   def activateAccount(self, userId):
      try:
         requestData = json.loads(request.data)

         emailConfirmationCode = requestData['emailConfirmationCode']
         sessionConnected = requestData['keepConnected']

         user = User({ 'keepConnected': sessionConnected })
         user.id = userId

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
      

UserController = UseUserController()