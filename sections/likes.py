from models.likes import Likes
from fastapi import  HTTPException, APIRouter
from mongo.mongo import users, posts,likes
from bson import ObjectId

router = APIRouter()

@router.post('/like')
def like_maker(like: Likes):
    if not ObjectId.is_valid(like.userId) or not ObjectId.is_valid(like.postId):
        raise HTTPException(status_code=401, detail="Uno o los dos Id son invalidos")
    user = users.find_one({"_id": ObjectId(like.userId)})
    post = posts.find_one({"_id": ObjectId(like.postId)})
    if not user or not post:
        raise HTTPException(status_code=401, detail="usuario o post inexistente")
    
    liker = likes.find_one(
        {
          "userId": ObjectId(like.userId),
          "postId": ObjectId(like.postId)
        }
    )
    if liker:
        raise HTTPException(status_code=401, detail="No se puede dar like dos veces")
    likes.insert_one({
          "userId": ObjectId(like.userId),
          "postId": ObjectId(like.postId)
    })

    posts.find_one_and_update(
        {"_id": ObjectId(like.postId)},
        {"$set": {
            "likes": post["likes"] + 1
        }}
    )

    return str(like.postId)

@router.delete('/like')
def delete_like(like: Likes):
    if not ObjectId.is_valid(like.userId) or not ObjectId.is_valid(like.postId):
        raise HTTPException(status_code=401, detail="Uno o los dos Id son invalidos")
    user = users.find_one({"_id": ObjectId(like.userId)})
    post = posts.find_one({"_id": ObjectId(like.postId)})
    if not user or not post:
        raise HTTPException(status_code=401, detail="usuario o post inexistente")

    liker = likes.find_one(
        {
          "userId": ObjectId(like.userId),
          "postId": ObjectId(like.postId)
        }
    )
    if not liker:
        raise HTTPException(status_code=401, detail="No se puede quitar like a un like inexistente")
    print(like)
    likes.delete_one({
          "userId": ObjectId(like.userId),
          "postId": ObjectId(like.postId)
    })

    posts.find_one_and_update(
        {"_id": ObjectId(like.postId)},
        {"$set": {
            "likes": post["likes"] - 1
        }}
    )

    return str(like.postId)

@router.get('/posts/likes/{id}')
def get_likes(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id invalido")
    post = posts.find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=400, detail="Post inexistente")
    if post["likes"] == 0:
        return "sin likes"

    like = likes.find({
        "postId": ObjectId(id)
    }).to_list()


    for i in like:
        i["_id"] =str(i["_id"])
        i["userId"] = str(i["userId"])
        i["postId"] = str(i["postId"])
    return like
        