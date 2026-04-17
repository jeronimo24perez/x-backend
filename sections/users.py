from fastapi import HTTPException, APIRouter
from models.user import User
from mongo.mongo import posts, users
from bson import ObjectId
from pymongo import ReturnDocument
router = APIRouter()

@router.get('/user/{id}')
def get_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="id invalido")
    user = users.find_one({"_id":  ObjectId( id )})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user["_id"] = str(user["_id"])
    return {"user": user}

@router.get('/user/posts/{id}')
def get_user_posts(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="id invalido")
    user = users.find_one({"_id":  ObjectId( id )})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    post = posts.find({"userId": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="Usuario sin posts")
    post_saver = []
    list_post = post.to_list()

    for i in list_post:
        i["_id"] = str(i["_id"])
        i["userId"] = str(i["userId"])
        post_saver.append(i)
    return post_saver

@router.put('/user/{id}')
def update_user(id: str, userObj: User):
    if not ObjectId.is_valid(id):
       raise HTTPException(status_code=404, detail="id invalido")
    user = users.find_one({"_id":  ObjectId( id )})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    print(user)
    updater = users.find_one_and_update(
            {"_id": ObjectId(id)},
            {
                "$set":{
                    "username": userObj.username,
                    "email": userObj.email,
                    "password": userObj.password,
                    "date": userObj.date,
                    "bio": userObj.bio,
                    "follows": userObj.follows,
                    "followers": userObj.followers,
                    "website": userObj.website,
                    "location": userObj.location
            }
            }
    ,
            return_document=ReturnDocument.AFTER
    )
    updater["_id"] = str(updater["_id"])
    return {"user": updater}