from dotenv import load_dotenv

load_dotenv()

import cloudinary, os
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
   cloud_name = os.environ.get('CLOUDINARY_NAME'), 
   api_key = os.environ.get('CLOUDINARY_API_KEY'), 
   api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
   secure = True
)

class UsePhotoService:
   def create(self, url):

      photo = cloudinary.uploader.upload(url, folder = "uploads")

      photoId = photo.get('public_id').split('/')[1]

      return photo.get('secure_url'), photoId

   def update(self, url, id):

      photo = cloudinary.uploader.upload(
         url,
         folder = 'uploads',
         public_id = id
      )

      return photo.get('secure_url'), id

   def delete(self, id):

      resp = cloudinary.uploader.destroy(f'uploads/{id}')

      return resp


PhotoService = UsePhotoService()