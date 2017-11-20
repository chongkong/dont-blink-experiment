import json

import flask

import dontblink.controller as ctrl

bp = flask.Blueprint("api", __name__, url_prefix="/api")


@bp.route("/participants", methods=["POST"])
def register_participant():
    try:
        args = flask.request.get_json()
        name = args["name"]
        age = int(args["age"])
        gender = args["gender"]
        department = args["department"]
        contact = args["contact"]
    except KeyError:
        return flask.abort(401)

    user = ctrl.register_participant(name, age, gender, department, contact)
    flask.session["user"] = json.dumps(user)
    return flask.jsonify(user)


@bp.route("/experiments/<int:exp_id>")
def get_experiment(exp_id):
    ctrl.assert_experiment(exp_id)
    return flask.jsonify(ctrl.get_experiment(exp_id))


@bp.route("/experiments/<int:exp_id>/<int:sec_idx>/<int:ans_idx>")
def record_answer(exp_id, sec_idx, ans_idx):
    ctrl.assert_experiment(exp_id)
    try:
        args = flask.request.get_json()
        choice = args["choice"]
        rt = args["rt"]
    except KeyError:
        return flask.abort(401)

    record_answer(exp_id, sec_idx, ans_idx, choice, rt)
    return "", 204


@bp.route("/data/<path:path>")
def get_file(path):
    pass  # flask.send_from_directory("")


@bp.route("/login")
def authenticate_admin():
    pass


@bp.route("/stats")
def view_stats():
    pass
