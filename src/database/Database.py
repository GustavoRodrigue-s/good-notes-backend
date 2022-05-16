import psycopg2
import os

class UseDatabase:

   def __init__(self):
      self.host = os.environ.get('DATABASE_HOST')
      self.dbname = os.environ.get('DATABASE_NAME')
      self.user = os.environ.get('DATABASE_USER')
      self.password = os.environ.get('DATABASE_PASSWORD')
      self.port = os.environ.get('DATABASE_PORT')

   def connect(self):
      
      connection = psycopg2.connect(
         host = self.host,
         dbname = self.dbname,
         user = self.user,
         password = self.password,
         port = self.port
      )

      cursor = connection.cursor()

      return cursor, connection
   
   def disconnect(self, cursor, connection):
      connection.commit()
      cursor.close()
      connection.close()


Database = UseDatabase()