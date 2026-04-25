from models.comment import Comment
from fastapi import  HTTPException, APIRouter
from mongo.mongo import users, posts,likes, comments
from bson import ObjectId

router = APIRouter()

@router.post('/comment/{post_id}')
def comment(post_id: str, comment: Comment):
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=400, detail="id invalido")
        post = posts.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(status_code=400, detail="Post inexistente")
        print(comment)
        commentCreate= comments.insert_one({
                "userId": comment.userId,
                "postId": post_id,
                "text": comment.text,
                "date": comment.date,
                "img": comment.img
        })
        commentPosted = {
            "_id": str(commentCreate.inserted_id),
            "comment": comment
        }


        return commentPosted
  
@router.delete('/comment/{id}')
def delete_comment(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id invalido")
    comment = comments.find_one({"_id": ObjectId(id)})
    if not comment:
       raise HTTPException(status_code=400, detail="comentario inexistente")
    comments.delete_one({
        "_id": ObjectId(id)
    })
    return {"message": "comentario eliminado"}

@router.get('/posts/{post_id}/comments/')
def get_comments(post_id: str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="id invalido")
    post = posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=400, detail="Post inexistente")
    post_comments = comments.find({"postId": post_id}).to_list()
    for i in post_comments:
        i["_id"] = str(i["_id"])
        i["userId"] = str( i["userId"])
        i["postId"] = str(i["postId"])
    return post_comments
