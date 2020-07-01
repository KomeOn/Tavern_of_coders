
import pymongo
from pymongo import MongoClient
import bcrypt
import datetime
from PIL import Image

class PreLoaderModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.tavernfocoders
        self.Images = self.db.images

    def get_image(self, catergor):
        if catergor == "login":
            img = self.Images.find({'used_on': catergor})
            dict_img = {}

            for i in img:
                dict_img = i
            
            return dict_img
    
    def get_all_event(self):
        pass
    
    def get_events(self):
        pass