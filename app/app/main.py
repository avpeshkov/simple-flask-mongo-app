
from flask import Flask

from .models.song import db
from .core.utils import initial_data_import

app = Flask(__name__)

from .core import app_setup
from .api import *

# import initial data
initial_data_import()

app.config['MONGODB_SETTINGS'] = {
    'db': 'music_db',
    'host': 'mongodb',
    'port': 27017
}

db.init_app(app)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
