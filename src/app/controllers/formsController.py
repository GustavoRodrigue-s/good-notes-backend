from database.connection import connectionDB

from app.models.App import App
from app.models.User import User

def createNewUserInDbHandler(user):

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

def loginFormHandler(requestData):

   user = User(requestData)

   userDB = connectionDB('getOneUser', {
      'item': '*',
      'condition': "email = %s OR username = %s",
      'datas': (user.email, user.email)
   })

   hasUserInDB = list(userDB) if userDB else userDB

   if hasUserInDB:
      hasUserInDB[3] = User.decryptHashPassword(hasUserInDB[3])

   App.checkLoginErrors(user, hasUserInDB)

   user.id = hasUserInDB[0]

def registerFormHandler(requestData):

   user = User(requestData)
   
   hasUserWithSomeCredentials = connectionDB('getUserWithSomeCredentials', {
      'condition1': "email = %s",
      'datas1': (user.email, ),
      'condition2': "username = %s",
      'datas2': (user.username, )
   })

   App.checkRegistrationErrors(user, hasUserWithSomeCredentials)

   createNewUserInDbHandler(user)