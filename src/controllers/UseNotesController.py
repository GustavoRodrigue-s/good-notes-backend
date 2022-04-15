from models.db.connection import connectionDB

class UseNotesController:
   @staticmethod
   def getNotesHandler(userId, categoryId):
      allNotes = connectionDB('getNotes', {
         'categoryId': categoryId,
         'userId': userId
      })

      return allNotes

   @staticmethod
   def createNoteHandler(userId, categoryId):
      noteId = connectionDB('insertNote', {
         'categoryId': categoryId,
         'userId': userId
      })
      
      return noteId