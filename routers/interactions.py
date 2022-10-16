from fastapi import APIRouter
from typing import Union, List
from fastapi import Query

from db.db import *

router = APIRouter()

@router.get("/create_category")
async def create_category(name: str = None):
    if(name != ""):
        try:
            category_verif = Category.nodes.filter(name=name).first()
        except:
            category = Category(name=name).save()
            return {"Status": "category Successfully Created !"}
        return {'error': 'category already exists'}
    else:
        return {"error": "name is empty"}

@router.get("/add_like")
async def add_like(username: str = None, id_gun: str = None):
    if username!="" and id_gun!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()

        if post.likes.is_connected(user):
            return {"Error": "You have already liked"}
        else:
            if post.dislikes.is_connected(user):
                post.dislikes.disconnect(user)
                post.likes.connect(user)
            else:
                post.likes.connect(user)
            return {"Status": "Like Created"} 
    else:
        {'error': "username or id_gun is empty"}

@router.get("/add_dislike")
async def add_dislike(username: str = None, id_gun: str = None):
    if username!="" and id_gun!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()
        
        if post.dislikes.is_connected(user):
            return {"Error": "You have already disliked"}
        else:
            if post.likes.is_connected(user):
                post.likes.disconnect(user)
                post.dislikes.connect(user)
            else:
                post.dislikes.connect(user)
            return {"Status": "DisLike Created"} 
        
    else:
        {'error': "username or id_gun is empty"}
        
@router.get("/delete_like")
async def delete_like(username: str = None, id_gun: str = None):
    if username!="" and id_gun!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()
        post.likes.disconnect(user)

        
        return {"status": "Like Deleted"} 
    else:
        {'error': "username or id_gun is empty"}

@router.get("/delete_dislike")
async def delete_dislike(username: str = None, id_gun: str = None):
    if username!="" and id_gun!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()
        post.dislikes.disconnect(user)

        
        return {"status": "Dislike Deleted"} 
    else:
        {'error': "username or id_gun is empty"}

@router.get("/add_comment")
async def add_comment(username: str = None, id_gun: str = None, content: str = None):
    if username!="" and id_gun!="" and content!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()
        com = Comment(content=content).save()

        com.users.connect(user)

        post.comments.connect(com)

        
        return {"status": "Comment Created"} 
    else:
        {'error': "username or id_gun or content is empty"}