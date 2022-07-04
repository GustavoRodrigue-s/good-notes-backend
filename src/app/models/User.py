from database.Database import Database

import os, sys

from cryptocode import encrypt, decrypt

sys.path.insert(1, './')

from dotenv import load_dotenv

from services.PhotoService import PhotoService

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

      errors = []

      errors.extend(self.validateEmail(userEmailExists))
      errors.extend(self.validateUsername(userUsernameExists))

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

   def validateUsername(self, userExists):

      errors = []

      if self.username == '':
         errors.append({'input': 'inputUsername', 'reason': 'empty input'})

      elif userExists:
         errors.append({'input': 'inputUsername', 'reason': 'username already exists'})

      return errors

   def validateEmail(self, userExists):

      errors = []

      if self.email == '':
         errors.append({'input': 'inputEmail', 'reason': 'empty input'})

      elif userExists:
         errors.append({'input': 'inputEmail', 'reason': 'email already exists'})

      return errors

   def validatePhotoUpload(self, photoData):

      if not photoData['type'] in ALLOWED_EXTENSIONS:
         raise Exception('image type not allowed')

      if photoData['size'] > MAXIMUM_PHOTO_SIZE:
         raise Exception('maximum photo size')

   def validatePassword(self, newPassword):

      userExists = self.findOne('id = %s', self.id)
      decodedPassword = self.decryptHashPassword(userExists[3])

      errors = []

      if self.password == '':
         errors.append({ 'input': 'inputOldPassword', 'reason': 'empty input' })

      elif self.password != decodedPassword:
         errors.append({ 'input': 'inputOldPassword', 'reason': 'wrong old password' })

      if newPassword == '':
         errors.append({ 'input': 'inputNewPassword', 'reason': 'empty input' })

      if not userExists:
         errors.append({ 'reason': 'user with id not found' })

      return errors

   def validateEmailConfirmationCode(self, code, user = None):

      userExists = user or self.findOne('id = %s', self.id)

      if not userExists:
         raise Exception('user not found')

      if len(code) < 5:
         raise Exception('code incomplete')

      if code != userExists[7]:
         raise Exception('invalid code')

   def validateForgotPassword(self, userExists):

      errors = []

      if self.password == '':
         errors.append({ 'input': 'inputPassword', 'reason': 'empty input' })

      if self.email == '':
         errors.append({ 'input': 'inputEmail', 'reason': 'empty input' })

      elif not userExists:
         errors.append({ 'input': 'inputEmail', 'reason': 'user not exists' })

      return errors

   def findOne(self, where, *value):

      query = f'''SELECT * FROM users WHERE {where}'''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (*value, ))
         user = cursor.fetchone()

      finally:
         Database.disconnect(cursor, connection)

      return user

   def create(self, code):

      self.hashPassword()

      query = '''
         INSERT INTO users(id, username, email, password, verification_code, active) 
         VALUES(DEFAULT, %s, %s, %s, %s, FALSE) RETURNING id
      '''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query,  (self.username, self.email, self.password, code))

         self.id = cursor.fetchone()[0]

      finally:
         Database.disconnect(cursor, connection)

   def delete(self):

      photoId = self.findOne('id = %s', self.id)[5]

      if photoId:
         PhotoService.delete(photoId)

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

   def update(self, set, where, *value):

      query = f'''UPDATE users SET {set} WHERE {where}'''

      cursor, connection = Database.connect()

      try:
         cursor.execute(query, (*value, ))

      finally:
         Database.disconnect(cursor, connection)

   def uploadPhoto(self, photoUrl):
      
      existingPhotoId = self.findOne('id = %s', self.id)[5]

      url, id = PhotoService.update(photoUrl, existingPhotoId) if existingPhotoId else PhotoService.create(photoUrl)

      self.update('photo_url = %s, photo_id = %s', 'id = %s', url, id, self.id)

      return url

   def hashPassword(self):
      hashPassword = encrypt(self.password, os.environ.get('HASH_PASSWORD_KEY'))

      self.password = hashPassword

   def decryptHashPassword(self, currentPassword):
      decodePassword = decrypt(currentPassword, os.environ.get('HASH_PASSWORD_KEY'))

      return decodePassword