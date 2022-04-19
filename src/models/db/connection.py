import psycopg2
from models.entities.DbActions import DbActions
import os

def connectionDB(action, data):
   try:
      dbConnection = psycopg2.connect(
         host = os.environ.get('DATABASE_HOST'),
         dbname = os.environ.get('DATABASE_NAME'),
         user = os.environ.get('DATABASE_USER'),
         password = os.environ.get('DATABASE_PASSWORD'),
         port = os.environ.get('DATABASE_PORT')
      )

      cursor = dbConnection.cursor()

      databaseActions = DbActions(cursor)

      chooseAction = {
         'createTable': databaseActions.createTable,
         'addUser': databaseActions.insertUser,
         'getOneUser': databaseActions.getOneUser,
         'updateUser': databaseActions.updateUser,
         'deleteUser': databaseActions.deleteUser,
         'getUserWithSomeCredentials': databaseActions.getUserWithSomeCredentials,
         'addCategory': databaseActions.insertCategory,
         'deleteCategory': databaseActions.deleteCategory,
         'updateCategory': databaseActions.updateCategory,
         'getCategories': databaseActions.getCategories,
         'getNotes': databaseActions.getNotes,
         'insertNote': databaseActions.insertNote,
         'deleteNote': databaseActions.deleteCategory,
         'updateNote': databaseActions.updateNote
      }

      responseData = chooseAction[action](data)

      dbConnection.commit()
      cursor.close()
      dbConnection.close()

      return responseData

   except Exception as e:
      cursor.close()
      dbConnection.close()

      print(e)

      raise Exception('This option is not exists.')