from models.db.connection import connectionDB

from datetime import datetime
import locale

class UseNotesController:
   @staticmethod
   def getNotesHandler(userId, categoryId):
      allNotes = connectionDB('getNotes', {
         'categoryId': categoryId,
         'userId': userId
      })

      def noteFormated(data):
         return { 
            'id': data[0],
            'categoryId': data[1],
            'title': data[2],
            'content': data[3],
            'dateOne': data[4],
            'dateTwo': data[5]
         }

      allNotesFormated = list(map(noteFormated, allNotes))

      return allNotesFormated

   @staticmethod
   def createNoteHandler(userId, categoryId):

      locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')

      dateOne = datetime.today().strftime('%d/%m/%Y às %H:%M')
      dateTwo = datetime.today().strftime('%d %B %Y às %H:%M')

      noteDatas = connectionDB('insertNote', {
         'categoryId': categoryId,
         'userId': userId,
         'dateOne': dateOne,
         'dateTwo': dateTwo
      })

      noteDataFormated = { 
         'id': noteDatas[0],
         'dateOne': noteDatas[1],
         'dateTwo': noteDatas[2] 
      }
      
      return noteDataFormated

   @staticmethod
   def deleteNoteHandler(noteId, categoryId, userId):
      connectionDB('deleteNote', {
         'noteId': noteId,
         'categoryId': categoryId,
         'userId': userId
      })

   @staticmethod
   def updateNoteHandler(userId, requestData):

      locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
      newUpdatedDate = datetime.today().strftime('%d/%m/%Y às %H:%M')

      connectionDB('updateNote', {
         'noteId': requestData['noteId'],
         'categoryId': requestData['categoryId'],
         'userId': userId,
         'newTitle': requestData['newTitle'],
         'newContent': requestData['newContent'],
         'newDateUpdated': newUpdatedDate
      })

      return newUpdatedDate