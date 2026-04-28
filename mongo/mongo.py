from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://jeronimo24perez:demar@back.dgejetl.mongodb.net/?appName=back"
client = MongoClient(uri, server_api=ServerApi('1'))



try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['X']
users = db['users']
posts = db['posts']
follows = db['follows']
likes = db['likes']
comments = db['comments']

