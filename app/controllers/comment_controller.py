from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from bson.objectid import ObjectId

comment = Blueprint('comment', __name__)

@comment.route('/', methods=['GET'])
def get_comments():
    try:   
        comments = db.Comment.find()
        return jsonify(comments), 200
    except Exception as e:
        return jsonify(str(e)), 400


@comment.route('/<int:comment_id>', methods=['GET'])
def get_comment_by_id(comment_id):
    try:   
        comment = db.Comment.find_one({"_id": ObjectId(comment_id)})
        if comment:
            return jsonify(comment), 200
        else:
            return jsonify({"message": "Comment not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@comment.route('/', methods=["POST"])
@login_required
def create_comment():
    try:
        inserted_id = db.Comment.insert_one(request.json).inserted_id
        return jsonify(db.Comment.find_one({"_id": ObjectId(inserted_id)})), 200 
    except Exception as e:
        return jsonify(str(e)), 400 



@comment.route('/<int:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    comment_id = ObjectId(comment_id)
    try:   
        comment = db.Comment.find_one({"_id": comment_id})
        if comment:
            if current_user._id == comment["userID"]:
                try: 
                    db.Comment.update_one({"_id": comment_id}, request.json)
                    return jsonify(db.Comment.find_one({"_id": comment_id})), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Unauthorized to update this comment."}), 403  
        else:
            return jsonify({"message": "Comment not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@comment.route('/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment_id = ObjectId(comment_id)
    try:   
        comment = db.Comment.find_one({"_id": comment_id})
        if comment:
            if current_user._id == comment["userID"] or current_user.userType == 'admin':
                try: 
                    db.Comment.delete_one({"_id": comment_id})
                    return jsonify({"message": "Comment deleted."}), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Unauthorized to delete this comment."}), 403  
        else:
            return jsonify({"message": "Comment not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

