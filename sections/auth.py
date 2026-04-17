
from helpers.generate_token import generate_token
from models.user import User
from models.login import Login
from bson import ObjectId
from fastapi import HTTPException, APIRouter
from mongo.mongo import users


router = APIRouter()


@router.post('/auth/register')
def register(user: User):
    email = users.find_one({"email": user.email})
    username = users.find_one({"username": user.username})

    if(not email and not username):
        users.insert_one({
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "date": user.date,
            "bio": "",
            "follows": 0,
            "followers": 0,
            "website": "",
            "location": "",
        })
        return {"message": "Registered", "user":user}
    else:
        raise HTTPException(status_code=401, detail="Ya existe alguien con ese email o ese nombre de usuario")

@router.post('/auth/login')
def login(data: Login):
    user = users.find_one({"email": data.email})
    if not user:
       raise HTTPException(status_code=404, detail="usuario no encontrado")
    if(user['password'] == data.password):
        return {"token": generate_token(), "auth": "true"}
    else:
        raise HTTPException(status_code=404, detail="contraseña fallida")

@router.get('/auth/me/{id}')
def auth(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="id invalido")

    user = users.find_one({"_id":  ObjectId( id )})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user["_id"] = str(user["_id"])
    return {"user": user}