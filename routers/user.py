from fastapi import APIRouter, Request

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

@router.post("/update_user")
async def update_user(username: str = None, info: Request = None):
    req_info = await info.json()  
        
    this_user = User.nodes.filter(username=username).first()
    if req_info['username'] != None:
        this_user.username = req_info['username']

    if req_info['first_name'] != None:
        this_user.first_name = req_info['first_name']
    
    if req_info['last_name']!= None:
        this_user.last_name = req_info['last_name']
        
    if req_info['dateBirth']!= None:
        this_user.birthdate = req_info['dateBirth']
    
    if req_info['email']!= None:
        this_user.email = req_info['email']

    this_user.save()
    

    return {"Status": "User Successfully Updated!"}
