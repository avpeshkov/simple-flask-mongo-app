from datetime import datetime

import mongoengine
import pytest
from flask import Flask

from flask_mongoengine import MongoEngine

from ..models.song import db


@pytest.fixture()
def app():
    mongoengine.connection.disconnect_all()
    from ..core import app_setup
    from ..api import api

    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'flask_mongoengine_test_db',
        'host': 'mongodb',
        'port': 27017
    }
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        yield app

    mongoengine.connection.disconnect_all()


@pytest.fixture()
def song(db):
    class Song(db.Document):
        artist = mongoengine.StringField()
        title = mongoengine.StringField()
        difficulty = mongoengine.FloatField()
        level = mongoengine.IntField()
        released = mongoengine.DateTimeField(default=datetime.utcnow)
        rating = mongoengine.IntField()

    return Song


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

if __name__ == '__main__':
    app.run()