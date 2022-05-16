from flask import request, json, jsonify

from database.connection import connectionDB

from app.models.App import App
from app.models.User import User

from app.controllers.AuthController import AuthController

class UseUserController():
   def store(self):

      user = json.loads(request.data)
   
      # colocar isso dentro de migrations
      existsUserWithSameCredentials = connectionDB('getUserWithSomeCredentials', {
         'condition1': "email = %s",
         'datas1': (user['email'], ),
         'condition2': "username = %s",
         'datas2': (user['username'], )
      })

      hasSomeErrors = App.checkRegistrationErrors(user, existsUserWithSameCredentials)

      if hasSomeErrors:
         # respData = [hasSomeErrors[0]] if type(hasSomeErrors[0]) != list else hasSomeErrors[0]

         return jsonify({"errors": hasSomeErrors, "state": "error"}, 401)


      # User.setNewIdForCurrentUser(user)

      apiKey = User.setNewApiKeyForCurrentUser(user.id)

      user.password = User.hashPassword(user.password[0])

      connectionDB('addUser', {
         'id': user.id,
         'username': user.username,
         'email': user.email,
         'password': user.password,
         'apiKey': apiKey
      })

      accessToken, refreshToken, apiKey = AuthController.createAuthentication(user, requestData['keepConnected'])

      # sessionData = AuthController.authenticate(user)

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

      newCredentials['id'] = userId

      hasUserWithSomeCredentials = connectionDB('getUserWithSomeCredentials', {
         'condition1': "email = %s AND id <> %s",
         'datas1': (newCredentials['email'], userId),
         'condition2': "username = %s AND id <> %s",
         'datas2': (newCredentials['username'], userId)
      })

      App.checkProfileErrors(newCredentials, hasUserWithSomeCredentials)

      newUserCredentials = connectionDB('updateUser', newCredentials)

      return { 'email': newUserCredentials[0], 'username': newUserCredentials[1] }


UserController = UseUserController()