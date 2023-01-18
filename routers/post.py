from fastapi import APIRouter
from typing import Union, List
from fastapi import Query

from db.db import *

router = APIRouter()

@router.get("/create_post")
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


@router.get("/get_post")
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

@router.get("/get_posts")
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
                rel_com = post.comments.relationship(comment)
                print(rel_com.since)
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
            # print(rel)
            rel = json.loads(json.dumps(rel.__properties__,default=str))
            
        
            merged = {**post, **metric, **rel, **like, **dislike, **comments, **liked_list, **disliked_list, **categories_list, **img_list}
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

            img_list = []
            for img in post.img:
                img_list.append(json.loads(json.dumps(img.__properties__,default=str)))

            img_list = {'img_list': img_list}

            # user_tmp = ""
            # for user in post.users:
            #     user_tmp = user.username
            #     print('user',user_tmp)

            # user = {"user": user_tmp}

        
            post = json.loads(json.dumps(post.__properties__,default=str))
            metric = json.loads(json.dumps(metric.__properties__,default=str))
            rel = json.loads(json.dumps(rel.__properties__,default=str))
            
        
            merged = {**post, **metric, **rel, **like, **dislike, **comments, **img_list}
            del merged['id']

            all_posts.append(merged)

    # return merged
    return all_posts

@router.get("/get_posts_by_categorie")
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

        img_list = []
        for img in post.img:
            img_list.append(json.loads(json.dumps(img.__properties__,default=str)))

        img_list = {'img_list': img_list}
        
        

        # user = {"user": user_tmp}

    
        post = json.loads(json.dumps(post.__properties__,default=str))
        metric = json.loads(json.dumps(metric.__properties__,default=str))
        rel = json.loads(json.dumps(rel.__properties__,default=str))
        
    
        merged = {**post, **metric, **rel, **like, **dislike, **comments, **liked_list, **disliked_list, **categories_list, **img_list}
        del merged['id']

        all_posts.append(merged)

    return all_posts