from fastapi import HTTPException, APIRouter
from models.follow import Follow
from bson import ObjectId
from mongo.mongo import users, follows


router = APIRouter()

@router.post('/follow')
def create_follow(follow: Follow):

    if (not ObjectId.is_valid( follow.followedId) or not ObjectId.is_valid( follow.followerId)):
        raise HTTPException(status_code=401, detail="Uno de los dos o los dos Id son incorrectos")
    followed = users.find_one({"_id": ObjectId( follow.followedId)})
    follower = users.find_one({"_id": ObjectId( follow.followerId)})
    if (not followed or not follower):
        raise HTTPException(status_code=401, detail="uno o los dos usuarios no existen")
    if (follow.followedId == follow.followerId):
        raise HTTPException(status_code=401, detail="No puedes seguirte a ti mismo")
    finder = follows.find_one({
        "followerId": ObjectId(follow.followerId),
        "followedId": ObjectId(follow.followedId)
    })

    if finder:
        raise HTTPException(status_code=401, detail="Ya sigues esta persona")
    follows.insert_one({
        "followerId": ObjectId(follow.followerId) ,
        "followedId": ObjectId(follow.followedId)
    })
    updater = users.find_one({"_id": ObjectId(follow.followedId)})

    users.find_one_and_update(
        {"_id": ObjectId(follow.followedId)},
        {"$set": {
            "followers": updater["followers"] + 1
        }}
    )
    updater_two = users.find_one({"_id": ObjectId(follow.followerId)})
    users.find_one_and_update(
        {"_id": ObjectId(follow.followerId)},
        {"$set": {
            "follows": updater_two["follows"] + 1
        }}
    )
    return {"peticion": "realizada"}

@router.delete('/follow')
def delete_follow(follow: Follow):
    if (not ObjectId.is_valid( follow.followedId) or not ObjectId.is_valid( follow.followerId)):
        raise HTTPException(status_code=401, detail="Uno de los dos o los dos Id son incorrectos")
    followed = users.find_one({"_id": ObjectId( follow.followedId)})
    follower = users.find_one({"_id": ObjectId( follow.followerId)})
    if (not followed or not follower):
        raise HTTPException(status_code=401, detail="uno o los dos usuarios no existen")
    finder = follows.find_one({
        "followerId": ObjectId(follow.followerId),
        "followedId": ObjectId(follow.followedId)
    })
    if not finder:
        raise HTTPException(status_code=401, detail="No existe este follow")
    follow_deleted = follows.find_one_and_delete({
        "followerId": ObjectId(follow.followerId) ,
        "followedId": ObjectId(follow.followedId)
    })
    updater = users.find_one({"_id": ObjectId(follow.followedId)})

    users.find_one_and_update(
        {"_id": ObjectId(follow.followedId)},
        {"$set": {
            "followers": updater["followers"] - 1
        }}
    )
    updater_two = users.find_one({"_id": ObjectId(follow.followerId)})
    users.find_one_and_update(
        {"_id": ObjectId(follow.followerId)},
        {"$set": {
            "follows": updater_two["follows"] - 1
        }}
    )
    follow_deleted["_id"] = str(follow_deleted["_id"])
    follow_deleted["followerId"] = str(follow_deleted["followerId"])
    follow_deleted["followedId"] = str(follow_deleted["followedId"])
    
    return follow_deleted

@router.get('/following/{id}')
def get_followers(id: str):
    if (not ObjectId.is_valid( id) ):
        raise HTTPException(status_code=401, detail=" Id incorrecto")
    user = users.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=401, detail="usuario no existe")
    finder = follows.find({
        "followerId": ObjectId(id),
    }).to_list()
    if not finder:
        raise HTTPException(status_code=401, detail="No existe este follow")

    for i in finder:
        i["_id"] = str(i["_id"])
        i["followerId"] = str(i["followerId"])
        i["followedId"] = str(i["followedId"])

    return {"find": finder}


@router.get('/followers/{id}')
def get_followed(id: str):
    if (not ObjectId.is_valid( id) ):
        raise HTTPException(status_code=401, detail=" Id incorrecto")
    user = users.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=401, detail="usuario no existe")
    finder = follows.find({
        "followedId": ObjectId(id),
    }).to_list()
    if not finder:
        raise HTTPException(status_code=401, detail="No existe este follow")

    for i in finder:
        i["_id"] = str(i["_id"])
        i["followerId"] = str(i["followerId"])
        i["followedId"] = str(i["followedId"])

    return {"find": finder}