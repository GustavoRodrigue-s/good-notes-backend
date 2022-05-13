from database.connection import connectionDB

from app.models.App import App
from app.models.User import User

class UseUserController():
   def store(self, requestData):

      user = User(requestData)
   
      hasUserWithSomeCredentials = connectionDB('getUserWithSomeCredentials', {
         'condition1': "email = %s",
         'datas1': (user.email, ),
         'condition2': "username = %s",
         'datas2': (user.username, )
      })

      App.checkRegistrationErrors(user, hasUserWithSomeCredentials)

      User.setNewIdForCurrentUser(user)

      apiKey = User.setNewApiKeyForCurrentUser(user.id)

      user.password = User.hashPassword(user.password[0])

      connectionDB('addUser', {
         'id': user.id,
         'username': user.username,
         'email': user.email,
         'password': user.password,
         'apiKey': apiKey
      })

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