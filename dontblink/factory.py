import os

import flask

import dontblink.api as api


def create_app():
    app = flask.Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(32)
    app.register_blueprint(api.bp)

    return app
