import sys

sys.path.insert(1, './')
from db.connection import connectionDB
from app.models.App import App

def handleRegistrationErrors(user):

   userDatabaseWithEmail = connectionDB('getOneUser', {'item': '*', 'condition': f"email = '{user.email}'"})
   userDatabaseWithUsername = connectionDB('getOneUser', {'item': '*', 'condition': f"username = '{user.username}'"})

   App.checkRegistrationErrors(user, {
      "userWithEmail": userDatabaseWithEmail,
      "userWithUsername": userDatabaseWithUsername 
   })