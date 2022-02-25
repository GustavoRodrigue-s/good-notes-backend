from db.connection import connectionDB
from controllers.apiKeyController import createApiKeyHandler

def addNewUser(user):

   userId = user.generateId()

   apiKey = createApiKeyHandler(userId)

   functionToExecute = [
      'INSERT INTO users (username, email, password, id, apiKey) values(?, ?, ?, ?, ?)', 
      (f"{user.username}", f"{user.email}", f"{user.password}", f"{userId}", f"{apiKey}")
   ]

   connectionDB(functionToExecute, {
      'toAddUser': True,
      'getAllUsers': False
   })