class App:
   def __init__(self):
      self.name = "Good Notes"
     

   @staticmethod
   def checkNoteErros(noteData):

      if not noteData['title']:
         raise Exception('The title must not be null')