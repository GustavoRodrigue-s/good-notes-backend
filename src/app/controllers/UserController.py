from flask import request, json, jsonify

from database.Database import connectionDB

from app.models.App import App
from app.models.User import User

from app.controllers.AuthController import AuthController

class UseUserController():
   def store(self):

      requestData = json.loads(request.data)
   
      user = User(requestData)

      hasSomeError = user.validateUserCreation()

      if hasSomeError:
         # respData = [hasSomeErrors[0]] if type(hasSomeErrors[0]) != list else hasSomeErrors[0]

         return jsonify({"errors": hasSomeError, "state": "error"}, 401)

      user.create()

      accessToken, refreshToken, apiKey = AuthController.createAuthentication(user, requestData['keepConnected'])

      sessionData = AuthController.authenticate(user)

      return jsonify (
         {
            "state": "success",
            "reason": "all right",
            "userData": { 'accessToken': accessToken, 'refreshToken': refreshToken, 'apiKey': apiKey }
         }, 200
      )


   def destore(self, userId):

      connectionDB('deleteUser', { 'userId': userId })

   def getStore(self, userId):

      userCredentials = connectionDB('getOneUser', {
         'item': '*',
         'condition': "id = %s",
         'datas': (userId, )
      })

      return userCredentials

   def updateStore(self, userId, newCredentials):

      # user = User(requestData) // usar isto

      newCredentials['id'] = userId

      # user.validateUsernameAndEmail()

      hasUserWithSomeCredentials = connectionDB('getUserWithSomeCredentials', {
         'condition1': "email = %s AND id <> %s",
         'datas1': (newCredentials['email'], userId),
         'condition2': "username = %s AND id <> %s",
         'datas2': (newCredentials['username'], userId)
      })

      App.checkProfileErrors(newCredentials, hasUserWithSomeCredentials)

      # n faz sentido retornar o mesmo valor do newCredentials
      newUserCredentials = connectionDB('updateUser', newCredentials)

      return { 'email': newUserCredentials[0], 'username': newUserCredentials[1] }


UserController = UseUserController()