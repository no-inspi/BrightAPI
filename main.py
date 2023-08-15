from neomodel import config

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

import os

from routers import main, post, user, interactions, user_post
from internal import admin, metrics, generate_post, admin_crud
from gcp import file

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'unified-firefly-364609-8f7b0e555e21.json'

app = FastAPI()

# config.DATABASE_URL = 'bolt://neo4j:test1234@localhost:7687'
# neo4j+s://f8ed2e04.databases.neo4j.io
config.DATABASE_URL = 'neo4j+s://{}:{}@{}'.format("neo4j", "9QU98_zanaY8ukCBOuXtfwSyzLPBw99TgOGHSHkjprY", "f8ed2e04.databases.neo4j.io")

# 9QU98_zanaY8ukCBOuXtfwSyzLPBw99TgOGHSHkjprY
# config.DATABASE_URL = 'bolt://neo4j:sM6Z48en@34.79.181.172:7687'
config.ENCRYPTED_CONNECTION = False

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

app.include_router(main.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(interactions.router)
app.include_router(user_post.router)

app.include_router(admin.router)
app.include_router(metrics.router)
app.include_router(generate_post.router)
app.include_router(admin_crud.router)

app.include_router(file.router)







    
    