from fastapi import APIRouter
# from typing import Union, List

from db.db import *

router = APIRouter()


@router.get("/get_metrics_admin_statsG")
async def get_metrics_admin_statsG():
    user = len(User.nodes.all())
    posts = len(Post.nodes.all())
    comments = len(Comment.nodes.all())

    query = "MATCH (n)-[r:LIKED]->() RETURN count(r)"
    like, meta = db.cypher_query(query)
    query = "MATCH (n)-[r:DISLIKED]->() RETURN count(r)"
    dislike, meta = db.cypher_query(query)


    result = {
        "user": user,
        "posts": posts,
        "comments": comments,
        "like": like[0][0],
        "dislike": dislike[0][0]
    }
    return result

@router.get("/get_metrics_admin_last_5")
async def get_metrics_admin_last_5(number: int):
    all_posts = []

    query = "MATCH (n:Post)-[r:EVAL]-(post) RETURN n order by r.since DESC LIMIT "+str(number)
    posts, meta = db.cypher_query(query)
    # posts = Post.nodes.order_by('-<id>').all()[:number]
    posts = [Post.inflate(row[0]) for row in posts]
    for post in posts:
        metric = Metrics.nodes.filter(id_gun=post.id_gun).first()
        # print(metric)
        rel = post.metrics.relationship(metric)
        
        like = {'like': len(post.likes)}
        dislike = {'dislike': len(post.dislikes)}
        

        # Commentaires
        comment_list = []
        for comment in post.comments:
            
            comment_username = ""
            for comment_user in comment.users:
                comment_username = comment_user.username

            comment.username = comment_username
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
        author = ""
        for user in post.users:
            author = user.username

        author = {"author": author}

    
        post = json.loads(json.dumps(post.__properties__,default=str))
        metric = json.loads(json.dumps(metric.__properties__,default=str))
        # print(rel)
        rel = json.loads(json.dumps(rel.__properties__,default=str))
        
    
        merged = {**post, **author, **metric, **rel, **like, **dislike, **comments, **liked_list, **disliked_list, **categories_list}
        del merged['id']

        all_posts.append(merged)
    return all_posts