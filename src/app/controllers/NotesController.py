from database.connection import connectionDB
from app.models.App import App 

class UseNotesController:
   def getStore(self, userId, categoryId):

      allNotes = connectionDB('getNotes', {
         'categoryId': categoryId,
         'userId': userId
      })

      def noteFormated(data):
         return { 
            'id': data[0],
            'categoryId': data[1],
            'title': data[2],
            'summary': data[3],
            'content': data[4],
            'dateCreated': data[5],
            'lastModification': data[6]
         }

      allNotesFormated = list(map(noteFormated, allNotes))

      return allNotesFormated

   def store(self, userId, categoryId):

      noteDatas = connectionDB('insertNote', {
         'categoryId': categoryId,
         'userId': userId,
      })

      noteDataFormated = { 
         'id': noteDatas[0],
         'dateCreated': noteDatas[1],
         'lastModification': noteDatas[2] 
      }
      
      return noteDataFormated

   def destore(self, noteId, categoryId, userId):

      connectionDB('deleteNote', {
         'noteId': noteId,
         'categoryId': categoryId,
         'userId': userId
      })

   def updateStore(self, userId, requestData):

      App.checkNoteErros(requestData)

      newLastModification = connectionDB('updateNote', {
         'noteId': requestData['id'],
         'categoryId': requestData['categoryId'],
         'userId': userId,
         'newTitle': requestData['title'],
         'newContent': requestData['content'],
         'newSummary': requestData['summary'],
      })

      return newLastModification


NotesController = UseNotesController()