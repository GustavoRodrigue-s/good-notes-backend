from functools import wraps
from flask import request, jsonify

import os, jwt

from services.JwtProvider import JwtProvider

def emailConfirmationMiddleware(f):
   @wraps(f)
   def wrapper(*args, **kwargs):

      try:
         emailConfirmationToken = request.args.get('emailConfirmationToken')

         if not emailConfirmationToken:
            raise Exception('no email confirmation token')

         try:
            payload = JwtProvider.readToken(emailConfirmationToken, os.environ.get('EMAIL_CONFIRMATION_TOKEN_KEY'))

            return f(*args, *kwargs, payload)

         except jwt.ExpiredSignatureError:
            raise Exception('email confirmation token expired')

      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   return wrapper