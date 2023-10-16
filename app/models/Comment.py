from app.db import db

def create_comment_collection():
    comment_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["userID", "postID", "message", "replies", "createAt", "updateAt"],
            "properties": {
                "userID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "postID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "message": {
                    "bsonType": "string",
                    "description": "must be a string and is required" 
                }, 
                "replies": {
                    "bsonType": "array",
                    # "default": [],
                    "items": {
                        "bsonType": "objectId",
                        "description": "must be an objectId"
                    }
                },
                "createAt": {
                    "bsonType": "date",
                    # "default": { "$toDate": "now" },
                    "description": "must be a date"
                },
                "updateAt": {
                    "bsonType": "date",
                    # "default": { "$toDate": "now" },
                    "description": "must be a date"
                }
            }
        }
    }

    try:
        db.create_collection("Comment")
    except Exception as e:
        print(e)

    db.command("collMod", "Comment", validator=comment_validator)