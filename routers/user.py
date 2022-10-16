from fastapi import APIRouter

from db.db import *

router = APIRouter()

@router.get("/create_user")
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


@router.get("/get_user")
async def get_user(username: str = None):
    if username and username!="":
        user = User.nodes.filter(username=username).first()
        user = json.loads(json.dumps(user.__properties__,default=str))
        return user
    else:
        return {'error': 'Username is empty'}

@router.get("/get_user_pass")
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

@router.get("/get_users")
async def get_users():
   
    user = User.nodes.all()
    # user = json.loads(json.dumps(user.__properties__,default=str))
    return user