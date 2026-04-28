from fastapi import APIRouter
import re
from mongo.mongo import users
from mongo.mongo import posts
router = APIRouter()

@router.get("/search")
def search(q: str):
    pattern = re.compile(q, re.IGNORECASE)

    found_users = list(users.find(
        {"username": {"$regex": pattern}},
        {"username": 1, "bio": 1, "followers": 1, "email": 1}
    ).limit(5))

    found_posts = list(posts.find(
        {"text": {"$regex": pattern}},
        {"userId": 1, "text": 1, "date": 1, "likes": 1}
    ).limit(10))

    for user in found_users:
        user["_id"] = str(user["_id"])

    for post in found_posts:
        post["_id"] = str(post["_id"])
        post["userId"] = str(post["userId"])

    return {"users": found_users, "posts": found_posts}