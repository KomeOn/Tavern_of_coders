import pymongo
from pymongo import MongoClient
import bcrypt

class RegisterModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.tavernfocoders
        self.Users = self.db.users

    def insert_user(self, data):
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        id = self.Users.insert({'username': data.username, 'name': data.name, 'password': hashed, 'email': data.email, 
                                "avatar": "None", "background": "None", "about": "None", "hobbies": "None", "birthday": "None"})
        print("UID is ",id) 
        usern = self.Users.find_one({'username': data.username})