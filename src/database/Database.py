import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

class UseDatabase:

   def connect(self):
      
      dbConnection = psycopg2.connect(
         host = os.environ.get('DATABASE_HOST'),
         dbname = os.environ.get('DATABASE_NAME'),
         user = os.environ.get('DATABASE_USER'),
         password = os.environ.get('DATABASE_PASSWORD'),
         port = os.environ.get('DATABASE_PORT')
      )

      cursor = dbConnection.cursor()

      return cursor, dbConnection
   
   def disconnect(self, cursor, dbConnection):
      dbConnection.commit()
      cursor.close()
      dbConnection.close()


Database = UseDatabase()