import sys

sys.path.insert(1, './')
from db.connection import connectionDB
from app.models.App import App

def handleRegistrationErrors(user):

   userDatabaseWithEmail = connectionDB('getOneUser', {
      'item': '*',
      'condition': "email = %s",
      'datas': (user.email, )
   })
   userDatabaseWithUsername = connectionDB('getOneUser', {
      'item': '*',
      'condition': "username = %s",
      'datas': (user.username, )
   })

   App.checkRegistrationErrors(user, {
      "userWithEmail": userDatabaseWithEmail,
      "userWithUsername": userDatabaseWithUsername 
   })