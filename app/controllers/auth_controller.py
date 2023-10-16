from flask import Blueprint, request, jsonify
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from dotenv import load_dotenv, find_dotenv
import os                      
from datetime import datetime

auth = Blueprint('auth', __name__)

load_dotenv(find_dotenv())
hash_password_string = os.environ.get('HASH_PWD_METHOD')

@auth.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = db.User.find({"email": email})
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({"message": "Login successfully!"}), 200
        else:
            return jsonify({"message": "Incorrect email or password!"}), 400
    else:
        return jsonify({"message": "User does not exist."}), 400



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully!"}), 200


@auth.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']

    user = db.User.find({"email": email})

    if user:
        return jsonify({"message": "User already existed."}), 400
    else:
        new_user = {
            "username": request.json['username'],
            "email": email,
            "password": generate_password_hash(password, method=hash_password_string),
            "userType": request.json['userType'],
            "avatar": request.json.get('avatar', None),
            "description": request.json.get('description', None),
            "notifications": [],
            "posts": [],
            "createAt": datetime.now(),
            "updatedAt": datetime.now()
        }
        try:
            inserted_id = db.User.insert_one(new_user).inserted_id
            login_user(user, remember=True)
            return jsonify({"message": "Register successfully", "user_id": inserted_id}), 200
        except Exception as e:
            print("ERROR: ", e)

 