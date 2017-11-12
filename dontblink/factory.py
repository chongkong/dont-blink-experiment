import os

import flask


def create_app():
    app = flask.Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(32)

    return app
