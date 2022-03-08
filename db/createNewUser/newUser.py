from db.connection import connectionDB
from controllers.apiKeyController import createApiKeyHandler

from datetime import datetime

def addNewUser(user):

   user.generateId() 

   currentDate = datetime.today().strftime('%Y-%m-%d %H:%M')

   apiKey = createApiKeyHandler(user.id)

   connectionDB('insertUser', {
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'password': user.password[0],
      'apiKey': apiKey,
      'currentDate': currentDate
   })