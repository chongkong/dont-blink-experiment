import os
import json
import typing

import pyrebase

import dontblink.model as model


firebase = pyrebase.initialize_app({
    "apiKey": os.environ["FIREBASE_API_KEY"],
    "authDomain": os.environ["FIREBASE_AUTH_DOMAIN"],
    "databaseURL": os.environ["FIREBASE_DATABASE_URL"],
    "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
    "serviceAccount": os.environ["FIREBASE_SERVICE_ACCOUNT_FILE"]
})
db = firebase.database().child("prod" if os.environ.get("IS_PROD") else "test")

with open("data/summary.json", "r") as f:
    _data = json.load(f)
docs: typing.Dict[str, model.Document] = \
    {doc["id"]: model.Document.from_dict(doc) for doc in _data["docs"]}
audios = _data["audios"]
