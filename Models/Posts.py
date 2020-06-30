import pymongo
from pymongo import MongoClient
import bcrypt
import datetime
import humanize
from bson import ObjectId

class Posts:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.tavernfocoders
        self.Users = self.db.users
        self.Posts = self.db.posts
        self.Comments = self.db.comments

    def insert_posts(self, data):
        inserted = self.Posts.insert({'username': data.username, 'content': data.content, 'date_added': datetime.datetime.now()})   
        post = self.Posts.find_one({"_id": inserted})
        new_post = {}
        new_post['name'] = self.Users.find_one({'username': post['username']})['name']
        new_post['content'] = post['content']
        return True    

    def get_all_posts(self):
        all_posts = self.Posts.find({}).sort('date_added', -1)
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({'username': post["username"]})
            post['timestamp'] = humanize.naturaltime(datetime.datetime.now() - post['date_added'])
            post['old_comments'] = self.Comments.find({'post_id': str(post['_id'])})
            post['comments'] = []

            for comment in post['old_comments']:
                comment['user'] = self.Users.find_one({'username': comment['username']})
                comment['timestamp'] = humanize.naturaltime(datetime.datetime.now() - comment['date_added'])
                post['comments'].append(comment)
            new_posts.append(post)

        return new_posts

    def get_user_posts(self, user):
        all_posts = self.Posts.find({'username': user}).sort('date_added', -1)
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({'username': post["username"]})
            post['timestamp'] = humanize.naturaltime(datetime.datetime.now() - post['date_added'])
            post['old_comments'] = self.Comments.find({'post_id': str(post['_id'])})
            post['comments'] = []

            for comment in post['old_comments']:
                comment['user'] = self.Users.find_one({'username': comment['username']})
                comment['timestamp'] = humanize.naturaltime(datetime.datetime.now() - comment['date_added'])
                post['comments'].append(comment)
            new_posts.append(post)

        return new_posts

    def add_comment(self, comment):
        inserted = self.Comments.insert({'post_id': comment["post_id"], 'comment-text': comment['comment-text'], 'date_added': datetime.datetime.now(), 'username': comment['username']})
        return inserted