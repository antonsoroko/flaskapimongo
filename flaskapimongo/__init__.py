from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo
from werkzeug.exceptions import default_exceptions
from pymongo import ASCENDING


def create_app():
    app = Flask(__name__)
    for code in default_exceptions:
        app.errorhandler(code)(_http_exceptions_handler)
    return app


def _http_exceptions_handler(error):
    message = {
            'status': error.code,
            'message': error.name,
            'description': error.description
    }
    return jsonify(message), error.code

app = create_app()
app.config.from_object('config')
mongo = PyMongo(app)
with app.app_context():
    mongo.db.activities.create_index([("uid", ASCENDING),("date", ASCENDING)])


from flaskapimongo import views
