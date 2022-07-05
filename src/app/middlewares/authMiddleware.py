from functools import wraps
from flask import request, jsonify

from app.controllers.AuthController import AuthController, sessionIdBlackList

from services.JwtService import JwtService
import jwt, os

from dotenv import load_dotenv

load_dotenv()

def authMiddleware(f):
   @wraps(f)
   def wrapper(*args, **kwargs):
      
      if not 'Authorization' in request.headers:
         return jsonify({ "state": "unauthorized", 'reason': 'no autorization token' }, 403)

      accessToken, refreshToken = request.headers['Authorization'].split(';')

      try:
         data = JwtService.readToken(accessToken, os.environ.get('ACCESS_TOKEN_KEY'))
         userId = data['id']

         if userId in sessionIdBlackList:
            return jsonify({ 'state': "unauthorized", 'reason': 'the session is not valid' }, 401)

      except jwt.ExpiredSignatureError:
         try:
            newAccessToken = AuthController.restoreAuthentication(refreshToken)

            return jsonify(
               { 
                  'state': 'authorized',
                  'newAccessToken': f'{newAccessToken}' 
               }, 100
            )
            
         except Exception as e:
            return jsonify({ 'state': 'unauthorized', 'reason': f'{e}' }, 401)

      except Exception as e:
         return jsonify({ 'state': 'unauthorized', 'reason': f'{e}' }, 401)

      return f(*args, *kwargs, userId)

   return wrapper