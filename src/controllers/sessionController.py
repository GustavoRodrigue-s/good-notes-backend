from services import jwtService

from dotenv import load_dotenv
import os

from models.db.connection import connectionDB

from models.entities.User import User
from models.entities.App import App

load_dotenv()

sessionIdBlackList = []


def createSessionHandler(requestData):

   currentUser = User(requestData)
   currentUser.id = User.getCurrentUserId(currentUser)
   
   if currentUser.id in sessionIdBlackList:
      sessionIdBlackList.remove(currentUser.id)

   apiKey = User.getApiKeyHandler(currentUser.id)

   accessToken = jwtService.generateToken(currentUser.id, os.environ.get('ACCESS_TOKEN_KEY'), 5)

   if requestData['keepConnected'] == True: refreshTokenExpirationTime = 43200
   else: refreshTokenExpirationTime = 1440

   refreshToken = jwtService.generateToken(currentUser.id, os.environ.get('REFRESH_TOKEN_KEY'), refreshTokenExpirationTime)

   return { 'accessToken': accessToken, 'refreshToken': refreshToken  }, apiKey
   
   
def restoreSessionHandler(refreshToken):
   
   userId = jwtService.decodeRefreshToken(refreshToken, os.environ.get('REFRESH_TOKEN_KEY'))

   if userId in sessionIdBlackList:
      raise Exception('the session is not valid')

   newAccessToken = jwtService.generateToken(userId, os.environ.get('ACCESS_TOKEN_KEY'), 5)

   return newAccessToken


def getSessionCredentialsHandler(userId):

   userCredentials = connectionDB('getOneUser', {
      'item': '*',
      'condition': "id = %s",
      'datas': (userId, )
   })

   return userCredentials


def updateSessionCredentialsHandler(userId, newCredentials):

   newCredentials['id'] = userId

   hasUserWithSomeCredentials = connectionDB('getUserWithSomeCredentials', {
      'condition1': "email = %s AND id <> %s",
      'datas1': (newCredentials['email'], userId),
      'condition2': "username = %s AND id <> %s",
      'datas2': (newCredentials['username'], userId)
   })

   App.checkNewCredentials(newCredentials, hasUserWithSomeCredentials)

   newUserCredentials = connectionDB('updateUser', newCredentials)

   return { 'email': newUserCredentials[0], 'username': newUserCredentials[1] }


def disableSessionHandler(userId):
   sessionIdBlackList.append(userId)


def deleteSessionHandler(userId):
   connectionDB('deleteUser', {"datas": (userId, )})