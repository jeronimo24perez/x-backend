from models.auth_request import Auth_request
from mongo.mongo import users
from fastapi import HTTPException, APIRouter
from google.oauth2 import id_token
from models.auth_request import Auth_request
from google.auth.transport import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
router = APIRouter()
@router.post('/auth/google')
def google_auth(auth_data: Auth_request):
    user_info = id_token.verify_oauth2_token(
            auth_data.token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
    google_id = user_info['sub']
    email = user_info['email']
    name = user_info['name']
    user = users.find_one({"email": email})
    
    if not user:
        # Si el usuario no existe por email, lo registramos
        time = datetime.now()
        formated = time.strftime("%d-%m-%Y")
        new_user = {
            "google_id": google_id,
            "email": email,
            "username": name,
            "date":  str(formated) ,
            "bio": " ",
            "follows": 0,
            "followers": 0,
            "website": "",
            "location": ""
        }

        userMaker = users.insert_one(new_user)
        message = "Usuario registrado con éxito"
        return {"msg": message, "id": str(userMaker.inserted_id) }
    else:
        # Si el usuario existe por email, verificamos si ya tiene el google_id
        if "google_id" not in user or not user["google_id"]:
            users.update_one({"_id": user["_id"]}, {"$set": {"google_id": google_id}})
        
        return {"id": str(user["_id"])}
