from typing import Union
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

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



@app.get("/")
def read_root():
    rowling =  Author(name='J. K. Rowling').save()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}