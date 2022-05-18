from flask import request, json, jsonify

from app.models.Note import Note
from app.models.Category import Category

class UseNotesController:
   def store(self, userId):

      requestData = json.loads(request.data)

      if not 'categoryId' in requestData:
         return jsonify({ 'state': 'error', 'reason': 'no category id' }, 401)

      note = Note()
      category = Category()

      category.id = requestData['categoryId']

      note.create(category.id, userId)
      category.updateLastModification(userId)

      return jsonify({ 
         'state': 'success', 
         'noteData': {
            'id': note.id,
            'dateCreated': note.dateCreated,
            'lastModification': note.lastModification
         } 
      }, 200)

   def destore(self, userId):

      requestData = json.loads(request.data)

      if not 'categoryId' in requestData or not 'noteId' in requestData:
         return jsonify({ 'state': 'error', 'reason': 'no note id or category id' }, 401)

      note = Note()
      category = Category()

      note.id = requestData['noteId']
      category.id = requestData['categoryId']

      note.delete(category.id, userId)
      category.updateLastModification(userId)

      return jsonify({ 'state': 'success' }, 200)

   def getStore(self, userId):

      requestData = json.loads(request.data)

      if not 'categoryId' in requestData:
         return jsonify({ 'state': 'error', 'reason': 'no category id' }, 401)

      note = Note()

      categoryId = requestData['categoryId']

      allNotes = note.findAll(categoryId, userId)

      def formatNotes(noteData):
         return { 
            'id': noteData[0],
            'categoryId': noteData[1],
            'title': noteData[2],
            'summary': noteData[3],
            'content': noteData[4],
            'dateCreated': noteData[5],
            'lastModification': noteData[6]
         }

      allNotesFormated = list(map(formatNotes, allNotes)) if allNotes else allNotes

      return jsonify({ 'state': 'success', 'notes': allNotesFormated }, 200)

   def updateStore(self, userId):

      requestData = json.loads(request.data)

      if not 'id' in requestData or not 'categoryId' in requestData:
         return jsonify({ 'state': 'error', 'reason': 'no note id or category id' }, 401)

      note = Note(requestData['title'], requestData['summary'], requestData['content'])
      category = Category()

      note.id = requestData['id']
      category.id = requestData['categoryId']

      hasSomeError = note.validateNoteUpdate()

      if hasSomeError:
         return jsonify({ 'state': 'error', 'reason': hasSomeError }, 401)

      note.update(category.id, userId)
      category.updateLastModification(userId)

      return jsonify({ 'state': 'success', 'lastModification': note.lastModification }, 200)


NotesController = UseNotesController()