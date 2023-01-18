from neomodel import config

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

import os

from routers import main, post, user, interactions, user_post
from internal import admin, metrics
from gcp import file

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'unified-firefly-364609-8f7b0e555e21.json'

app = FastAPI()

config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
# config.DATABASE_URL = 'bolt://neo4j:test@34.78.232.83:7687'
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

app.include_router(file.router)







    
    