from db.connection import connectionDB

def getUserDatas(userId):
   
   functionToExecute = f'SELECT * from users where id = "{userId}"'

   userCredentials = connectionDB(functionToExecute, { 'toAddUser': False, 'getAllUsers': False })

   return userCredentials