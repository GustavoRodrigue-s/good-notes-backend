from flask import request, json, jsonify

from app.models.Category import Category

class UseCategoryController:
   def store(self, userId):
      try:

         requestData = json.loads(request.data)

         category = Category(requestData['categoryName'])

         category.create(userId)

         return jsonify({ 'state': 'success', 'categoryId': category.id }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def destore(self, userId):
      try:
         
         requestData = json.loads(request.data)

         category = Category()

         category.id = requestData['categoryId']

         category.delete(userId)

         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def updateStore(self, userId):
      try:

         requestData = json.loads(request.data)

         category = Category(requestData['newCategoryName'])

         category.id = requestData['categoryId']

         category.update(userId)
            
         return jsonify({ 'state': 'success' }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

   def getStore(self, userId):
      try:

         category = Category()

         allCategories = category.findAll(userId)

         return jsonify({ 'state': 'success', 'categories': allCategories }, 200)

      except Exception as e:
         return jsonify({ "state": "error", 'reason': f'{e}' }, 401)

CategoryController = UseCategoryController()
