from fastapi import APIRouter

from typing import List

from fastapi import UploadFile
import shutil
from pathlib import Path

from google.cloud import storage
import os

from db.db import *

router = APIRouter()

# http://127.0.0.1:8000/uploadfiles/?destination=images
@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile], destination: Path, id_gun: str = None):
    storage_client = storage.Client()
    bucket_name = "braightimgstorage"
    bucket = storage_client.get_bucket(bucket_name)
    post = Post.nodes.filter(id_gun=id_gun).first()


    for file in files:
        destinationtamp = str(destination)+'/'+file.filename
        
        try:
            with Path(destinationtamp).open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except:
            return {'error': 'error in uploading file'}
        finally:
            file.file.close()
            # return {"filenames": [file.filename for file in files]}
        bucket_file = file.filename
        blob = bucket.blob(bucket_file)
        # Upload the file to a destination
        blob.upload_from_filename('images/'+file.filename)
        blob.make_public()

        img = PathImg(nomimg=blob.public_url).save()
        post.img.connect(img)

    return {'status': 'success'}



@router.post("/testgcp/")
async def testgcp(files: List[UploadFile]):
    storage_client = storage.Client()
    bucket_file = files[0].filename
    #The name for the new bucket
    bucket_name = "braightimgstorage"

    bucket = storage_client.get_bucket(bucket_name)

    # # Creates the new bucket
    # bucket = storage_client.create_bucket(bucket_name)

    # Create a blob object from the filepath
    blob = bucket.blob(bucket_file)
    # Upload the file to a destination
    blob.upload_from_filename('images/'+files[0].filename)
    blob.make_public()
    
    # print(f"Bucket {bucket.name} created.")
    return {'test on gcp': 'success'}