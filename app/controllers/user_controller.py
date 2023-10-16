from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from bson.objectid import ObjectId

user = Blueprint('user', __name__)

@user.route('/', methods=['GET'])
@login_required
def get_users():
    if current_user.userType == 'admin':
        try:   
            users = db.User.find()
            return jsonify(users), 200
        except Exception as e:
            return jsonify(str(e)), 400
    else: 
        return jsonify({"message": "Unauthorized to get all users."}), 403
    

@user.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:   
        user = db.User.find_one({"_id": ObjectId(user_id)})
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400


@user.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user_id = ObjectId(user_id)
    try:   
        user = db.User.find_one({"_id": user_id})
        if user:
            if current_user._id == user["userID"]:
                try: 
                    db.User.update_one({"_id": user_id}, request.json)
                    return jsonify(db.User.find_one({"_id": user_id})), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Unauthorized to update this user."}), 403  
        else:
            return jsonify({"message": "User not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@user.route('/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user_id = ObjectId(user_id)
    try:   
        user = db.User.find_one({"_id": user_id})
        if user:
            if current_user._id == user["userID"]:
                try: 
                    db.User.delete_one({"_id": user_id})
                    return jsonify({"message": "User deleted."}), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Unauthorized to delete this user."}), 403  
        else:
            return jsonify({"message": "User not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

