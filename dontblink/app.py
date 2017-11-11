import flask
import pyrebase
import os


def create_app():
    app = flask.Flask(__name__)
    firebase = pyrebase.initialize_app({
        "apiKey": os.environ["FIREBASE_API_KEY"],
        "authDomain": os.environ["FIREBASE_AUTH_DOMAIN"],
        "databaseUrl": os.environ["FIREBASE_DATABASE_URL"],
        "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
        "serviceAccount": os.environ["FIREBASE_SERVICE_ACCOUNT_FILE"]
    })
    db = firebase.database()

    return app, firebase, db
