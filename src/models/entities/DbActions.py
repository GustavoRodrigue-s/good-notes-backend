class DbActions:
   def __init__(self, cursor):
      self.cursor = cursor

   def createTable(self, none):
      self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS users(
         id          VARCHAR(5) NOT NULL,
         username    VARCHAR(255) NOT NULL,
         email       VARCHAR(255) NOT NULL,
         password    VARCHAR(255)  NOT NULL,
         apiKey      VARCHAR(21)  NOT NULL,
         date        VARCHAR(19),
         PRIMARY KEY (id)
      );

      CREATE TABLE IF NOT EXISTS categories(
         id          SERIAL NOT NULL,
         user_id     VARCHAR(5) NOT NULL,
         category_name    VARCHAR(255) NOT NULL,
         PRIMARY KEY (id),
         FOREIGN KEY (user_id) REFERENCES users(id)
      );
      
      CREATE TABLE IF NOT EXISTS notes(
         id           SERIAL NOT NULL,
         category_id  INTEGER NOT NULL,
         user_id      VARCHAR(5) NOT NULL,
         note_title   VARCHAR(255),
         note_content TEXT,
         date_one     VARCHAR(40) NOT NULL,
         date_two     VARCHAR(40) NOT NULL,
         PRIMARY KEY  (id),
         FOREIGN KEY  (category_id) REFERENCES categories(id),
         FOREIGN KEY  (user_id) REFERENCES users(id)
      )''')
   
   def insertUser(self, data):
      self.cursor.execute(
         "INSERT INTO users(id, username, email, password, apiKey, date) VALUES(%s,%s,%s,%s,%s,%s)",
         (data['id'], data['username'], data['email'], data['password'], data['apiKey'], data['currentDate'])
      )

   def getOneUser(self, data):
      self.cursor.execute(
         f'''SELECT {data['item']} FROM users WHERE {data['condition']}''',
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
      self.cursor.execute('''DELETE FROM users WHERE id = %s''', data['datas'])

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
         'DELETE FROM categories WHERE id = %s AND user_id = %s',
         (data['categoryId'], data['userId'])
      )

   def updateCategory(self, data):
      self.cursor.execute(
         'UPDATE categories SET category_name = %s WHERE id = %s AND user_id = %s',
         (data['newCategoryName'], data['categoryId'], data['userId'])
      )

   def getCategories(self, data):
      self.cursor.execute(
         'SELECT id, category_name FROM categories WHERE user_id = %s',
         (data['userId'], )
      )

      allCategories = self.cursor.fetchall()

      return allCategories

   def getNotes(self, data):
      self.cursor.execute(
         '''
            SELECT id, category_id, note_title, note_content, date_one, date_two 
            FROM notes 
            WHERE category_id = %s AND user_id = %s
            ORDER BY date_one DESC
         ''',
         (data['categoryId'], data['userId']) 
      )

      allNotes = self.cursor.fetchall()

      return allNotes

   def insertNote(self, data):
      self.cursor.execute(
         '''
         INSERT INTO notes(id, category_id, user_id, note_title, note_content, date_one, date_two) 
         VALUES(DEFAULT, %s, %s, 'Nova Nota', 'O conteúdo da nova nota está aqui...', %s, %s) 
         RETURNING id, date_one, date_two''',
         (data['categoryId'], data['userId'], data['dateOne'], data['dateTwo'])
      )

      noteDatas = self.cursor.fetchone()

      return noteDatas

   def deleteCategory(self, data):
      self.cursor.execute(
         'DELETE FROM notes WHERE id = %s AND category_Id = %s AND user_id = %s',
         (data['noteId'], data['categoryId'], data['userId'])
      )

   def updateNote(self, data):
      self.cursor.execute(
         '''
            UPDATE notes SET note_title = %s, note_content = %s, date_one = %s
            WHERE id = %s AND category_id = %s AND user_id = %s
         ''',
         (
            data['newTitle'], data['newContent'], data['newDateUpdated'], 
            data['noteId'], data['categoryId'], data['userId']
         )
      )