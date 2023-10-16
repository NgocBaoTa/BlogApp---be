from app.db import db

def create_notification_collection():
    notification_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["notiType", "postID", "userID", "status", "createAt"],
            "properties": {
                "notiType": {
                    "bsonType": "string",
                    "enum": [ "reply", "comment", "approve", "review", "decline"],
                    "description": "must be a string and is required"
                }, 
                "status": {
                    "bsonType": "string",
                    "enum": [ "read", "unread"],
                    "description": "must be a string and is required"
                },
                "postID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "userID": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                }, 
                "createAt": {
                    "bsonType": "date",
                    # "default": { "$toDate": "now" },
                    "description": "must be a date and is required"
                }
            }
        }
    }

    try:
        db.create_collection("Notification")
    except Exception as e:
        print(e)

    db.command("collMod", "Notification", validator=notification_validator)