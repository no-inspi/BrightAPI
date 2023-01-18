from fastapi import APIRouter
from typing import Union, List
from fastapi import Query

from db.db import *

router = APIRouter()


@router.get("/get_all_post_user")
async def get_post(user: str = None):
    all_posts = []
    
    query = "match (u:User {username: '"+user+"'})<-[rel:`POSTED_BY`]-(t:Post) return t"

    posts, meta = db.cypher_query(query)
    posts = [Post.inflate(row[0]) for row in posts]
    
    for post in posts:
        # post = post.properties
        metric = Metrics.nodes.filter(id_gun=post.id_gun).first()
        rel = post.metrics.relationship(metric)
        
        like = {'like': len(post.likes)}
        dislike = {'dislike': len(post.dislikes)}
        

        # Commentaires
        comment_list = []
        for comment in post.comments:
            rel_com = post.comments.relationship(comment)
            comment_username = ""
            for comment_user in comment.users:
                comment_username = comment_user.username

            comment.username = comment_username
            comment.since = rel_com.since
            comment_list.append(json.loads(json.dumps(comment.__properties__,default=str)))
            

        comments = {"comments": comment_list}

        liked_list = []
        for user in post.likes:
            liked_list.append(json.loads(json.dumps(user.__properties__,default=str)))

        liked_list = {'liked_list': liked_list}

        disliked_list = []
        for user in post.dislikes:
            disliked_list.append(json.loads(json.dumps(user.__properties__,default=str)))

        disliked_list = {'disliked_list': disliked_list}

        categories_list = []
        for category in post.categories:
            categories_list.append(json.loads(json.dumps(category.__properties__,default=str)))

        categories_list = {'categories_list': categories_list}

        img_list = []
        for img in post.img:
            img_list.append(json.loads(json.dumps(img.__properties__,default=str)))

        img_list = {'img_list': img_list}
        

    
        post = json.loads(json.dumps(post.__properties__,default=str))
        metric = json.loads(json.dumps(metric.__properties__,default=str))
        rel = json.loads(json.dumps(rel.__properties__,default=str))
        
    
        merged = {**post, **metric, **rel, **like, **dislike, **comments, **liked_list, **disliked_list, **categories_list, **img_list}
        del merged['id']

        all_posts.append(merged)

    return all_posts