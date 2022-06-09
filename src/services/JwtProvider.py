import jwt

from datetime import datetime, timedelta

class UseJwtProvider:
   def createToken(self, id, SECRET_KEY, time):

      data = { "id": id, "exp": datetime.utcnow() + timedelta(minutes=time) }
   
      token = jwt.encode(data, SECRET_KEY, algorithm='HS256')

      return token

   def readToken(self, token, SECRET_KEY):

      payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

      return payload
   

JwtProvider = UseJwtProvider()   