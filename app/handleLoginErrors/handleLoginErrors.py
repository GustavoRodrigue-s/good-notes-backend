import sys

sys.path.insert(1, './')
from db.connection import connectionDB
from app.models.App import App

def handleLoginErrors(user):

   userDatabase = connectionDB('getOneUser', {
      'item': '*',
      'condition': "email = %s AND password = %s OR username = %s AND password = %s",
      'datas': (user.email, user.password, user.email, user.password)
   })

   App.checkLoginErrors(user, userDatabase)

   user.id = userDatabase[0]