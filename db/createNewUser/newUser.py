from db.connection import connectionDB
from controllers.apiKeyController import createApiKeyHandler

def addNewUser(user):

   user.generateId()

   apiKey = createApiKeyHandler(user.id)

   connectionDB('insertUser', {
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'password': user.password[0],
      'apiKey': apiKey
   })