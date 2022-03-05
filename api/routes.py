from flask import Flask, request, json, jsonify
from flask_cors import CORS
import os, sys

sys.dont_write_bytecode = True

sys.path.insert(1, './')
from db.createNewUser.newUser import addNewUser
from app.models.User import User

from db.connection import connectionDB

from app.handleLoginErrors.handleLoginErrors import handleLoginErrors
from app.handleRegistrationErrors.handleRegistrationErrors import handleRegistrationErrors 

from db.getUserData.getData import getUserDatas
from controllers.sessionController import createSessionHandler, deleteSessionHandler

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
      user = User(requestData)

      handleLoginErrors(user)

      print('vai chamar o createSessionHandler!', requestData['keepConnected'])

      sessionData = createSessionHandler(user, requestData['keepConnected'])

      return jsonify(
         {
            "state": "success",
            "reason": "all right",
            'apiKey': sessionData[1],
            "userData": sessionData[0]
         }, 200
      )
   except Exception as e:
      return jsonify({"errors": e, "state": "error"}, 401)


@app.route('/register', methods=['POST'])
def routeRegister():
   requestData = json.loads(request.data)

   try:
      user = User(requestData)
      
      handleRegistrationErrors(user)

      addNewUser(user)

      sessionData = createSessionHandler(user, requestData['keepConnected'])

      return jsonify(
         {
            "state": "success",
            "reason": "all right",
            "apiKey": sessionData[1],
            "userData": sessionData[0]
         }, 200
      )
   except Exception as e:
      return jsonify({"errors": e.args[0], "state": "error"}, 401)


# get user credentials
@app.route('/profile', methods=['GET'])
@apiKey_required
@jwt_required
def routeGetData(userId):
   try:
      userCredentials = getUserDatas(userId)

      return jsonify(
         { 'username': userCredentials[1], 'email': userCredentials[2] }, 200
      )
   except:
      return jsonify({ "state": "unauthorized" }, 401)


# check tokens
@app.route('/required', methods=['GET'])
@apiKey_required
@jwt_required
def routeTokenRequired(userId):

   return jsonify({ "state": "authorized" }, 200)


@app.route('/logout', methods=['GET'])
@apiKey_required
@jwt_required
def routeLogoutUser(userId):
   deleteSessionHandler(userId)

   return jsonify({ 'state': 'success' }, 200)



# Port config
def main():
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
   main()