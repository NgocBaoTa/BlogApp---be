from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from bson.objectid import ObjectId

category = Blueprint('category', __name__)

@category.route('/', methods=['GET'])
def get_categories():
    try:   
        cates = db.Category.find()
        return jsonify(cates), 200
    except Exception as e:
        return jsonify(str(e)), 400


@category.route('/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    try:   
        cate = db.Category.find_one({"_id": ObjectId(category_id)})
        if cate:
            return jsonify(cate), 200
        else:
            return jsonify({"message": "Category not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@category.route('/', methods=["POST"])
@login_required
def create_category():
    if current_user.userType == "admin":
        try:
            inserted_id = db.Category.insert_one(request.json).inserted_id
            return jsonify(db.Category.find_one({"_id": ObjectId(inserted_id)})), 200 
        except Exception as e:
            return jsonify(str(e)), 400 
    else:
        return jsonify({"message": "Unauthorized to create category."}), 403  



@category.route('/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    if current_user.userType == 'admin':
        cate_id = ObjectId(category_id)
        try:   
            cate = db.Category.find_one({"_id": cate_id})
            if cate:
                try: 
                    db.Category.update_one({"_id": cate_id}, request.json)
                    return jsonify(db.Category.find_one({"_id": cate_id})), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Category not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to update this category."}), 403  
    

@category.route('/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    if current_user.userType == 'admin':
        cate_id = ObjectId(category_id)
        try:   
            cate = db.Category.find_one({"_id": cate_id})
            if cate:
                try: 
                    db.Category.delete_one({"_id": cate_id})
                    return jsonify({"message": "Category deleted."}), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Category not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to delete this category."}), 403  
