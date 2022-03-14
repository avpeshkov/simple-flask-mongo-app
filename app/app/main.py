
from flask import Flask

from .core.settings import MONGO_DB, MONGO_HOST, MONGO_PORT
from .models.song import db
from .core.utils import initial_data_import

app = Flask(__name__)

from .core import app_setup
from .api import *

# import initial data
initial_data_import()

app.config['MONGODB_SETTINGS'] = {
    'db': MONGO_DB,
    'host': MONGO_HOST,
    'port': MONGO_PORT
}

db.init_app(app)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
