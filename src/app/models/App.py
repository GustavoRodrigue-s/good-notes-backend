class App:
   def __init__(self):
      self.name = "Good Notes"

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
   def checkNoteErros(noteData):

      if not noteData['title']:
         raise Exception('The title must not be null')