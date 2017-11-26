# Don't Blink Experiment

2017F 말과마음 프로젝트


## Used stacks

- Firebase for backend database
- S3 or GCS for file storage
- Application is deployed on Heroku
- Python 3.6.3
- Node.js 8.9.1

## Build Setup

### Setup python

Uses `virtualenvwrapper` for isolated python environment

```shell
$ mkvirtualenv dontblink
Installing..

(dontblink) $ pip install -r requirements.txt 
```

Before running you have to configure `config.py` with following keys:

- `SECRET_KEY`: created from `os.urandom(n)`
- `STAGE`: Arbitrary string for deployment stage. I uses `staging`, `prod`
- `FIREBASE_DATABASE_URL`: maybe `https://<project_id>.firebaseio.com`
- `FIREBASE_AUTH_DOMAIN`: maybe `<project_id>.firebaseapp.com`
- `FIREBASE_STORAGE_BUCKET`: maybe `<project_id>.appspot.com`
- `FIREBASE_API_KEY`: your API key from firebase console
- `FIREBASE_MESSAGE_SENDER_ID`: your sender ID from firebase console
- `FIREBASE_PROJECT_ID`: your project ID
- `FIREBASE_SERVICE_ACCOUNT_FILE`: your account json file path
- `DATA_SUMMARY`: "data/summary.json"
- `GCS_BUCKET`: your bucket
- `GCS_BUCKET_PREFIX`: your bucket prefix

and set environment variable `CONFIG_FILE` that points `config.py` path.

After setup, you can run local server at 8081 port by

``` shell
(dontblink) $ python app.py
```

### Setup Vue

``` shell
$ npm install  # install dependencies
$ npm run dev  # serve with hot reload at localhost:8080
$ npm run build  # build for production with minification
```

For detailed explanation on how things work, consult the [docs for vue-loader](http://vuejs.github.io/vue-loader).
