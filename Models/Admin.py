import pymongo
from pymongo import MongoClient
import bcrypt
import datetime
from PIL import Image

class AdminModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.tavernfocoders
        self.Admins = self.db.admins
        self.Images = self.db.images
        self.Sources = self.db.sources   

    def insert_user(self, data):
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        id = self.Admins.insert({'username': data.username, 'name': data.name, 'password': hashed, 'email': data.email})
        print("UID is ",id) 
        usern = self.Admins.find_one({'username': data.username})

    def check_user(self, data):
        user = self.Admins.find_one({'username': data.username})

        if user:
            if bcrypt.checkpw(data.password.encode(), user['password']):
                return user
            else:
                return False
        else:
            return False

    def update_info(self, data):
        updated = self.Admins.update_one({
            "username": data['username']
        }, {'$set': data})

        return True
    
    def update_image(self, update):
        updated = self.Users.update_one({'used_on': update['type'], 'by': update['username'], 'date_added': datetime.datetime.now()}, {'$set': {update["type"]: update['img']}})
        #updated = self.Images.insert({'used_on': update['type'], 'restrict_img': {'avatar': update['img'], 'background': '', 'other': ''}, 
        #                              'public_img': {'avatar': '', 'background': '', 'other': ''}, 'by': update['username'], 'date_added': datetime.datetime.now()})
        return updated

    def get_profile(self, user):
        user_info = self.Admins.find_one({'username': user})
        return user_info

    def post_event(self):
        pass

    def get_all_event(self):
        pass
    
    def get_events(self):
        pass


    