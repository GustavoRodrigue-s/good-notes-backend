from database.Database import Database
from random import sample

from dotenv import load_dotenv
import os

from cryptocode import encrypt, decrypt

load_dotenv()
class User:

   def __init__(self, username = None, email = None, password = None, confirmPassword = None):

      self.username = username
      self.email = email
      self.password = password
      self.confirmPassword = confirmPassword

   def validateUserCreation(self):

      errors = [*self.validateUsernameAndEmail()]

      if self.password == '' or self.confirmPassword == '':
         errors.append({'input': 'inputsPasswords', "reason": 'empty inputs'})

      elif self.password != self.confirmPassword:
         errors.append({'input': 'inputsPasswords', "reason": "differents passwords"})
         
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

   def findOneUser(self, condition, value):

      query = f'''SELECT * FROM users WHERE {condition}''', (value, )

      cursor, connection = Database.connect()

      cursor.execute(query)
      user = cursor.fetchone()

      Database.disconnect(cursor, connection)

      return user

   def create(self):

      self.createId()
      self.createApiKey()
      self.hashPassword()

      query = '''
         INSERT INTO users(id, username, email, password, apiKey) VALUES(%s, %s, %s, %s ,%s)
      ''',
      (self.id, self.username, self.email, self.password, self.apiKey)

      cursor, connection = Database.connect()

      cursor.execute(query)

      Database.disconnect(cursor, connection)

   def createId(self):
      letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

      while True:
         randomId = ''.join(sample(letters, 5))

         user = self.findOneUser('id = %s', randomId)

         if user == None:
            break                

      self.id = randomId

   def getCurrentUserId(self, currentUser):
      currentId = connectionDB('getOneUser', {
         'item': 'id',
         'condition': "email = %s OR username = %s",
         'datas': (currentUser.email, currentUser.email)
      })[0]

      return currentId

   def getApiKeyHandler(self, currentUserId):
      
      apiKey = connectionDB('getOneUser', {
         'item': 'apiKey',
         'condition': "id = %s",
         'datas': (currentUserId,)
      })[0]

      return apiKey

   def createApiKey(self):
      letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

      randomKey = ''.join(sample(letters, 15))

      apiKey = randomKey + "-" + self.id

      self.apiKey = apiKey

   def hashPassword(self):
      hashPassword = encrypt(self.password, os.environ.get('HASH_PASSWORD_KEY'))

      self.password = hashPassword

   def decryptHashPassword(self, currentHashPassword):
      decodePassword = decrypt(currentHashPassword, os.environ.get('HASH_PASSWORD_KEY'))

      return decodePassword