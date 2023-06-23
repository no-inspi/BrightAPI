from fastapi import APIRouter
import hashlib
from random_username.generate import generate_username
import random
from math import ceil, floor

from db.db import *

router = APIRouter()

@router.get("/delete_post")
async def delete_post(id_delete: int = None):
    post = Post.nodes.filter(nomimg=id_delete).first()
    post.delete()
    return {"post deleted"}

@router.get("/delete_image_by_id")
async def delete_image_by_id(nomimg: str = None):
    pathImg = PathImg.nodes.first(nomimg=nomimg)
    pathImg.delete()
    return {"image deleted"}



@router.get("/generate_users")
async def generate_users(numberofuser: int = None):
    username = 'charlie'
    password = 'test'
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    array_user_generated = generate_username(numberofuser)
    i=0
    for username in array_user_generated:
        i+=1
        if(username != "" and password != ""):
            try:
                user_verif = User.nodes.filter(username=username).first()
            except:
                user = User(username=username, password=password_hash).save()
        print('user created, username : '+str(username)+' numero : '+str(i))

    return {"users created"}

def add_like(post,user):
    if post.likes.is_connected(user):
        print('already liked')
    else:
        if post.dislikes.is_connected(user):
            post.dislikes.disconnect(user)
            post.likes.connect(user)
        else:
            post.likes.connect(user)

def add_dislike(post,user):
    if post.dislikes.is_connected(user):
        print('already disliked')
    else:
        if post.likes.is_connected(user):
            post.likes.disconnect(user)
            post.dislikes.connect(user)
        else:
            post.dislikes.connect(user)

def random_username_like_dislike(all_users,numberofuser):
    random_array = random.choices(all_users,k=numberofuser)

    percentage = random.uniform(0.6, 0.95)

    like_array = random.choices(random_array, k = ceil(len(random_array)*percentage))
    dislike_array = []
    for random_user in random_array:
        if random_user not in like_array:
            dislike_array.append(random_user)



    return like_array, dislike_array


@router.get("/generate_like_dislike")
async def generate_like_dislike():
    all_posts = Post.nodes.all()
    all_users = User.nodes.all()

    for post in all_posts:
        number_user = random.uniform(25,len(all_users))
        like_array, dislike_array = random_username_like_dislike(all_users,floor(number_user))
        for like_user in like_array:
            add_like(post,like_user)
        
        for dislike_user in dislike_array:
            add_dislike(post,dislike_user)
    # for post in all_posts:
    #     print(post.title)
    # for user in all_users:
    #     print(user.username)
    return {'Done'}