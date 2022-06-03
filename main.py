from typing import Union
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, StructuredRel, DateTimeProperty
import datetime
import pytz

from fastapi import FastAPI

app = FastAPI()

config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
config.ENCRYPTED_CONNECTION = False


class Book(StructuredNode):
    title = StringProperty(unique_index=True)
    author = RelationshipTo('Author', 'AUTHOR')

class Author(StructuredNode):
    name = StringProperty(unique_index=True)
    books = RelationshipFrom('Book', 'AUTHOR')

class FriendRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.now(pytz.utc)
    )
    met = StringProperty()

class Person(StructuredNode):
    name = StringProperty()
    friends = RelationshipTo('Person', 'FRIEND', model=FriendRel)

class Post(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    metrics = RelationshipTo('Metrics', 'METRICS')

class Metrics(StructuredNode):
    vues = StringProperty(unique_index=True)
    post = RelationshipTo('Post', 'POST')

class MetricsRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.now(pytz.utc)
    )

@app.get("/")
def read_root():
    harry_potter = Book(title='Harry potter and the..').save()
    rowling =  Author(name='J. K. Rowling').save()
    harry_potter.author.connect(rowling)
    return {"Hello": "World"}

@app.get("/get_posts")
def read_item():
    post = Post.nodes.filter(id_gun="186054fezd630")
    print(post)
    # for metrics in post[2].metrics:
    #     print(metrics)
    return {"item_id": "test"}

@app.get("/create_post")
def create_post():
    post = Post(id_gun='186054fezd630d').save()
    metrics =  Metrics(vues='180').save()
    post.metrics.connect(metrics)
    return {"Status": "Created"}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}