from database.Database import Database

class Note:
   
   def __init__(self, title = None, summary = None, content = None):

      self.title = title
      self.summary = summary
      self.content = content

   def validateNoteUpdate(self):

      if self.title == '':
         return 'note title cannot be empty'

   def findAll(self, categoryId, userId):
      
      query = '''
         SET lc_time to 'pt_BR.UTF-8';
         SET TIMEZONE='America/Sao_Paulo';

         SELECT 
            id, category_id, note_title, note_summary, note_content,
            TO_CHAR(date_created, 'dd TMMonth yyyy às TMHH24:MI'),
            TO_CHAR(last_modification, 'dd/MM/yyyy às TMHH24:MI')
         FROM notes 
         WHERE category_id = %s AND user_id = %s
         ORDER BY last_modification DESC
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (categoryId, userId))

         items = cursor.fetchall()

      finally:
         Database.disconnect(cursor, connection)

      return items

   def create(self, categoryId, userId):
      
      summary = 'O resumo da nova nota está aqui...'
      content = 'O conteúdo da nova nota está aqui...'

      query = '''
         SET lc_time to 'pt_BR.UTF-8';
         SET TIMEZONE='America/Sao_Paulo';

         INSERT INTO notes(id, category_id, user_id, note_title, note_summary, note_content) 
         VALUES(DEFAULT, %s, %s, 'Nova Nota', %s, %s) 
         RETURNING id, 
            TO_CHAR(date_created, 'dd TMMonth yyyy às TMHH24:MI'),
            TO_CHAR(last_modification, 'dd/MM/yyyy às TMHH24:MI')
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (categoryId, userId, summary, content))

         id, dateCreated, lastModification = cursor.fetchone()

      finally:
         Database.disconnect(cursor, connection)

      self.id = id
      self.dateCreated = dateCreated
      self.lastModification = lastModification

   def delete(self, categoryId, userId):

      query = 'DELETE FROM notes WHERE id = %s AND category_Id = %s AND user_id = %s'

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.id, categoryId, userId))

      finally:
         Database.disconnect(cursor, connection)

   def update(self, categoryId, userId):

      query = '''
         SET lc_time to 'pt_BR.UTF-8';
         SET TIMEZONE='America/Sao_Paulo';

         UPDATE notes 
         SET note_title = %s, note_summary = %s, note_content = %s, last_modification = NOW()
         WHERE id = %s AND category_id = %s AND user_id = %s
         RETURNING TO_CHAR(last_modification, 'dd/MM/yyyy às TMHH24:MI')
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.title, self.summary, self.content, self.id, categoryId, userId))

         self.lastModification = cursor.fetchone()[0]

      finally:
         Database.disconnect(cursor, connection)