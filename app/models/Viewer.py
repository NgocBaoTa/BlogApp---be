from app.db import db

def create_viewer_collection():
    viewer_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "email"],
            "properties": {
                "username": {
                    "bsonType": "string",
                    "description": "must be a string and is required" 
                },
                "email": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                }
            }
        }
    }

    try:
        db.create_collection("Viewer")
    except Exception as e:
        print(e)

    db.command("collMod", "Viewer", validator=viewer_validator)