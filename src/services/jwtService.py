import jwt

from datetime import datetime, timedelta

def generateToken(id, SECRET_KEY, time):

   data = { "id": id, "exp": datetime.utcnow() + timedelta(minutes=time) }
   
   token = jwt.encode(data, SECRET_KEY, algorithm='HS256')

   return token


def decodeToken(token, SECRET_KEY):

      payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

      return payload
      

def decodeRefreshToken(refreshToken, SECRET_KEY):
   try:

      userId = decodeToken(refreshToken, SECRET_KEY)['id']

      return userId

   except jwt.ExpiredSignatureError:
      raise Exception('expired refreshToken')
   except jwt.InvalidTokenError:
      raise Exception('invalid refreshToken')
   except Exception as e:
      raise Exception(e)