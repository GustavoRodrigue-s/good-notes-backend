from flask import jsonify

import sys

sys.path.insert(1, './src')

from app.controllers.AuthController import AuthController
from app.controllers.UserController import UserController
from app.controllers.CategoryController import CategoryController
from app.controllers.NotesController import NotesController

from app.middlewares.authMiddleware import authMiddleware

def createRoutes(app):
   @app.route('/login', methods=['POST'])
   def routeLogin():
      return AuthController.authenticate()

   @app.route('/register', methods=['POST'])
   def routeRegister():
      return UserController.store()

   @app.route('/logout', methods=['GET'])
   @authMiddleware
   def routeLogoutUser(userId):
      return AuthController.exitAuthentication(userId)

   @app.route('/auth', methods=['GET'])
   @authMiddleware
   def routeTokenRequired(userId):
      return UserController.getStore(userId)

   @app.route('/getProfile', methods=['GET'])
   @authMiddleware
   def routeGetData(userId):
      return UserController.getStore(userId)

   @app.route('/updateCredentials', methods=['PUT'])
   @authMiddleware
   def routeUpdateCredentials(userId):
      return UserController.updateStore(userId)

   @app.route('/updatePassword', methods=['PUT'])
   @authMiddleware
   def routeUpdatePassword(userId):
      return UserController.updatePassword(userId)

   @app.route('/uploadPhoto', methods=['POST'])
   @authMiddleware
   def routeUpload(userId):
      return UserController.uploadPhoto(userId)

   @app.route('/deleteAccount', methods=['DELETE'])
   @authMiddleware
   def routeDeleteAccount(userId):
      return UserController.destore(userId)

   # ----- Endpoints Categorys ------

   @app.route('/addCategory', methods=['POST'])
   @authMiddleware
   def routeAddCategory(userId):
      return CategoryController.store(userId)

   @app.route('/deleteCategory', methods=['DELETE'])
   @authMiddleware
   def routeDeleteCategory(userId):
      return CategoryController.destore(userId)

   @app.route('/updateCategory', methods=['PUT'])
   @authMiddleware
   def routeUpdateCategory(userId):
      return CategoryController.updateStore(userId)

   @app.route('/getCategories', methods=['GET'])
   @authMiddleware
   def routeGetCategories(userId):
      return CategoryController.getStore(userId)
      
   # # ----- Endpoints Notes ------

   @app.route('/getNotes', methods=['GET'])
   @authMiddleware
   def routeGetNotes(userId):
      return NotesController.getStore(userId)

   @app.route('/addNote', methods=['POST'])
   @authMiddleware
   def routeAddNote(userId):
      return NotesController.store(userId)

   @app.route('/deleteNote', methods=['DELETE'])
   @authMiddleware
   def routeDeleteNote(userId):
      return NotesController.destore(userId)

   @app.route('/updateNote', methods=['PUT'])
   @authMiddleware
   def routeUpdateNote(userId):
      return NotesController.updateStore(userId)