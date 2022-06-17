import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

class UseDatabase:

   def createTables(self):

      query = '''
         SET lc_time to 'pt_BR.UTF-8';
         SET TIMEZONE='America/Sao_Paulo';

         CREATE TABLE IF NOT EXISTS users(
            id                SERIAL NOT NULL,
            username          VARCHAR(255) NOT NULL,
            email             VARCHAR(255) NOT NULL,
            password          VARCHAR(255)  NOT NULL,
            photo_url         VARCHAR,
            photo_id          VARCHAR,
            datetime          TIMESTAMPTZ DEFAULT NOW(),
            verification_code VARCHAR(5) NOT NULL,
            active            BOOLEAN NOT NULL,
            PRIMARY KEY (id)
         );
  
         CREATE TABLE IF NOT EXISTS categories(
            id                SERIAL NOT NULL,
            user_id           INTEGER NOT NULL,
            category_name     VARCHAR(255) NOT NULL,
            datetime          TIMESTAMPTZ DEFAULT NOW(),
            last_update       TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES users(id)
         );
         
         CREATE TABLE IF NOT EXISTS notes(
            id                SERIAL NOT NULL,
            category_id       INTEGER NOT NULL,
            user_id           INTEGER NOT NULL,
            note_title        VARCHAR(255),
            note_summary      VARCHAR(255), 
            note_content      TEXT,
            date_created      TIMESTAMPTZ DEFAULT NOW(),
            last_modification TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY  (id),
            FOREIGN KEY  (category_id) REFERENCES categories(id),
            FOREIGN KEY  (user_id) REFERENCES users(id)
         )
      '''

      cursor, connection = self.connect()

      cursor.execute(query)

      self.disconnect(cursor, connection)

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