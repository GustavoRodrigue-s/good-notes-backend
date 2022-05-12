from database.connection import connectionDB 

def createCategoryHandler(userId, categoryName):

   categoryId = connectionDB('addCategory', {
      'userId': userId,
      'categoryName': categoryName or 'Nova Categoria'
   })

   return categoryId

def deleteCategoryHandler(userId, categoryId):
   
   connectionDB('deleteCategory', {
      'userId': userId,
      'categoryId': categoryId
   })

def updateCategoryHandler(userId, requestData):

   connectionDB('updateCategory', {
      'userId': userId,
      'categoryId': requestData['categoryId'],
      'newCategoryName': requestData['newCategoryName'] or 'Nova Categoria'
   })

def getCategoriesHandler(userId):

   allCurrentCategories = connectionDB('getCategories', { 'userId': userId })

   return allCurrentCategories