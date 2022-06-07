from flask import request, json, jsonify

from app.models.User import User

import base64, hashlib, os

from app.controllers.AuthController import AuthController

class UseUserController():
   def store(self):
      try:

         data = json.loads(request.data)
      
         user = User(data)

         hasSomeError = user.validateSignUp()

         if hasSomeError:
            return jsonify({ "errors": hasSomeError, "state": "error" }, 401)

         user.create()

         accessToken, refreshToken = AuthController.createAuthentication(user)
         
         return jsonify (
            {
               "state": "success",
               "reason": "all right",
               "userData": { 'accessToken': accessToken, 'refreshToken': refreshToken }
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

         photo = self.getPhoto(credentials[4]) if credentials[4] else None

         return jsonify(
            { 
               'state': 'success',
               'username': credentials[1],
               'email': credentials[2],
               'photo': photo
            }, 200
         )

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def getPhoto(self, photoName):
      
      imgExtension = photoName.split('.')[1]

      directory = os.path.join(os.getcwd() + '\\src\\uploads\\', photoName)
      imgData = open(directory, 'rb')

      if not imgData:
         return None

      imgBase64 = base64.b64encode(imgData.read())
      imgFormated = f'data:image/{imgExtension};base64,{imgBase64}'.replace("b'", '').replace("'", '')

      return imgFormated

   def updateStore(self, userId):
      try:

         requestData = json.loads(request.data)

         user = User(requestData)

         user.id = userId

         userEmailExists = user.findOne('email = %s AND id <> %s', user.email, user.id)
         userUsernameExists = user.findOne('username = %s AND id <> %s', user.username, user.id)

         hasSomeError = user.validateUsernameAndEmail(userEmailExists, userUsernameExists)

         if hasSomeError:
            return jsonify({ 'state': 'error', 'reason': hasSomeError }, 403)

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

   def uploadPhoto(self, userId):
      try:

         photoDatas = json.loads(request.data)

         user = User({})
         user.id = userId

         user.validatePhotoUpload(photoDatas)

         photoBase64 = photoDatas['photo'].split('base64,')[1]
         photoBytes = base64.b64decode(photoBase64)

         filename = hashlib.md5(os.urandom(16)).hexdigest() + photoDatas['name']

         lastPhotoName = user.findOne('id = %s', user.id)[4]

         user.uploadPhoto(filename)

         directory = os.getcwd() + '\\src\\uploads\\'
         newPhoto = os.path.join(directory, filename)

         if lastPhotoName:
            oldPhoto = os.path.join(directory, lastPhotoName)
            os.remove(oldPhoto)
         
         with open(newPhoto, 'wb') as photo:
            photo.write(photoBytes) 

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)


UserController = UseUserController()