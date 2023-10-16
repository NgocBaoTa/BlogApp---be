from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from bson.objectid import ObjectId

notification = Blueprint('notification', __name__)

@notification.route('/', methods=['GET'])
@login_required
def get_notifications():
    try:   
        user = db.User.aggregate([
            {
                "$match": {
                    "_id": current_user._id
                }
            },
            {
                "$lookup": {
                    "from": "Notification",
                    "localField": "notifications",
                    "foreignField": "_id",
                    "as": "notifications"
                }
            }, 
            {
                "$sort": {
                    "createAt": 1
                }
            }
        ]).next()
        return jsonify(user['notifications']), 200
    except Exception as e:
        return jsonify(str(e)), 400


@notification.route('/<int:notification_id>', methods=['GET'])
@login_required
def get_notification_by_id(notification_id):
    try:   
        user = db.User.aggregate([
            {
                "$match": {
                    "_id": current_user._id
                }
            },
            {
                "$lookup": {
                    "from": "Notification",
                    "localField": "notifications",
                    "foreignField": "_id",
                    "as": "notifications"
                }
            }, 
            {
                "$sort": {
                    "createAt": 1
                }
            }
        ]).next()
        
        notification = next((n for n in user['notifications'] if n['_id'] == ObjectId(notification_id)), None)
        if notification:
            return jsonify(notification), 200
        else:
            return jsonify({"message": "Notification not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@notification.route('/', methods=["POST"])
@login_required
def create_notification():
    try:
        inserted_id = db.Notification.insert_one(request.json).inserted_id
        return jsonify(db.Notification.find_one({"_id": ObjectId(inserted_id)})), 200 
    except Exception as e:
        return jsonify(str(e)), 400 
    

@notification.route('/<int:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    notification_id = ObjectId(notification_id)
    try:   
        notification = db.Notification.find_one({"_id": notification_id})
        if notification:
            if current_user._id == notification["userID"]:
                try: 
                    db.Notification.delete_one({"_id": notification_id})
                    return jsonify({"message": "Notification deleted."}), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Unauthorized to update this media."}), 403  
        else:
            return jsonify({"message": "Notification not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

