from flask import request, json, jsonify

import sys
from app.controllers.AuthController import AuthController

sys.path.insert(1, './src')

from app.controllers.AuthController import AuthController
from app.controllers.UserController import UserController
from app.controllers.categoryController import CategoryController
from app.controllers.NotesController import NotesController

from app.middlewares.authMiddleware import authMiddleware

# separar de acordo com os controllers
def createRoutes(app):
   @app.route('/login', methods=['POST'])
   def routeLogin():
      return AuthController.authenticate()

   @app.route('/register', methods=['POST'])
   def routeRegister():
      return UserController.store()

   @app.route('/auth', methods=['GET'])
   @authMiddleware
   def routeTokenRequired(userId):
      return jsonify({ "state": "authorized" }, 200)

   @app.route('/logout', methods=['GET'])
   @authMiddleware
   def routeLogoutUser(userId):
      return AuthController.exitAuthentication(userId)

   @app.route('/getCredentials', methods=['GET'])
   @authMiddleware
   def routeGetData(userId):
      return UserController.getStore(userId)

   @app.route('/updateCredentials', methods=['POST'])
   @authMiddleware
   def routeUpdateCredentials(userId):
      return UserController.updateStore(userId)

   @app.route('/deleteAccount', methods=['DELETE'])
   @authMiddleware
   def routeDeleteAccount(userId):
      return UserController.destore(userId)

   # ----- Endpoints Categorys ------

   @app.route('/addCategory', methods=['POST'])
   @authMiddleware
   def routeAddCategory(userId):
      return CategoryController.store(userId)

   @app.route('/deleteCategory', methods=['POST'])
   @authMiddleware
   def routeDeleteCategory(userId):
      return CategoryController.destore(userId)

   @app.route('/updateCategory', methods=['POST'])
   @authMiddleware
   def routeUpdateCategory(userId):
      return CategoryController.updateStore(userId)

   @app.route('/getCategories', methods=['GET'])
   @authMiddleware
   def routeGetCategories(userId):
      return CategoryController.getStore(userId)
      
   # # ----- Endpoints Notes ------

   @app.route('/getNotes', methods=['POST'])
   @authMiddleware
   def routeGetNotes(userId):
      return NotesController.getStore(userId)

   @app.route('/addNote', methods=['POST'])
   @authMiddleware
   def routeAddNote(userId):
      return NotesController.store(userId)

   @app.route('/deleteNote', methods=['POST'])
   @authMiddleware
   def routeDeleteNote(userId):
      return NotesController.destore(userId)

   @app.route('/updateNote', methods=['POST'])
   @authMiddleware
   def routeUpdateNote(userId):
      return NotesController.updateStore(userId)