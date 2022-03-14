from flask_mongoengine import MongoEngine

db = MongoEngine()


class Song(db.Document):
    artist = db.StringField()
    title = db.StringField()
    difficulty = db.FloatField()
    level = db.IntField()
    released = db.DateTimeField()
    rating = db.IntField()
    meta = {
        "auto_create_index": False,
        "index_background": True,
        'indexes': [
            '$title',  # text index
            '$artist',  # text index
            'level',
        ]
    }
