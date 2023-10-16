from app.db import db

def create_user_collection():
    user_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "email", "password", "userType", "avatar", "description", "posts", "notifications", "createAt", "updateAt"],
            "properties": {
                "username": {
                    "bsonType": "string",
                    "description": "must be an string and is required"
                },
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "description": "must be an string and is required"
                },
                "password": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }, 
                "userType": {
                    "bsonType": "string",
                    "enum": [ "user", "admin"],
                    "description": "must be a string and is required"
                }, 
                "avatar": {
                    "bsonType": ["null", "string"],
                    "description": "can be a string or null"
                },
                "description": {
                    "bsonType": ["null", "string"],
                    "description": "can be a string or null"
                },
                "notifications": {
                    "bsonType": "array",
                    # "default": [],
                    "items": {
                        "bsonType": "objectId",
                        "description": "must be an objectId"
                    }
                },
                "posts": {
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
        db.create_collection("User")
    except Exception as e:
        print(e)

    db.command("collMod", "User", validator=user_validator)