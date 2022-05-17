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

      # connectionDB('deleteUser', { 'userId': userId })
      return 'rtest'

   def getStore(self, userId):

      # userCredentials = connectionDB('getOneUser', {
      #    'item': '*',
      #    'condition': "id = %s",
      #    'datas': (userId, )
      # })

      return 'userCredentials'

   def updateStore(self, userId, newCredentials):

      # user = User(requestData) // usar isto

      newCredentials['id'] = userId

      # user.validateUsernameAndEmail()

      # hasUserWithSomeCredentials = connectionDB('getUserWithSomeCredentials', {
      #    'condition1': "email = %s AND id <> %s",
      #    'datas1': (newCredentials['email'], userId),
      #    'condition2': "username = %s AND id <> %s",
      #    'datas2': (newCredentials['username'], userId)
      # })

      App.checkProfileErrors(newCredentials, hasUserWithSomeCredentials)

      # n faz sentido retornar o mesmo valor do newCredentials
      # newUserCredentials = connectionDB('updateUser', newCredentials)

      return { 'email': newUserCredentials[0], 'username': newUserCredentials[1] }


UserController = UseUserController()