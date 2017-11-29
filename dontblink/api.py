import json

import flask

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

    participant = flask.g.ctrl.register_participant(name, age, gender, department, contact)
    return flask.jsonify(participant)


@bp.route("/experiment")
def get_experiment():
    participant = flask.g.ctrl.load_session()
    return flask.jsonify(flask.g.ctrl.get_experiment(participant.experiment_id))


@bp.route("/experiment/<int:sec_idx>/<int:ans_idx>", methods=["POST"])
def record_answer(sec_idx, ans_idx):
    participant = flask.g.ctrl.load_session()
    try:
        args = flask.request.get_json()
        choice = int(args["choice"])
        rt = float(args["responseTime"])
    except KeyError:
        return flask.abort(401)

    flask.g.ctrl.record_answer(participant.experiment_id, sec_idx, ans_idx, choice, rt)
    return "", 204


@bp.route("/logout", methods=["POST"])
def logout():
    flask.g.ctrl.logout()
    return "", 204


@bp.route("/result")
def view_result():
    id_filter = flask.request.args.get("filter")
    experiments = flask.g.ctrl.get_all_experiments(id_filter)
    return flask.render_template("result.html", experiments=experiments)


@bp.route("/result/csv")
def download_result_csv():
    exps = flask.g.ctrl.list_experiments_for_csv()
    columns = ",".join(["실험번호", "섹션", "문서", "표시", "오디오", "문항", "답안",
                        "정답", "반응시간"])
    csv = "\n".join([columns] + [",".join(item) for item in exps])
    return flask.Response(
      csv, mimetype="text/csv", headers={
        "Content-Disposition": "attachment; filename=ExperimentResult.csv"
      })
