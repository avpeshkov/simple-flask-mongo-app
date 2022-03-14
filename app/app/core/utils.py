import json

from pymongo import MongoClient

from ..core.settings import MONGO_DB, MONGO_HOST, MONGO_PORT


def initial_data_import():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    if MONGO_DB not in client.list_database_names():
        db = client[MONGO_DB]
        collection_song = db['song']

        with open('./songs.json') as f:
            file_data = json.load(f)

        collection_song.insert_many(file_data)
    client.close()
