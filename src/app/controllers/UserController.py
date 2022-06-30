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

         emailConfirmationToken = user.sendActivationEmailCode(activateCode)

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

         print(requestData)

         user = User(requestData)
         user.id = userId

         hasSomeError = []
         approvedActions = []

         class CreateFieldInterface:
            def __init__(self, validate, update):
               self.state = False
               self.validate = validate
               self.update = update

         # transformar esses campos em dispatch field para criar um interface

         class AcceptedFields:
            def email(self):
               def validate():
                  userExists = user.findOne('email = %s AND id <> %s', user.email, user.id)
                  hasSomeError.extend(user.validateEmail(userExists))

               def update():
                  userExists = user.findOne('id = %s', user.id)

                  if user.email != userExists[2]:
                     resp['emailConfirmationToken'] = user.sendEmailCodeToUpdateEmail()

               field = CreateFieldInterface(validate, update)

               return field

            def username(self):
               def validate():
                  userExists = user.findOne('username = %s AND id <> %s', user.username, user.id)
                  hasSomeError.extend(user.validateUsername(userExists))

               def update():
                  user.update('username = %s', 'id = %s', user.username, user.id)

               field = CreateFieldInterface(validate, update)        

               return field       

            def password(self):
               hasSomeError.extend(user.validatePassword(requestData['newPassword']))

               def action():
                  user.password = requestData['newPassword']
                  user.hashPassword()

                  user.update('password = %s', 'id = %s', user.password, user.id)

               approvedActions.append(action)

            def emailAndUsername(self):
               self.email()
               self.username()

         acceptedFields = AcceptedFields()
         
         getattr(acceptedFields, requestData['currentField'])()

         if hasSomeError:
            return jsonify({ 'state': 'error', 'errors': hasSomeError }, 403)

         resp = { 'state': 'success' }

         for action in approvedActions:
            action()

         return jsonify(resp, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

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

   # dinamizar o payload
   def sendEmailConfirmation(self):
      try:
         requestData = json.loads(request.data)

         user = User(requestData)
         
         userExists = user.findOne('email = %s', user.email)

         if not userExists:
            raise Exception('user not found')

         user.id = userExists[0]
         user.username = userExists[1]
         user.email = requestData['emailToUpdate'] if 'emailToUpdate' in requestData else user.email

         token = user.sendActivationEmailCode()

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

         hasSomeError = user.validateForgotPassword()

         if hasSomeError:
            return jsonify({ "errors": hasSomeError, "state": "error" }, 401)

         userExists = user.findOne('email = %s', user.email)

         if not userExists:
            raise Exception('user not exists')

         user.id = userExists[0]
         user.username = userExists[1]

         token = user.sendPasswordResetEmailCode()

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

         user.hashPassword()
         user.update('password = %s', 'id = %s', user.password, user.id)

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)
      

UserController = UseUserController()