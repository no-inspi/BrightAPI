from fastapi import APIRouter

from db.db import *

router = APIRouter()



@router.get("/update_metrics_view")
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