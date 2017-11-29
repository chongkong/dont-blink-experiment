import random

import flask

import dontblink.model as model
import dontblink.util as util


class Controller(object):
    def __init__(self, db, stage, docs, audios, gcs_bucket, gcs_bucket_prefix):
        self._db = db
        self.stage = stage
        self.docs = docs
        self.audios = audios
        self.gcs_bucket = gcs_bucket
        self.gcs_bucket_prefix = gcs_bucket_prefix

    @property
    def db(self):
        return self._db.child(self.stage)

    @staticmethod
    def load_session():
        try:
            participant_dict = flask.session["participant"]
            participant = model.Participant.from_dict(participant_dict)
            return participant
        except KeyError:
            flask.abort(401)

    def _get_gcs_filename(self, filename):
        return f"https://storage.googleapis.com/{self.gcs_bucket}" \
               f"/{self.gcs_bucket_prefix}{filename}"

    @staticmethod
    def _generate_combs(k):
        pops = [("full", False), ("full", True), ("blink", False), ("blink", True)]
        combs = []
        while k >= 4:
            combs += random.sample(pops, 4)
            k -= 4
        combs += random.sample(pops, k)
        return combs

    def _compose_sections(self):
        doc_ids = random.sample(list(self.docs.keys()), k=len(self.docs))
        combs = self._generate_combs(len(self.docs))
        sections = []
        audios = random.sample(self.audios, len([_ for _, use_audio in combs if use_audio]))
        for i, (disp_type, use_audio) in enumerate(combs):
            audio_file = None if not use_audio else self._get_gcs_filename(audios.pop())
            sections.append(model.Section(doc_id=doc_ids[i], disp_type=disp_type,
                                          answers=[], audio_file=audio_file,
                                          completed=False, completed_at=None))
        return sections

    def register_participant(self, name, age, gender, department, contact):
        participant = model.Participant(id=util.random_string(12), name=name, age=age,
                                        gender=gender, department=department,
                                        contact=contact)
        exp = model.Experiment(id=util.random_string(12),
                               sections=self._compose_sections(),
                               started_at=util.now())
        participant.experiment_id = exp.id
        exp.participant_id = participant.id
        self.db.child("Experiments").child(exp.id).set(exp)
        self.db.child("Participants").child(participant.id).set(participant)
        flask.session["participant"] = participant
        return participant

    @staticmethod
    def _remove_answer(doc: dict):
        doc = model.Document.from_dict(doc)
        for q in doc.questions:
            q.pop("answer")
        return doc

    def get_experiment(self, exp_id):
        resp = self.db.child("Experiments").child(exp_id).get()
        exp = model.Experiment.from_dict(resp.val())
        for sec in exp.sections:
            doc_id = sec.pop("doc_id")
            sec["doc"] = self._remove_answer(self.docs[doc_id])
        return exp

    def record_answer(self, exp_id, sec_idx, ans_idx, choice, response_time):
        resp = self.db.child(f"Experiments/{exp_id}/sections/{sec_idx}").get()
        section = model.Section.from_dict(resp.val())
        doc = self.docs[section.doc_id]
        patch = {
            f"answers/{ans_idx}/choice": choice,
            f"answers/{ans_idx}/correct": doc.questions[ans_idx].answer == choice,
            f"answers/{ans_idx}/response_time": response_time,
        }
        if ans_idx == len(doc.questions) - 1:
            patch["completed"] = True
            patch["completed_at"] = util.now()

        self.db.child(f"Experiments/{exp_id}/sections/{sec_idx}").update(patch)

    @staticmethod
    def logout():
        flask.session.clear()

    def get_all_experiments(self, id_filter=None):
        resp = self.db.child("Experiments").get()
        experiments = [model.Experiment.from_dict(exp)
                       for exp_id, exp in resp.val().items()
                       if id_filter is None or exp_id.startswith(id_filter)]
        for exp in experiments:
            exp.completed = all(sec.completed for sec in exp.sections)
            exp.num_logs = sum([len(sec.answers) for sec in exp.sections])
        return sorted(experiments, key=lambda e: e.started_at, reverse=True)

    def list_experiments_for_csv(self, show_all=False):
        experiments = self.get_all_experiments()
        return [piece for exp in experiments
                for piece in self._parse_experiment(exp)
                if show_all or exp.completed]

    @staticmethod
    def _parse_experiment(exp):
        for sec_idx, sec in enumerate(exp.sections):
            for ans_idx, ans in enumerate(sec.answers):
                yield (exp.id, str(sec_idx + 1), sec.doc_id, str(ans_idx + 1),
                       str(ans.choice), str(ans.correct).lower(),
                       str(ans.response_time))  # Typo compensation
