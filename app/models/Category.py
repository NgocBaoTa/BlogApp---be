from app.db import db

def create_category_collection():
    category_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["categoryName", "createAt", "updateAt"],
            "properties": {
                "categoryName": {
                    "bsonType": "string",
                    "description": "must be a string and is required" 
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
        db.create_collection("Category")
    except Exception as e:
        print(e)

    db.command("collMod", "Category", validator=category_validator)

