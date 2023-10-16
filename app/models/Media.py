from app.db import db

def create_media_collection():
    media_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["postID", "mediaType", "mediaUrl", "size"],
            "properties": {
                "postID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "mediaType": {
                    "bsonType": "string",
                    "enum": ["image", "video"],
                    "description": "must be a string and is required" 
                }, 
                "mediaUrl": {
                    "bsonType": "string",
                    "description": "must be in Delta format and is required"
                },
                "size": {
                    "bsonType": "object",
                    "required": ["width", "height"],
                    "properties": {
                        "width": {
                            "bsonType": "int",
                            "minimum": 1,
                            "description": "must be an integer greater than 0"
                        },
                        "height": {
                            "bsonType": "int",
                            "minimum": 1,
                            "description": "must be an integer greater than 0"
                        }
                    }
                }
            }
        }
    }

    try:
        db.create_collection("Media")
    except Exception as e:
        print(e)

    db.command("collMod", "Media", validator=media_validator)