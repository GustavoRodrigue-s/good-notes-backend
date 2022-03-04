from db.connection import connectionDB

def getUserDatas(userId):

   userCredentials = connectionDB('getOneUser', {
      'item': '*',
      'condition': f"id = '{userId}'" 
   })

   return userCredentials