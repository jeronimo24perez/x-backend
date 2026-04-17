
from fastapi import FastAPI
from mongo.mongo import users
from sections import auth, posts, users, follows, likes, comments
app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}

#auth
#read users
@app.get("/users")
async def  get_users():
    finder = users.find({}).to_list(100)

    return [
        {**user, "_id": str(user["_id"])}
        for user in finder
    ]
#auth
app.include_router(auth.router)

#users

app.include_router(users.router)

#follows

app.include_router(follows.router)

#posts

app.include_router(posts.router)
#likes

app.include_router(likes.router)
#comments
app.include_router(comments.router)
