class App:
   def __init__(self):
      self.name = "Good Notes"

   @staticmethod
   def checkRegistrationErrors(user, usersDatabase):
      wrongInputs = []

      inputsArray = [
         { 'name': 'inputUsername', "value": user.username },
         { 'name': 'inputEmail', "value": user.email },
         { 'name': 'inputsPasswords', "value": user.password[0] },
         { 'name': 'inputsPasswords', "value": user.password[1] }
      ]

      for input in inputsArray:
         if input["value"] == '':
            reason = 'empty inputs' if input['name'] == 'inputsPasswords' else 'empty input'

            wrongInputs.append({'input': input['name'], "reason": reason})

      if usersDatabase['hasUserWithSomeUsername']: 
         wrongInputs.append({'input': 'inputUsername', "reason": "username already exists"})

      if usersDatabase['hasUserWithSomeEmail']:
         wrongInputs.append({'input': 'inputEmail', "reason": "email already exists"})

      if user.password[0] and user.password[1] and user.password[0] != user.password[1]:
         wrongInputs.append({'input': 'inputsPasswords', "reason": "differents passwords"})
         
      if wrongInputs != []: 
         return wrongInputs

   @staticmethod
   def checkLoginErrors(user, userDatabase):

      wrongInputs = []

      inputsArray = [
         { 'name': 'inputEmail', "value": user.email },
         { 'name': 'inputPassword', "value": user.password }
      ]

      for input in inputsArray:
         if input["value"] == '':
            wrongInputs.append({'input': input['name'], "reason": "empty input"})

      if user.email and user.password:
         if not userDatabase or userDatabase[3] != user.password:
            wrongInputs.append({'input': 'some', "reason": "wrong credentials"})


      if wrongInputs != []: raise Exception(wrongInputs)

   @staticmethod
   def checkProfileErrors(user, hasUserWithSomeCredentials):

      wrongValues = []

      if user['email'] == '':
         wrongValues.append({'input': 'inputEmail', 'reason': 'empty input'})

      if user['username'] == '':
         wrongValues.append({'input': 'inputUsername', 'reason': 'empty input'})

      if hasUserWithSomeCredentials['hasUserWithSomeEmail']:
         wrongValues.append({'input': 'inputEmail', 'reason': 'email already exists'})

      if hasUserWithSomeCredentials['hasUserWithSomeUsername']:
         wrongValues.append({'input': 'inputUsername', 'reason': 'username already exists'})


      if wrongValues != []: raise Exception(wrongValues)

   @staticmethod
   def checkNoteErros(noteData):

      if not noteData['title']:
         raise Exception('The title must not be null')