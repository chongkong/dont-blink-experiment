import json
import random

import flask

import dontblink.model as model
import dontblink.g as g
import dontblink.util as util


def assert_experiment(exp_id):
    if "user" not in flask.session:
        flask.abort(403)
    user = model.Participant.from_dict(json.loads(flask.session["user"]))
    if user.experiment_id != exp_id:
        flask.abort(403)


def _compose_sections():
    doc_ids = random.sample(list(g.docs.keys()), k=4)
    combs = [("text", False), ("text", True), ("dontblink", False), ("dontblink", True)]
    # random.shuffle(combs)
    sections = []
    audios = random.sample(g.audios, 2)
    for i, (disp_type, use_audio) in enumerate(combs):
        audio_file = None if use_audio else audios.pop()
        sections.append(model.Section(doc_id=doc_ids[i], disp_type=disp_type, answers=[],
                                      audio_file=audio_file, completed=False,
                                      completed_at=None))
    return sections


def register_participant(name, age, gender, department, contact):
    user = model.Participant(id=util.random_string(12), name=name, age=age,
                             gender=gender, department=department, contact=contact)
    exp = model.Experiment(id=util.random_string(12), sections=_compose_sections(),
                           started_at=util.now())
    user.experiment_id = exp.id
    exp.participant_id = user.id
    g.db.child("Experiments").child(exp.id).set(exp)
    g.db.child("Participants").child(user.id).set(user)
    return user


def _remove_answer(doc: dict):
    doc = model.Document.from_dict(doc)
    for q in doc.questions:
        q.pop("answer")
    return doc


def get_experiment(exp_id):
    resp = g.db.child("Experiments").child(exp_id).get()
    exp = model.Experiment.from_dict(resp.val())
    for sec in exp.sections:
        doc_id = sec.pop("doc_id")
        sec["doc"] = _remove_answer(g.docs[doc_id])
    return exp


def record_answer(exp_id, sec_idx, ans_idx, choice, response_time):
    resp = g.db.child(f"Experiments/{exp_id}/sections/{sec_idx}").get()
    section = model.Section.from_dict(resp.val())
    doc = g.docs[section.doc_id]
    patch = {
        f"answers/{ans_idx}/choice": choice,
        f"answers/{ans_idx}/correct": doc.questions[ans_idx].answer == choice,
        f"answers/{ans_idx}/respone_time": response_time,
    }
    if ans_idx == len(doc.questions) - 1:
        patch["completed"] = True
        patch["completed_at"] = util.now()

    g.db.child(f"Experiments/{exp_id}/sections/{sec_idx}").update(patch)


def authenticate_admin(id, password):
    pass


def view_stats():
    pass
