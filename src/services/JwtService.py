import jwt

from datetime import datetime, timedelta

class UseJwtService:
   def createToken(self, payload, SECRET_KEY, time):

      payload["exp"] = datetime.utcnow() + timedelta(minutes=time)
   
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

      return token

   def readToken(self, token, SECRET_KEY):

      payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

      return payload
   

JwtService = UseJwtService()   