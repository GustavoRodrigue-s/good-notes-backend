import sys

sys.path.insert(1, './')
from db.connection import connectionDB
from app.models.App import App

def handleLoginErrors(user):
    
   userDatabase = connectionDB('getOneUser', {
      'item': '*',
      'condition': f"email = '{user.email}' OR username = '{user.email}'"
   })

   App.checkLoginErrors(user, userDatabase)

   user.id = userDatabase[0]