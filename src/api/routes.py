from flask import Flask, request, json, jsonify
from flask_cors import CORS
import os, sys

sys.dont_write_bytecode = True

sys.path.insert(1, './src')

from models.db.connection import connectionDB

from controllers import sessionController
from controllers import formsController
from controllers import categoryController
from controllers.UseNotesController import UseNotesController

from decorators import jwt_required, apiKey_required


# API config 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# If not exists, create new table
connectionDB('createTable', None)

#Routes
@app.route('/login', methods=['POST'])
def routeLogin():
   requestData = json.loads(request.data)

   try:
      formsController.loginFormHandler(requestData)

      sessionData = sessionController.createSessionHandler(requestData)

      return jsonify(
         {
            "state": "success",
            "reason": "all right",
            'apiKey': sessionData[1],
            "userData": sessionData[0]
         }, 200
      )
   except Exception as e:
      respData = [e.args[0]] if type(e.args[0]) != list else e.args[0]

      return jsonify({"errors": respData, "state": "error"}, 401)


@app.route('/register', methods=['POST'])
def routeRegister():
   requestData = json.loads(request.data)

   try:
      formsController.registerFormHandler(requestData)

      sessionData = sessionController.createSessionHandler(requestData)

      return jsonify(
         {
            "state": "success",
            "reason": "all right",
            "apiKey": sessionData[1],
            "userData": sessionData[0]
         }, 200
      )
   except Exception as e:
      respData = [e.args[0]] if type(e.args[0]) != list else e.args[0]

      return jsonify({"errors": respData, "state": "error"}, 401)


@app.route('/userCredentials', methods=['GET'])
@apiKey_required
@jwt_required
def routeGetData(userId):
   try:
      userCredentials = sessionController.getSessionCredentialsHandler(userId)

      return jsonify(
         { 'state': 'success' ,'username': userCredentials[1], 'email': userCredentials[2] }, 200
      )
   except:
      return jsonify({ "state": "unauthorized" }, 401)


@app.route('/auth', methods=['GET'])
@apiKey_required
@jwt_required
def routeTokenRequired(userId):

   return jsonify({ "state": "authorized" }, 200)


@app.route('/logout', methods=['GET'])
@apiKey_required
@jwt_required
def routeLogoutUser(userId):
   sessionController.disableSessionHandler(userId)

   return jsonify({ 'state': 'success' }, 200)


@app.route('/updateUser', methods=['POST'])
@apiKey_required
@jwt_required
def routeUpdateCredentials(userId):

   requestData = json.loads(request.data)

   try: 
      response = sessionController.updateSessionCredentialsHandler(userId, requestData)

      return jsonify({
         'state': 'success',
         'newDatas': response
      }, 200)

   except Exception as e:
      respData = [e.args[0]] if type(e.args[0]) != list else e.args[0]

      return jsonify({'state': 'error', 'reason': respData}, 403)


@app.route('/deleteUser', methods=['GET'])
@apiKey_required
def routeDeleteAccount(userId):
   try:
      sessionController.deleteSessionHandler(userId)

      return jsonify({'state': 'success'}, 200)
   except Exception as e:
      return jsonify({'state': 'error', 'reason': f'{e}'}, 401)

# ----- Endpoints Categorys ------

@app.route('/addCategory', methods=['POST'])
@apiKey_required
@jwt_required
def routeAddCategory(userId):
   requestData = json.loads(request.data)

   try:
      categoryName = requestData['categoryName']

      categoryId = categoryController.createCategoryHandler(userId, categoryName)

      return jsonify({'state': 'success', 'categoryId': categoryId}, 200)
   except Exception as e:
      return jsonify({'state': 'error', 'reason': 'no category name'}, 401)


@app.route('/deleteCategory', methods=['POST'])
@apiKey_required
@jwt_required
def routeDeleteCategory(userId):
   requestData = json.loads(request.data)

   try:
      categoryId = requestData['categoryId']

      categoryController.deleteCategoryHandler(userId, categoryId)

      return jsonify({'state': 'success'}, 200)
   except Exception as e:
      return jsonify({'state': 'error', 'reason': 'no category id'}, 401)


@app.route('/updateCategory', methods=['POST'])
@apiKey_required
@jwt_required
def routeUpdateCategory(userId):
   requestData = json.loads(request.data)

   try:
      categoryController.updateCategoryHandler(userId, requestData)

      return jsonify({'state': 'success'}, 200)
   except Exception as e:
      return jsonify({'state': 'error', 'reason': 'no category id or new category name'}, 401)


@app.route('/getCategories', methods=['GET'])
@apiKey_required
@jwt_required
def routeGetCategories(userId):
   try:
      allCategories =  categoryController.getCategoriesHandler(userId)

      return jsonify({ 'state': 'success', 'categories': allCategories }, 200)
   except Exception as e:
      return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)
   
# ----- Endpoints Notes ------

@app.route('/getNotes', methods=['POST'])
@apiKey_required
@jwt_required
def routeGetNotes(userId):
   requestData = json.loads(request.data)

   try:
      categoryId = requestData['categoryId']

      allNotes = UseNotesController.getNotesHandler(userId, categoryId)

      return jsonify({ 'state': 'success', 'notes': allNotes }, 200)
   except Exception as e:
      return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)


@app.route('/addNote', methods=['POST'])
@apiKey_required
@jwt_required
def routeAddNote(userId):
   requestData = json.loads(request.data)

   try:
      currentCategoryId = requestData['categoryId']

      noteId = UseNotesController.createNoteHandler(userId, currentCategoryId)

      return jsonify({ 'state': 'success', 'noteId': noteId }, 200)
   except Exception as e:
      return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

# Port config
def main():
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
   main()