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

class UsePhotoUploader:
   def create(self, fileName, id):

      photo = cloudinary.uploader.upload(
         fileName,
         folder = 'uploads',
         public_id = id
      )

      return photo.get('secure_url')

   def delete(self, id):

      resp = cloudinary.uploader.destroy(f'uploads/{id}')

      return resp


PhotoUploader = UsePhotoUploader()