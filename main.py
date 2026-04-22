
from fastapi import FastAPI
from mongo.mongo import users
from sections import auth, posts, users, follows, likes, comments
from  fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:5173",  # tu frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def index():
    return {"message": "Hello World"}



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
