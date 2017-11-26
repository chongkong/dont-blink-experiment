import json

import flask
import pyrebase

import dontblink.model as model
import dontblink.controller as ctrl
import dontblink.api as api
import dontblink.config as config


def create_app():
    app = flask.Flask(__name__)
    config.load_config_from_env(app)

    firebase = pyrebase.initialize_app({
        "apiKey": app.config["FIREBASE_API_KEY"],
        "authDomain": app.config["FIREBASE_AUTH_DOMAIN"],
        "databaseURL": app.config["FIREBASE_DATABASE_URL"],
        "storageBucket": app.config["FIREBASE_STORAGE_BUCKET"],
        "serviceAccount": app.config["FIREBASE_SERVICE_ACCOUNT_FILE"]
    })
    db = firebase.database()

    with open(app.config["DATA_SUMMARY"], "r") as f:
        summary = json.load(f)
        docs = {doc["id"]: model.Document.from_dict(doc) for doc in summary["docs"]}
        audios = summary["audios"]

    @app.before_request
    def register_globals():
        flask.g.ctrl = ctrl.Controller(db, app.config["STAGE"], docs, audios,
                                       app.config["GCS_BUCKET"],
                                       app.config["GCS_BUCKET_PREFIX"])

    app.register_blueprint(api.bp)

    return app
