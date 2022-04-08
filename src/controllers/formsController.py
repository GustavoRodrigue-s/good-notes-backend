from models.db.connection import connectionDB

from models.entities.App import App
from models.entities.User import User

from datetime import datetime

def createNewUserInDbHandler(user):

   User.setNewIdForCurrentUser(user)

   currentDate = datetime.today().strftime('%Y-%m-%d %H:%M')

   apiKey = User.setNewApiKeyForCurrentUser(user.id)

   connectionDB('addUser', {
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'password': user.password[0],
      'apiKey': apiKey,
      'currentDate': currentDate
   })


def loginFormHandler(requestData):

   user = User(requestData)

   hasUser = connectionDB('getOneUser', {
      'item': '*',
      'condition': "email = %s AND password = %s OR username = %s AND password = %s",
      'datas': (user.email, user.password, user.email, user.password)
   })

   App.checkLoginErrors(user, hasUser)

   user.id = hasUser[0]


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