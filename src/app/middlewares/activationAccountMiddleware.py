from functools import wraps
from flask import request, jsonify

import os, jwt

from services.JwtProvider import JwtProvider

def activationAccountMiddleware(f):
   @wraps(f)
   def wrapper(*args, **kwargs):

      try:
         activationToken = request.args.get('activationToken')

         if not activationToken:
            raise Exception('no activation token')

         try:
            userId = JwtProvider.readToken(activationToken, os.environ.get('ACTIVATION_TOKEN_KEY'))['id']

            return f(*args, *kwargs, userId)

         except jwt.ExpiredSignatureError:
            raise Exception('activation token expired')

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   return wrapper