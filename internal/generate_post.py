from fastapi import APIRouter
from generate_with_openai import clean_file, get_response_from_openai, generate_image
# from typing import Union, List
import hashlib
from Crypto.Cipher import AES
import datetime


from db.db import *

router = APIRouter()

k = hashlib.sha256(b"my-secret-key@123").digest()

@router.get("/generate_post")
async def generate_post():
    lines = clean_file("idea_end_withoutblank.txt")
    currentTimestamp = datetime.datetime.now().timestamp()
    username = 'padaqor'
    # id_to_crypt = str(currentTimestamp) + '+' + username + '+' + 'test'
    
    # cipher = AES.new(k, AES.MODE_EAX)
    # id_encrypt, tag = cipher.encrypt_and_digest(bytes(id_to_crypt, encoding='utf-8'))
    i=0
    try:
        posts = Post.nodes.order_by('-id_gun').first()
        id_gun = int(posts.id_gun)
    except: 
        id_gun = 0

    for line in lines:
        i+=1
        resp_tamp = get_response_from_openai(line)
        




        post = Post(id_gun=id_gun, content=resp_tamp, title=line).save()
        metrics =  Metrics(vues=0, id_gun=id_gun).save()
        user = User.nodes.filter(username='padaqor').first()

        post.users.connect(user)
        rel = post.metrics.connect(metrics)
        rel.save()

        if (i<8):
            c = ['Artificial intelligence']
        elif i<18:
            c = ['Deep learning']
        elif i<23:
            c = ["DevOps"]
        elif i<33:
            c = ["Computer Science"]
        elif i<42:
            c = ["Programming language"]
        elif i>=42:
            c = ['General fact about software engineer']
        

        # c = ['Computer science', 'artificial intelligence']

        for category in c:
            category_save = ""
            try:
                category_save = Category.nodes.filter(name=category).first()
            except:
                category_save = Category(name=category).save()

            post.categories.connect(category_save)
        
        print('post generated successfully number : '+str(i))
        id_gun+=1

    return {'Status': 'Done'}

@router.get("/init_index")
async def init_index():
    post = Post.nodes.order_by('-id_gun').first()
    print(post.id_gun)
    # all_post = Post.nodes.all()
    # i=0
    # for post in all_post:
    #    post.id_gun = i
    #    post.save()
    #    i+=1 
@router.get("/init_index_metrics")
async def init_index_metrics():
    all_post = Metrics.nodes.all()
    for post in all_post:
       post.id_gun = int(post.id_gun)
       post.save()

from pathlib import Path
import pathlib
import json
import openai
import os
from decouple import config
from base64 import b64decode

DATA_DIR = Path.cwd() / "responses"
DATA_DIR.mkdir(exist_ok=True)

IMAGE_DIR = Path.cwd() / "images"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

ALL_PATH_IMAGE_DIR = r"C:\Users\charl\Mes documents\Github\FrontAndGunBright\public\images"

print(ALL_PATH_IMAGE_DIR)

@router.get("/generate_image")
async def generate_image(): 
    all_post = Post.nodes.all()
    openai.api_key = config("OPENAI_API_KEY")
    i=0
    for post in all_post:
        i+=1
        if len(post.img)==0:

            response = openai.Image.create(
                prompt=post.title,
                n=1,
                size="512x512",
                response_format="b64_json",
            )

            image_data = b64decode(response['data'][0]["b64_json"])
            image_file = ALL_PATH_IMAGE_DIR+"\\"+"-"+str(i)+".png"

            with open(image_file, mode="wb") as png:
                png.write(image_data)
                
            img = PathImg(nomimg='images/'+"-"+str(i)+".png").save()
            post.img.connect(img)
        print("image generated successfully number : "+str(i))

    return {'status': 'success'}
