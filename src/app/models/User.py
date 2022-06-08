from database.Database import Database

import os

from cryptocode import encrypt, decrypt

from dotenv import load_dotenv

from src.services.PhotoUploader import PhotoUploader

load_dotenv()

MAXIMUM_PHOTO_SIZE = 1 * 1024 * 1024 # 1MB
ALLOWED_EXTENSIONS = ['image/png', 'image/jpg', 'image/jpeg']

class User:

   def __init__(self, data):

      self.username = data['username'] if 'username' in data else None
      self.email = data['email'] if 'email' in data else None
      self.password = data['password'] if 'password' in data else None
      self.confirmPassword = data['confirmPassword'] if 'confirmPassword' in data else None
      self.keepConnected = data['keepConnected'] if 'keepConnected' in data else None

   def validateSignUp(self):

      userEmailExists = self.findOne('email = %s', self.email)
      userUsernameExists = self.findOne('username = %s', self.username)

      errors = [
         *self.validateUsernameAndEmail(userEmailExists, userUsernameExists)
      ]

      if self.password == '' or self.confirmPassword == '':
         errors.append({'input': 'inputsPasswords', "reason": 'empty inputs'})

      elif self.password != self.confirmPassword:
         errors.append({'input': 'inputsPasswords', "reason": "differents passwords"})
         
      return errors

   def validateSignIn(self, userExists):

      errors = []

      if self.email == '':
         errors.append({'input': 'inputEmail', "reason": "empty input"})

      if self.password == '':
         errors.append({'input': 'inputPassword', "reason": "empty input"})

      if not self.email or not self.password:
         return errors

      if not userExists:
         errors.append({ "reason": "wrong credentials" })

         return errors

      userExistsPassword = self.decryptHashPassword(userExists[3])

      if userExistsPassword != self.password:
         errors.append({ "reason": "wrong credentials" })

      return errors

   def validateUsernameAndEmail(self, userEmailExists, userUsernameExists):
      
      errors = []

      if self.email == '':
         errors.append({'input': 'inputEmail', 'reason': 'empty input'})

      elif userEmailExists:
         errors.append({'input': 'inputEmail', 'reason': 'email already exists'})

      if self.username == '':
         errors.append({'input': 'inputUsername', 'reason': 'empty input'})

      elif userUsernameExists:
         errors.append({'input': 'inputUsername', 'reason': 'username already exists'})

      return errors

   def validatePhotoUpload(self, photoData):

      if not photoData['type'] in ALLOWED_EXTENSIONS:
         raise Exception('image type not allowed')

      if photoData['size'] > MAXIMUM_PHOTO_SIZE:
         raise Exception('maximum photo size')

   def findOne(self, where, *value):

      query = f'''SELECT * FROM users WHERE {where}'''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (*value, ))
         user = cursor.fetchone()

      finally:
         Database.disconnect(cursor, connection)

      return user

   def create(self):

      self.hashPassword()

      query = '''
         INSERT INTO users(id, username, email, password) 
         VALUES(DEFAULT, %s, %s, %s) RETURNING id
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query,  (self.username, self.email, self.password))

         self.id = cursor.fetchone()[0]

      finally:
         Database.disconnect(cursor, connection)

   def delete(self):

      photoId = self.findOne('id = %s', self.id)[4]

      if photoId:
         PhotoUploader.delete(photoId)

      query = '''
         DELETE FROM notes WHERE user_id = %s;
         DELETE FROM categories WHERE user_id = %s;
         DELETE FROM users WHERE id = %s
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.id, self.id, self.id))

      finally:
         Database.disconnect(cursor, connection)

   def uploadPhoto(self, photoUrl, photoId):
      
      urlOfTheUploadedPhoto = PhotoUploader.create(photoUrl, photoId)

      query = '''UPDATE users SET photo = %s WHERE id = %s'''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (photoId, self.id))

      finally:
         Database.disconnect(cursor, connection)

      return urlOfTheUploadedPhoto

   def updateUsernameAndEmail(self):

      query = 'UPDATE users SET email = %s, username = %s WHERE id = %s'

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (self.email, self.username, self.id))

      finally:
         Database.disconnect(cursor, connection)

   def hashPassword(self):
      hashPassword = encrypt(self.password, os.environ.get('HASH_PASSWORD_KEY'))

      self.password = hashPassword

   def decryptHashPassword(self, currentPassword):
      decodePassword = decrypt(currentPassword, os.environ.get('HASH_PASSWORD_KEY'))

      return decodePassword