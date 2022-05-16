from database.Database import connectionDB 

class UseCategoryController:
   def store(self, userId, categoryName):
      categoryId = connectionDB('addCategory', {
         'userId': userId,
         'categoryName': categoryName or 'Nova Categoria'
      })

      return categoryId

   def destore(self, userId, categoryId):

      connectionDB('deleteCategory', {
         'userId': userId,
         'categoryId': categoryId
      })

   def updateStore(self, userId, requestData):

      connectionDB('updateCategory', {
         'userId': userId,
         'categoryId': requestData['categoryId'],
         'newCategoryName': requestData['newCategoryName'] or 'Nova Categoria'
      })

   def getStore(self, userId):

      allCurrentCategories = connectionDB('getCategories', { 'userId': userId })

      return allCurrentCategories


CategoryController = UseCategoryController()