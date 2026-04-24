from fastapi import HTTPException, APIRouter
from models.posts import Post
from mongo.mongo import posts, users, follows
from bson import ObjectId

router = APIRouter()

@router.post('/posts')
def create_post(post: Post):

    if not ObjectId.is_valid(post.userId):
        raise HTTPException(status_code=401, detail="Object id invalido")

    user = users.find_one({"_id": ObjectId(post.userId)})
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    posts.insert_one({
        "userId": ObjectId(post.userId) ,
        "email": user["email"],
        "autor": user["username"],
        "likes": 0,
        "text": post.text,  
        "img": post.img,
        "date": post.date
    })
    return post

@router.get('/post/{id}')
def get_post(id: str):
    if not ObjectId:
        raise HTTPException(status_code=401, detail="id invalido")
    post = posts.find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="post no encontrado")
    post["_id"] = str(post["_id"])
    post["userId"] = str(post["userId"])
    return post

@router.delete('/post/{id}')
def delete_post(id: str):
    if not ObjectId:
        raise HTTPException(status_code=401, detail="id invalido")
    post = posts.delete_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="post no encontrado")
    return "post eliminado correctamente"
@router.get('/posts')
def get_posts(skip:int = 0):
    try:
        printer = posts.find({}).sort("date", -1).skip(int(skip)).limit(10)
        post_array = printer.to_list()
        array = []
        for i in post_array:
            i["_id"] = str(i["_id"])
            i["userId"] = str(i["userId"])
            array.append(i)
        return array
    except:
        raise HTTPException(status_code=401, detail="algo fallo")

@router.get('/feed/{id}')
def get_feed(id: str):

        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=401, detail="Id invalido")
        user = users.find_one({"_id": ObjectId(id)})
        if not user:
            raise HTTPException(status_code=401, detail="No existe el usuario")
        following = follows.find({
            "followerId": ObjectId(id)
        }).to_list()

        if not following:
            raise HTTPException(status_code=400, detail="no sigues a nadie")
        post_array = []
        for i in following:
            post = posts.find({"userId": ObjectId(i["followedId"])}).to_list()
            post_array.append(post)
        if not post:
            raise HTTPException(status_code=400, detail="sin posts")

        final_array = []
        for i in post_array:
            for j in i:
                j["_id"] = str(j["_id"])
                j["userId"] = str(j["userId"])
                final_array.append(j)
            #i["_id"] = str(i["_id"])
            #i["userId"] = str(i["userId"])
        return final_array
