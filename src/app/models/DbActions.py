class DbActions:
   def __init__(self, cursor):
      self.cursor = cursor

   def createTable(self, none):
      self.cursor.execute('''
         SET lc_time to 'pt_BR.UTF-8';
         SET TIMEZONE='America/Sao_Paulo';

         CREATE TABLE IF NOT EXISTS users(
            id          VARCHAR(5) NOT NULL,
            username    VARCHAR(255) NOT NULL,
            email       VARCHAR(255) NOT NULL,
            password    VARCHAR(255)  NOT NULL,
            apiKey      VARCHAR(21)  NOT NULL,
            datetime    TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (id)
         );

         CREATE TABLE IF NOT EXISTS categories(
            id          SERIAL NOT NULL,
            user_id     VARCHAR(5) NOT NULL,
            category_name    VARCHAR(255) NOT NULL,
            datetime    TIMESTAMPTZ DEFAULT NOW(),
            last_update TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES users(id)
         );
         
         CREATE TABLE IF NOT EXISTS notes(
            id           SERIAL NOT NULL,
            category_id  INTEGER NOT NULL,
            user_id      VARCHAR(5) NOT NULL,
            note_title   VARCHAR(255),
            note_summary VARCHAR(255), 
            note_content TEXT,
            date_created TIMESTAMPTZ DEFAULT NOW(),
            last_modification TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY  (id),
            FOREIGN KEY  (category_id) REFERENCES categories(id),
            FOREIGN KEY  (user_id) REFERENCES users(id)
         )
      ''')
   
   def insertUser(self, data):
      self.cursor.execute(
         "INSERT INTO users(id, username, email, password, apiKey) VALUES(%s,%s,%s,%s,%s)",
         (data['id'], data['username'], data['email'], data['password'], data['apiKey'])
      )

   def getOneUser(self, data):
      self.cursor.execute(
         f'''
            SELECT {data['item']} FROM users WHERE {data['condition']}
         ''',
         data['datas']
      )

      response = self.cursor.fetchone()

      return response

   def updateUser(self, data):
      self.cursor.execute(
         '''
            UPDATE users SET email = %s, username = %s WHERE id = %s
            RETURNING email, username
         ''',
         (data['email'], data['username'], data['id'])
      )

      response = self.cursor.fetchone()

      return response
   
   def deleteUser(self, data):
      self.cursor.execute(
      '''
         DELETE FROM notes WHERE user_id = %s;
         DELETE FROM categories WHERE user_id = %s;
         DELETE FROM users WHERE id = %s
      ''', 
         (data['userId'], data['userId'], data['userId'])
      )

      return 'deleted'

   def getUserWithSomeCredentials(self, data):
      self.cursor.execute(
         f'''SELECT * FROM users WHERE {data['condition1']}''',
         data['datas1']
      )

      response1 = self.cursor.fetchone()

      self.cursor.execute(
         f'''SELECT * FROM users WHERE {data['condition2']}''',
         data['datas2']
      )

      response2 = self.cursor.fetchone()

      return {"hasUserWithSomeEmail": response1, "hasUserWithSomeUsername": response2}

   def insertCategory(self, data):
      self.cursor.execute(
         "INSERT INTO categories(id ,user_id, category_name) VALUES(DEFAULT ,%s, %s) RETURNING id",
         (data['userId'], data['categoryName'])
      )

      categoryId = self.cursor.fetchone()

      return categoryId[0]

   def deleteCategory(self, data):
      self.cursor.execute(
         '''
            DELETE FROM notes WHERE category_id = %s AND user_id = %s;
            DELETE FROM categories WHERE id = %s AND user_id = %s
         ''',
         (data['categoryId'], data['userId'], data['categoryId'], data['userId'])
      )

   def updateCategory(self, data):
      self.cursor.execute(
         '''
            UPDATE categories SET category_name = %s , last_update = NOW()
            WHERE id = %s AND user_id = %s
         ''',
         (data['newCategoryName'], data['categoryId'], data['userId'])
      )

      self.setLastCategoryUpdate(data)

   def getCategories(self, data):
      self.cursor.execute(
         '''
            SELECT id, category_name FROM categories WHERE user_id = %s
            ORDER BY last_update DESC
         ''',
         (data['userId'], )
      )

      allCategories = self.cursor.fetchall()

      return allCategories

   def setLastCategoryUpdate(self, data):
      self.cursor.execute(
         '''
            UPDATE categories SET last_update = NOW()
            WHERE id = %s AND user_id = %s
         ''',
         (data['categoryId'], data['userId'])
      )

   def getNotes(self, data):
      self.cursor.execute(
         '''
            SET lc_time to 'pt_BR.UTF-8';
            SET TIMEZONE='America/Sao_Paulo';

            SELECT 
               id, category_id, note_title, note_summary, note_content,
               TO_CHAR(date_created, 'dd TMMonth yyyy às TMHH24:MI'),
               TO_CHAR(last_modification, 'dd/MM/yyyy às TMHH24:MI')
            FROM notes 
            WHERE category_id = %s AND user_id = %s
            ORDER BY last_modification DESC
         ''',
         (data['categoryId'], data['userId']) 
      )

      allNotes = self.cursor.fetchall()

      return allNotes

   def insertNote(self, data):
      self.cursor.execute(
         '''
            SET lc_time to 'pt_BR.UTF-8';
            SET TIMEZONE='America/Sao_Paulo';

            INSERT INTO notes(id, category_id, user_id, note_title, note_summary, note_content) 
            VALUES(DEFAULT, %s, %s, 'Nova Nota', 'O resumo da nova nota está aqui...', 'O conteúdo da nova nota está aqui...') 
            RETURNING id, 
               TO_CHAR(date_created, 'dd TMMonth yyyy às TMHH24:MI'),
               TO_CHAR(last_modification, 'dd/MM/yyyy às TMHH24:MI')
         ''',
         (data['categoryId'], data['userId'])
      )

      noteDatas = self.cursor.fetchone()

      self.setLastCategoryUpdate(data)

      return noteDatas

   def deleteNote(self, data):
      self.cursor.execute(
         'DELETE FROM notes WHERE id = %s AND category_Id = %s AND user_id = %s',
         (data['noteId'], data['categoryId'], data['userId'])
      )

      self.setLastCategoryUpdate(data)

   def updateNote(self, data):
      self.cursor.execute(
         '''
            SET lc_time to 'pt_BR.UTF-8';
            SET TIMEZONE='America/Sao_Paulo';

            UPDATE notes 
            SET note_title = %s, note_summary = %s, note_content = %s, last_modification = NOW()
            WHERE id = %s AND category_id = %s AND user_id = %s
            RETURNING TO_CHAR(last_modification, 'dd/MM/yyyy às TMHH24:MI')
         ''',
         (
            data['newTitle'], data['newSummary'], data['newContent'], 
            data['noteId'], data['categoryId'], data['userId']
         )
      )

      lastModification = self.cursor.fetchone()[0]

      self.setLastCategoryUpdate(data)

      return lastModification

# dividir as querys em classes (pesquisar sobre migrations)