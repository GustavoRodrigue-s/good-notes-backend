from db.connection import connectionDB

def getUserDatas(userId):

   userCredentials = connectionDB('getOneUser', {
      'item': '*',
      'condition': "id = %s",
      'datas': (userId, )
   })

   return userCredentials