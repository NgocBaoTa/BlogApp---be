from app.db import db

def create_post_collection():
    post_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["categoryID", "authorID", "postTitle", "postContent", "postType", "comments", "createAt", "updateAt"],
            "properties": {
                "categoryID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "authorID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "postTitle": {
                    "bsonType": "string",
                    "description": "must be a string and is required" 
                }, 
                "postContent": {
                    "bsonType": "string",
                    "description": "must be in Delta format and is required",
                    "pattern": "^(?:{\"ops\":\\[.*\\]})$" 
                },
                "postType": {
                    "bsonType": "string",
                    "enum": [ "posted", "updated", "reviewing"],
                    "description": "must be a string and is required"
                },
                "comments": {
                    "bsonType": "array",
                    # "default": [],
                    "items": {
                        "bsonType": "objectId",
                        "description": "must be an objectId and is required"
                    }
                },
                "createAt": {
                    "bsonType": "date",
                    # "default": { "$toDate": "now" },
                    "description": "must be a date and is required"
                },
                "updateAt": {
                    "bsonType": "date",
                    # "default": { "$toDate": "now" },
                    "description": "must be a date and is required"
                }
            }
        }
    }

    try:
        db.create_collection("Post")
    except Exception as e:
        print(e)

    db.command("collMod", "Post", validator=post_validator)