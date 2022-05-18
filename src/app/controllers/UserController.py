from flask import request, json, jsonify

from app.models.User import User

from app.controllers.AuthController import AuthController

class UseUserController():
   def store(self):

      data = json.loads(request.data)
   
      user = User(data)

      hasSomeError = user.validateSignUp()

      if hasSomeError:
         return jsonify({"errors": hasSomeError, "state": "error"}, 401)

      user.create()

      accessToken, refreshToken = AuthController.createAuthentication(user)
      
      return jsonify (
         {
            "state": "success",
            "reason": "all right",
            "userData": { 'accessToken': accessToken, 'refreshToken': refreshToken }
         }, 200
      )

   def destore(self, userId):

      user = User({})

      user.id = userId
      
      user.delete()

      return jsonify({ 'state': 'success' }, 200)

   def getStore(self, userId):

      user = User({})

      credentials = user.findOne('id = %s', userId)

      return jsonify(
         { 
            'state': 'success',
            'username': credentials[1],
            'email': credentials[2] 
         }, 200
      )

   def updateStore(self, userId):

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


UserController = UseUserController()