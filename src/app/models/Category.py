
from database.Database import Database 

class Category:

   def __init__(self, categoryName = None):

      self.name = categoryName or 'Nova Categoria'

   def findAll(self, userId):

      query = '''
         SELECT id, category_name FROM categories WHERE user_id = %s
         ORDER BY last_update DESC
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (userId, ))

         items = cursor.fetchall()

      finally:
         Database.disconnect(cursor, connection)

      return items

   def create(self, userId):

      query = '''
         INSERT INTO categories(id ,user_id, category_name) VALUES(DEFAULT ,%s, %s) 
         RETURNING id
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (userId, self.name))

         self.id = cursor.fetchone()

      finally:
         Database.disconnect(cursor, connection)

   def delete(self, userId):

      query = '''
         DELETE FROM notes WHERE category_id = %s AND user_id = %s;
         DELETE FROM categories WHERE id = %s AND user_id = %s
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.id, userId, self.id, userId))

      finally:
         Database.disconnect(cursor, connection)

   def update(self, userId):
      
      query = '''
         UPDATE categories SET category_name = %s, last_update = NOW()
         WHERE id = %s AND user_id = %s
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.name, self.id, userId))

      finally:
         Database.disconnect(cursor, connection)

   def updateLastModification(self, userId):

      query = '''
         UPDATE categories SET last_update = NOW()
         WHERE id = %s AND user_id = %s
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.id, userId))

      finally:
         Database.disconnect(cursor, connection)