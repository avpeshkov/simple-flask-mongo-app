import json

from pymongo import MongoClient


def initial_data_import():
    client = MongoClient('mongodb', 27017)
    if 'music_db' not in client.list_database_names():
        db = client['music_db']
        collection_song = db['song']

        with open('./songs.json') as f:
            file_data = json.load(f)

        collection_song.insert_many(file_data)
    client.close()
