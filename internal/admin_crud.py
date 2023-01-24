from fastapi import APIRouter

from db.db import *

router = APIRouter()

@router.get("/delete_post")
async def delete_post(id_delete: int = None):
    post = Post.nodes.filter(nomimg=id_delete).first()
    post.delete()
    return {"post deleted"}

@router.get("/delete_image_by_id")
async def delete_image_by_id(nomimg: str = None):
    pathImg = PathImg.nodes.first(nomimg=nomimg)
    pathImg.delete()
    return {"image deleted"}