import flask

from ..api import api  # noqa
from ..main import app


@app.route("/")
def index():
    # This could also be returning an index.html
    return flask.render_template("index.html")


