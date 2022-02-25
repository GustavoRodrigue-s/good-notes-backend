import sys

sys.path.insert(1, '../')
from db.connection import connectionDB
from app.app import App

def handleLoginErrors(user):
    
   functionToExecute = f'SELECT * from users WHERE email = "{user.email}" OR username = "{user.email}"'

   userDatabase = connectionDB(functionToExecute, { 'toAddUser': False, 'getAllUsers': False })

   App.checkLoginErrors(user, userDatabase)
