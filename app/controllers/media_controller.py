from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from bson.objectid import ObjectId

media = Blueprint('media', __name__)

@media.route('/', methods=['GET'])
def get_medias():
    try:   
        medias = db.Media.find()
        return jsonify(medias), 200
    except Exception as e:
        return jsonify(str(e)), 400


@media.route('/<int:media_id>', methods=['GET'])
def get_media_by_id(media_id):
    try:   
        media = db.Media.find_one({"_id": ObjectId(media_id)})
        if media:
            return jsonify(media), 200
        else:
            return jsonify({"message": "Media not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@media.route('/', methods=["POST"])
@login_required
def create_media():
    try:
        inserted_id = db.Media.insert_one(request.json).inserted_id
        return jsonify(db.Media.find_one({"_id": ObjectId(inserted_id)})), 200 
    except Exception as e:
        return jsonify(str(e)), 400 


@media.route('/<int:media_id>', methods=['PUT'])
@login_required
def update_media(media_id):
    media_id = ObjectId(media_id)
    try:   
        media = db.Media.find_one({"_id": media_id})
        if media:
            try:
                post = db.Post.find_one({"_id": media['postID']})
                if post:
                    author = post['authorID']

                    if current_user._id == author or current_user.userType == 'admin':
                        try: 
                            db.Media.update_one({"_id": media_id}, request.json)
                            return jsonify(db.Media.find_one({"_id": media_id})), 200
                        except Exception as e:
                            return jsonify(str(e)), 400
                    else:
                        return jsonify({"message": "Unauthorized to update this media."}), 403  
                else:
                    return jsonify({"message": "Associated post not found."}), 400
            
            except Exception as e:
                return jsonify(str(e)), 400
        else:
            return jsonify({"message": "Media not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@media.route('/<int:media_id>', methods=['DELETE'])
@login_required
def delete_media(media_id):
    media_id = ObjectId(media_id)
    try:   
        media = db.media.find_one({"_id": media_id})
        if media:
            try: 
                post = db.Post.find_one({"_id": media['postID']})
                if post: 
                    author = post['authorID']
                    if current_user._id == author or current_user.userType == 'admin':
                        try: 
                            db.media.delete_one({"_id": media_id})
                            return jsonify({"message": "media deleted."}), 200
                        except Exception as e:
                            return jsonify(str(e)), 400
                    else:
                        return jsonify({"message": "Unauthorized to update this media."}), 403
                else:
                    try: 
                        db.media.delete_one({"_id": media_id})
                        return jsonify({"message": "media deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                    
            except Exception as e:
                return jsonify(str(e)), 400
        else:
            return jsonify({"message": "media not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

