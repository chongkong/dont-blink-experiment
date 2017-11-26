import os


def load_config_from_env(app):
    keys = [
        "SECRET_KEY",
        "STAGE",
        "FIREBASE_DATABASE_URL",
        "FIREBASE_AUTH_DOMAIN",
        "FIREBASE_STORAGE_BUCKET",
        "FIREBASE_API_KEY",
        "FIREBASE_MESSAGE_SENDER_ID",
        "FIREBASE_PROJECT_ID",
        "FIREBASE_SERVICE_ACCOUNT_FILE",
        "DATA_SUMMARY",
        "GCS_BUCKET",
        "GCS_BUCKET_PREFIX",
    ]
    for key in keys:
        app.config.setdefault(key, os.environ.get(key))
