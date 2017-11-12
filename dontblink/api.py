import flask

bp = flask.Blueprint("api", __name__, url_prefix="/api")


@bp.route("/participants", methods=["POST"])
def register_participant():
    name = flask.request.args["name"]
    pass


@bp.route("/experiments/<int:id>")
def get_experiment(id):
    pass


@bp.route("/experiments/<int:exp_id>/<int:sess_id>/<int:ans_idx>")
def record_answer(exp_id, sess_id, ans_idx):
    pass


@bp.route("/data/<path:path>")
def get_file(path):
    pass


@bp.route("/login")
def authenticate_admin():
    pass


@bp.route("/stats")
def view_stats():
    pass
