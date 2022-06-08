from flask import request, json, jsonify

from app.models.User import User

import base64, hashlib, os

from app.controllers.AuthController import AuthController

directory = os.path.abspath('uploads')

print(directory)

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

         # talvez add isso no models direto no delete 
         photo = user.findOne('id = %s', user.id)[4]

         if photo:
            photoPath = os.path.join(directory, photo)
            os.remove(photoPath)
         
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
      
      photoExtension = photoName.split('.')[1]

      photoPath = os.path.join(directory, photoName)
      photoBytes = open(photoPath, 'rb')

      photoInBase64 = base64.b64encode(photoBytes.read())
      photoFormated = f'data:image/{photoExtension};base64,{photoInBase64}'.replace("b'", '').replace("'", '')

      return photoFormated

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

         photoBytes = base64.b64decode(photoDatas['photo'].split('base64,')[1])
         photoName = hashlib.md5(os.urandom(16)).hexdigest() + photoDatas['name']

         lastPhotoPath = user.findOne('id = %s', user.id)[4]

         user.uploadPhoto(photoName)

         if lastPhotoPath:
            oldPhoto = os.path.join(directory, lastPhotoPath)
            os.remove(oldPhoto)
         
         newPhotoPath = os.path.join(directory, photoName)

         with open(newPhotoPath, 'wb') as photo:
            photo.write(photoBytes) 

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)


UserController = UseUserController()