from app.models.User import User
from app.models.App import App

from db.connection import connectionDB

def updateUser(userId, newDatas):
   # colocar isso tudo dentro do user (depois)

   wrongErrors = []

   if newDatas['email'] == '':
      wrongErrors.append({'input': 'input-email', 'reason': 'empty input'})

   if newDatas['username'] == '':
      wrongErrors.append({'input': 'input-username', 'reason': 'empty input'})

   if wrongErrors != []:
      raise Exception(wrongErrors)

   newUserCredentials = User.updateUserCredentials(userId, newDatas)

   if newUserCredentials != None:
      return newUserCredentials

   hasUsername =  connectionDB('getOneUser', {
      "item": '*',
      'condition': "username = %s AND id <> %s",
      'datas': (newDatas['username'], userId)
   })

   hasEmail = connectionDB('getOneUser', {
      'item': '*',
      'condition': 'email = %s AND id <> %s',
      'datas': (newDatas['email'], userId)
   })

   App.checkNewCredentials(hasUsername, hasEmail)

   