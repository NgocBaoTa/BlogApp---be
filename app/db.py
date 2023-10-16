from dotenv import load_dotenv, find_dotenv
import os                       
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash 

load_dotenv(find_dotenv())

hash_password_string = os.environ.get('HASH_PWD_METHOD')
connection_string = os.environ.get('MONGODB_URI')
client = MongoClient(connection_string)  
db = client.Blog 

from .models.Category import create_category_collection
from .models.Comment import create_comment_collection
from .models.Media import create_media_collection
from .models.Notification import create_notification_collection
from .models.Post import create_post_collection
from .models.User import create_user_collection
from .models.Viewer import create_viewer_collection


def create_collections(): 
    create_category_collection()
    create_comment_collection()
    create_media_collection()
    create_notification_collection()
    create_post_collection()
    create_user_collection()
    create_viewer_collection()


def insert_category():
    categories = [
        {
            "categoryName": "Breakfast",
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "categoryName": "Bread",
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "categoryName": "Salad",
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "categoryName": "Dessert",
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "categoryName": "Soup",
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
    ]

    db.Category.insert_many(categories)


def insert_user():
    users = [
        {
            "username": "admin",
            "email": "admin@gmail.com",
            "password": generate_password_hash("password", method=hash_password_string),
            "userType": "admin",
            "avatar": "https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg",
            "description": "This is admin of the website.",
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "username": "user1",
            "email": "user1@gmail.com",
            "password": generate_password_hash("password1", method=hash_password_string),
            "userType": "user",
            "avatar": "https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg",
            "description": "This is user1 of the website.",
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": generate_password_hash("password2", method=hash_password_string),
            "userType": "user",
            "avatar": "https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg",
            "description": "This is user2 of the website.",
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "username": "user3",
            "email": "user3@gmail.com",
            "password": generate_password_hash("password3", method=hash_password_string),
            "userType": "user",
            "avatar": "https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg",
            "description": "This is user3 of the website.",
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "username": "user4",
            "email": "user4@gmail.com",
            "password": generate_password_hash("password4", method=hash_password_string),
            "userType": "user",
            "avatar": "https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg",
            "description": "This is user4 of the website.",
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
        {
            "username": "user5",
            "email": "user5@gmail.com",
            "password": generate_password_hash("password5", method=hash_password_string),
            "userType": "user",
            "avatar": "https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg",
            "description": "This is user5 of the website.",
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updateAt": datetime.now()
        },
    ]

    db.User.insert_many(users)


create_collections()
insert_category()
insert_user()