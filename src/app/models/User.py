from database.Database import Database

from dotenv import load_dotenv
import os

from cryptocode import encrypt, decrypt

load_dotenv()
class User:

   def __init__(self, data):

      self.username = data['username'] if 'username' in data else None
      self.email = data['email'] if 'email' in data else None
      self.password = data['password'] if 'password' in data else None
      self.confirmPassword = data['confirmPassword'] if 'confirmPassword' in data else None
      self.keepConnected = data['keepConnected'] if 'keepConnected' in data else None

   def validateSignUp(self):

      errors = [*self.validateUsernameAndEmail()]

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

   def validateUsernameAndEmail(self):

      userExistsWithEmail = self.findOneUser('email = %s', self.email)
      userExistsWithUsername = self.findOneUser('username = %s', self.username)

      errors = []

      if self.email == '':
         errors.append({'input': 'inputEmail', 'reason': 'empty input'})

      elif userExistsWithEmail:
         errors.append({'input': 'inputEmail', 'reason': 'email already exists'})

      if self.username == '':
         errors.append({'input': 'inputUsername', 'reason': 'empty input'})

      elif userExistsWithUsername:
         errors.append({'input': 'inputUsername', 'reason': 'username already exists'})

      return errors

   def findOneUser(self, where, *value):

      query = f'''SELECT * FROM users WHERE {where}'''

      cursor, connection = Database.connect()

      cursor.execute(query, (*value, ))
      user = cursor.fetchone()

      Database.disconnect(cursor, connection)

      return user

   def create(self):

      self.hashPassword()

      query = '''
         INSERT INTO users(id, username, email, password) 
         VALUES(DEFAULT, %s, %s, %s) RETURNING id
      '''

      cursor, connection = Database.connect()

      cursor.execute(query,  (self.username, self.email, self.password))

      self.id = cursor.fetchone()[0]

      Database.disconnect(cursor, connection)

   # talvez tirar todos esses gets e usar o findOneUser
   def getId(self):

      id = self.findOneUser('email = %s OR username = %s', self.email, self.email)[0]

      return id

   def hashPassword(self):
      hashPassword = encrypt(self.password, os.environ.get('HASH_PASSWORD_KEY'))

      self.password = hashPassword

   def decryptHashPassword(self, currentPassword):
      decodePassword = decrypt(currentPassword, os.environ.get('HASH_PASSWORD_KEY'))

      return decodePassword