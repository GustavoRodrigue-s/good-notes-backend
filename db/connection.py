import psycopg2
from app.models.DbActions import DbActions

def connectionDB(action, data):
   try:
      dbConnection = psycopg2.connect(
         host = 'ec2-3-232-22-121.compute-1.amazonaws.com',
         dbname = 'd5pgvpckltfutt',
         user = 'nhbwthpxduwbgk',
         password = '6d80cc40b58a27349796b638a004c182fca40212ed615fa9be9e00e24ce99cc2',
         port = 5432
      )

      cursor = dbConnection.cursor()

      databaseActions = DbActions(cursor)

      chooseAction = { 
         'createTable': databaseActions.createTable,
         'insertUser': databaseActions.insertUser,
         'getOneUser': databaseActions.getOneUser,
         'getAllUsers': databaseActions.getAllUsers,
         'updateUser': databaseActions.updateUser,
         'deleteUser': databaseActions.deleteUser    
      }

      responseData = chooseAction[action](data)

      dbConnection.commit()
      cursor.close()
      dbConnection.close()

      return responseData

   except:
      cursor.close()
      dbConnection.close()

      raise Exception('This option is not exists.')