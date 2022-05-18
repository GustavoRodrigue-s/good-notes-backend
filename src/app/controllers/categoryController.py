from flask import request, json, jsonify

from app.models.Category import Category

class UseCategoryController:
   def store(self, userId):

      requestData = json.loads(request.data)

      category = Category(requestData['categoryName'])

      category.create(userId)

      return jsonify({ 'state': 'success', 'categoryId': category.id }, 200)

   def destore(self, userId):

      requestData = json.loads(request.data)

      if not 'categoryId' in requestData:
         return jsonify({ 'state': 'error', 'reason': 'no category id' }, 401)

      category = Category()

      category.id = requestData['categoryId']

      category.delete(userId)

      return jsonify({ 'state': 'success' }, 200)

   def updateStore(self, userId):

      requestData = json.loads(request.data)
      
      if not 'categoryId' in requestData:
         return jsonify({ 'state': 'error', 'reason': 'no category id' }, 401)

      category = Category(requestData['newCategoryName'])

      category.id = requestData['categoryId']

      category.update(userId)
         
      return jsonify({ 'state': 'success' }, 200)

   def getStore(self, userId):

      category = Category()

      allCategories = category.findAll(userId)

      return jsonify({ 'state': 'success', 'categories': allCategories }, 200)

CategoryController = UseCategoryController()