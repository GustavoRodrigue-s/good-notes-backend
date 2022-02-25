import sys

sys.path.insert(1, '../')
from db.connection import connectionDB
from app.app import App

def handleRegistrationErrors(user):

   functionToExecuteEmail = f'select * from users where email = "{user.email}"'
   functionToExecuteUsername = f'select * from users where username = "{user.username}"'

   userDatabaseWithEmail = connectionDB(functionToExecuteEmail, { 'toAddUser': False, 'getAllUsers': False })
   userDatabaseWithUsername = connectionDB(functionToExecuteUsername, { 'toAddUser': False, 'getAllUsers': False })

   App.checkRegistrationErrors(user, {
      "userWithEmail": userDatabaseWithEmail,
      "userWithUsername": userDatabaseWithUsername 
   })
