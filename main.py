from typing import Union
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, StructuredRel, DateTimeProperty
import datetime,json
import pytz

from fastapi import FastAPI

app = FastAPI()

config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
config.ENCRYPTED_CONNECTION = False


# class Book(StructuredNode):
#     title = StringProperty(unique_index=True)
#     author = RelationshipTo('Author', 'AUTHOR')

# class Author(StructuredNode):
#     name = StringProperty(unique_index=True)
#     books = RelationshipFrom('Book', 'AUTHOR')

# class FriendRel(StructuredRel):
#     since = DateTimeProperty(
#         default=lambda: datetime.now(pytz.utc)
#     )
#     met = StringProperty()

# class Person(StructuredNode):
#     name = StringProperty()
#     friends = RelationshipTo('Person', 'FRIEND', model=FriendRel)
# class SupplierRel(StructuredRel):
#     since = DateTimeProperty(default=datetime.now)


# class Supplier(StructuredNode):
#     name = StringProperty()
#     delivery_cost = IntegerProperty()
#     coffees = RelationshipTo('Coffee', 'SUPPLIES')


# class Coffee(StructuredNode):
#     name = StringProperty(unique_index=True)
#     price = IntegerProperty()
#     suppliers = RelationshipFrom(Supplier, 'SUPPLIES', model=SupplierRel)

class MetricsRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )
class LikeRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )

class DisLikeRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )

class CommentRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )

class User(StructuredNode):
    username = StringProperty(unique_index=True)

class Comment(StructuredNode):
    content = StringProperty()
    users = RelationshipTo(User, 'POSTED_BY')

class Metrics(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    vues = StringProperty()
    post = RelationshipTo('Post', 'EVAL')

class Post(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    content = StringProperty()
    metrics = RelationshipFrom(Metrics, 'EVAL', model=MetricsRel)
    users = RelationshipTo(User, 'POSTED_BY')
    likes = RelationshipFrom(User, 'LIKED', model=LikeRel)
    dislikes = RelationshipFrom(User, 'DISLIKED', model=DisLikeRel)
    comments = RelationshipFrom(Comment, 'COMMENT', model=CommentRel)


@app.get("/")
def read_root():
    return {"Status": "Working"}



@app.get("/create_post")
async def create_post(id_gun: str = None, username: str = None, content: str = None):
    if(id_gun != "" and username != "" and content != ""):
        post = Post(id_gun=id_gun, content=content).save()
        metrics =  Metrics(vues='170', id_gun=id_gun).save()
        user = User.nodes.filter(username=username).first()

        post.users.connect(user)
        rel = post.metrics.connect(metrics)
        
        print(rel.since)
        rel.save()
        return {"Status": "Successfully Created !"}
    else:
        return {"error": "id_gun is empty"}

@app.get("/create_user")
async def create_user(username: str = None):
    if(username != ""):
        user = User(username=username).save()
        return {"Status": "User Successfully Created !"}
    else:
        return {"error": "username is empty"}

@app.get("/add_like")
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

@app.get("/add_dislike")
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
        
@app.get("/delete_like")
async def delete_like(username: str = None, id_gun: str = None):
    if username!="" and id_gun!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()
        post.likes.disconnect(user)

        
        return {"status": "Like Deleted"} 
    else:
        {'error': "username or id_gun is empty"}

@app.get("/delete_dislike")
async def delete_dislike(username: str = None, id_gun: str = None):
    if username!="" and id_gun!="":
        post = Post.nodes.filter(id_gun=id_gun).first()
        user = User.nodes.filter(username=username).first()
        post.dislikes.disconnect(user)

        
        return {"status": "Dislike Deleted"} 
    else:
        {'error': "username or id_gun is empty"}

@app.get("/add_comment")
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

@app.get("/get_post")
async def get_post(id_gun: str = None):
    post = Post.nodes.filter(id_gun=id_gun).first()
    metric = Metrics.nodes.filter(id_gun=id_gun).first()
    # for metrics in post.metrics:
    #     print(metrics)
    #     metric = Metrics.nodes.filter(id_gun='186054fezd630defe').first()
    #     print(metric.vues)
        
    rel = post.metrics.relationship(metric)

    print(len(post.dislikes))
    like = {'like': len(post.likes)}
    dislike = {'dislike': len(post.dislikes)}

    post = json.loads(json.dumps(post.__properties__,default=str))
    metric = json.loads(json.dumps(metric.__properties__,default=str))
    rel = json.loads(json.dumps(rel.__properties__,default=str))
    
    merged = {**post, **metric, **rel, **like, **dislike}
    del merged['id']

    return merged

@app.get("/get_user")
async def get_user(username: str = None):
    if username!="":
        user = User.nodes.filter(username=username).first()
        user = json.loads(json.dumps(user.__properties__,default=str))
        return user
    else:
        return {'error': 'Invalid username'}


    
    