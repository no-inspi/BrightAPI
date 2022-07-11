from dis import dis
from email.policy import default
from typing import Union, List
from neomodel import StructuredNode, ArrayProperty, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, config, StructuredRel, DateTimeProperty, Q, db
import datetime,json
import pytz

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Query

app = FastAPI()

config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
# config.DATABASE_URL = 'bolt://neo4j:test@34.140.33.55:7687'
# config.ENCRYPTED_CONNECTION = False

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    password = StringProperty()

class Comment(StructuredNode):
    content = StringProperty()
    users = RelationshipTo(User, 'POSTED_BY')

class Metrics(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    vues = IntegerProperty()
    post = RelationshipTo('Post', 'EVAL')
    liked_list_view = ArrayProperty(StringProperty(), default=[])

class Category(StructuredNode):
    name = StringProperty(unique_index=True)

class Post(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    content = StringProperty()
    title = StringProperty()
    metrics = RelationshipFrom(Metrics, 'EVAL', model=MetricsRel)
    users = RelationshipTo(User, 'POSTED_BY')
    likes = RelationshipFrom(User, 'LIKED', model=LikeRel)
    dislikes = RelationshipFrom(User, 'DISLIKED', model=DisLikeRel)
    comments = RelationshipFrom(Comment, 'COMMENT', model=CommentRel)
    categories = RelationshipTo(Category, 'CATEGORISED BY')


@app.get("/")
def read_root():
    return {"Status": "Working"}



@app.get("/create_post")
async def create_post(id_gun: str = None, username: str = None, title: str = None, content: str = None, c: Union[List[str], None] = Query(default=None)):
    if(id_gun != "" and username != "" and content != "" and c and title != ""):
        post = Post(id_gun=id_gun, content=content, title=title).save()
        metrics =  Metrics(vues=0, id_gun=id_gun).save()
        user = User.nodes.filter(username=username).first()

        post.users.connect(user)
        rel = post.metrics.connect(metrics)
        rel.save()

        for category in c:
            category_save = ""
            try:
                category_save = Category.nodes.filter(name=category).first()
            except:
                category_save = Category(name=category).save()

            post.categories.connect(category_save)

        # print(rel.since)
        # rel.save()
        return {"Status": "Successfully Created !"}
    else:
        return {"error": "One parameter is missing"}

@app.get("/create_user")
async def create_user(username: str = None, password: str = None):
    if(username != "" and password != ""):
        try:
            user_verif = User.nodes.filter(username=username).first()
        except:
            # print(password)
            user = User(username=username, password=password).save()
            return {"Status": "User Successfully Created !"}
        return {'error': 'user already exists'}
    else:
        return {"error": "username is empty"}

@app.get("/create_category")
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
    
    # Commentaires
    comment_list = []
    for comment in post.comments:
        
        comment_username = ""
        for comment_user in comment.users:
            comment_username = comment_user.username
            
        comment.username = comment_username
        comment_list.append(json.loads(json.dumps(comment.__properties__,default=str)))
        

    comments = {"comments": comment_list}
        
    like = {'like': len(post.likes)}
    dislike = {'dislike': len(post.dislikes)}
    comments = {"comments": comment_list}

    
    post = json.loads(json.dumps(post.__properties__,default=str))
    metric = json.loads(json.dumps(metric.__properties__,default=str))
    rel = json.loads(json.dumps(rel.__properties__,default=str))
    
    
    merged = {**post, **metric, **rel, **like, **dislike, **comments}
    del merged['id']

    return merged

@app.get("/get_user")
async def get_user(username: str = None):
    if username and username!="":
        user = User.nodes.filter(username=username).first()
        user = json.loads(json.dumps(user.__properties__,default=str))
        return user
    else:
        return {'error': 'Username is empty'}

@app.get("/get_user_pass")
async def get_user_pass(username: str = None, password: str = None):
    if username and username!="" and password and password!= "":
        user = User.nodes.filter(username=username, password=password).first_or_none()
        if(user):
            user = json.loads(json.dumps(user.__properties__,default=str))
            return user
        else:
            return {'error': 'Username or password is incorrect'}
    else:
        return {'error': 'Username or pass is empty'}

@app.get("/get_users")
async def get_users():
   
    user = User.nodes.all()
    # user = json.loads(json.dumps(user.__properties__,default=str))
    return user
    



@app.get("/get_posts")
async def get_posts(search: str = None):

    all_posts = []
    if search=="":

        posts = Post.nodes.all()
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
            
            

            # user = {"user": user_tmp}

        
            post = json.loads(json.dumps(post.__properties__,default=str))
            metric = json.loads(json.dumps(metric.__properties__,default=str))
            # print(rel)
            rel = json.loads(json.dumps(rel.__properties__,default=str))
            
        
            merged = {**post, **metric, **rel, **like, **dislike, **comments, **liked_list, **disliked_list, **categories_list}
            del merged['id']

            all_posts.append(merged)

    else:
        print("searching ...")
        posts = Post.nodes.filter(Q(content__icontains=search) | Q(id_gun__contains=search)).all()
        for post in posts:
            metric = Metrics.nodes.filter(id_gun=post.id_gun).first()
            rel = post.metrics.relationship(metric)
            
            like = {'like': len(post.likes)}
            dislike = {'dislike': len(post.dislikes)}
            # Commentaires
            comment_list = []
            for comment in post.comments:
                comment_list.append(json.loads(json.dumps(comment.__properties__,default=str)))

            comments = {"comments": comment_list}

            # user_tmp = ""
            # for user in post.users:
            #     user_tmp = user.username
            #     print('user',user_tmp)

            # user = {"user": user_tmp}

        
            post = json.loads(json.dumps(post.__properties__,default=str))
            metric = json.loads(json.dumps(metric.__properties__,default=str))
            rel = json.loads(json.dumps(rel.__properties__,default=str))
            
        
            merged = {**post, **metric, **rel, **like, **dislike, **comments}
            del merged['id']

            all_posts.append(merged)

    # return merged
    return all_posts

@app.get("/get_posts_by_categorie")
async def get_posts_by_categorie(categorie:str = None):

    all_posts = []
    
    query = "match (c:Category {name: '"+categorie+"'})<-[rel:`CATEGORISED BY`]-(t) return t"
    posts, meta = db.cypher_query(query)
    posts = [Post.inflate(row[0]) for row in posts]
    
    # posts = Post.nodes.all()
    for post in posts:
        # post = post.properties
        metric = Metrics.nodes.filter(id_gun=post.id_gun).first()
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
        
        

        # user = {"user": user_tmp}

    
        post = json.loads(json.dumps(post.__properties__,default=str))
        metric = json.loads(json.dumps(metric.__properties__,default=str))
        rel = json.loads(json.dumps(rel.__properties__,default=str))
        
    
        merged = {**post, **metric, **rel, **like, **dislike, **comments, **liked_list, **disliked_list, **categories_list}
        del merged['id']

        all_posts.append(merged)

    return all_posts


@app.get("/update_metrics_view")
async def update_metrics(id_post:str = None, username:str = None):
    print(username)
    if username and username!="" and username is not None and username!="null":
        print("enter")
        post = Post.nodes.filter(id_gun=id_post).first()
        metric = Metrics.nodes.filter(id_gun=id_post).first()

        if (username not in metric.liked_list_view):
            metric.liked_list_view.append(username)
        metric.vues = metric.vues + 1
        metric.save()

        metric = json.loads(json.dumps(metric.__properties__,default=str))
                
            
        merged = {**metric}

        return {'test': merged}
    else:
        return {"error": "error you have not send username"}

@app.get("/get_metrics_admin_statsG")
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

@app.get("/get_metrics_admin_last_5")
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


    
    