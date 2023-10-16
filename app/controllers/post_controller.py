from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from bson.objectid import ObjectId

post = Blueprint('post', __name__)

@post.route('/', methods=['GET'])
def get_posts():
    try:   
        posts = db.Post.find()
        return jsonify(posts), 200
    except Exception as e:
        return jsonify(str(e)), 400


@post.route('/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    try:   
        post = db.Post.find_one({"_id": ObjectId(post_id)})
        if post:
            return jsonify(post), 200
        else:
            return jsonify({"message": "Post not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@post.route('/', methods=["POST"])
@login_required
def create_post():
    pass


@post.route('/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    pass
    

@post.route('/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    pass


@post.route('/', methods=['GET'])
def search_post():
    search_text = request.args.get('searchText', '')

    if len(search_text) == 0:
        return None
    else:
        unique_posts = {}
        posts = list(db.Post.find({
            "postTitle": {"$regex": search_text, "$options": "i"}
        }))

        cates = list(db.Category.find({
            "categoryName": {"$regex": search_text, "$options": "i"}
        }))

        for post in posts:
            unique_posts[post["_id"]] = post

        for cate in cates:
            related_post = db.Post.find_one({
                "_id": cate["_id"]
            })
            if related_post:
                unique_posts[related_post["_id"]] = related_post
        
        unique_posts_list = list(unique_posts.values())

    if not posts:
        return jsonify({"message": "No post matches."}), 200

    return jsonify(unique_posts_list), 200
