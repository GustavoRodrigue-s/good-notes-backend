from functools import wraps
from flask import request, jsonify

from controllers.sessionController import restoreSessionHandler, sessionIdBlackList
from controllers.apiKeyController import getApiKeyHandler

from services.tokenKey import ACCESS_TOKEN_KEY

from services.jwtToken import decodeToken
import jwt

def jwt_required(f):
   @wraps(f)
   def wrapper(*args, **kwargs):
      accessToken = None
      
      if 'Authorization' in request.headers:
         accessToken = request.headers['Authorization'].split(';')[0]
      else:
         return jsonify({ "state": "unauthorized", 'reason': 'no autorization token' }, 403)

      try:
         decoded = decodeToken(accessToken, ACCESS_TOKEN_KEY)
         userId = decoded['id']

         if userId in sessionIdBlackList:
            return jsonify({ 'state': "unauthorized", 'reason': 'the session is not valid' }, 401)

      # create new accessToken
      except jwt.ExpiredSignatureError:
         refreshToken = request.headers['Authorization'].split(';')[1]

         try:
            newAccessToken = restoreSessionHandler(refreshToken)

            return jsonify(
               { 
                  'state': 'authorized',
                  'reason': 'new accessToken',
                  'newAccessToken': f'{newAccessToken}' 
               }, 100)

         except Exception as e:
            return jsonify({ 'state': 'unauthorized', 'reason': f'{e}' }, 401)

      except jwt.InvalidTokenError:
         return jsonify({ 'state': 'unauthorized', 'reason': 'invalid token' }, 401)
      except Exception as e:
         return jsonify({ 'state': 'unauthorized', 'reason': f'{e}' }, 401)


      return f(userId = userId, *args, *kwargs)

   return wrapper


def apiKey_required(f):
   @wraps(f)
   def wrapper(*args, **kwargs):

      try:
         userApiKey = request.args.get('key')

         if userApiKey == '' or userApiKey == None:
            return jsonify({ 'state': 'unauthorized', 'reason': 'no api key' }, 403)

         userId = userApiKey.split('-')[1]

         apiKeyOfThisUser = getApiKeyHandler(userId)

         if userApiKey != apiKeyOfThisUser:
            return jsonify({ 'state': "unauthorized", 'reason': 'the api key is wrong' }, 401)
            
      except:
         return jsonify({ 'state': "unauthorized" }, 403)

      return f(*args, *kwargs)

   return wrapper