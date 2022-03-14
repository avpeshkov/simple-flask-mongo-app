import flask
from flask import jsonify

from ..api import api  # noqa
from ..main import app


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({'errorCode': 404, 'message': 'Route not found'}), 400


@app.errorhandler(Exception)
def exception_handler(error):
    return jsonify({'errorCode': 500, 'message': repr(error)}), 500
