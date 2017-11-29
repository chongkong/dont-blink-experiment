import typing


ID_TYPE = str


def _create_dict_property(key):
    def key_get(self):
        return self.get(key)

    def key_set(self, val):
        self[key] = val

    def key_del(self):
        self.pop(key)

    return property(key_get, key_set, key_del)


class _DictModel(type):
    def __new__(mcs, name, bases, attrs):
        assert dict in bases
        model = super().__new__(mcs, name, bases, attrs)
        for key in attrs["__annotations__"].keys():
            setattr(model, key, _create_dict_property(key))
        return model


class Participant(dict, metaclass=_DictModel):
    id: ID_TYPE
    experiment_id: ID_TYPE
    name: str
    age: int
    gender: str
    department: str
    contact: str

    def __init__(self, **kwargs):
        super(Participant, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, dic):
        return cls(**dic)


class Question(dict, metaclass=_DictModel):
    statement: str
    choices: typing.List[str]
    answer: int

    def __init__(self, **kwargs):
        super(Question, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, dic):
        return cls(**dic)


class Document(dict, metaclass=_DictModel):
    id: ID_TYPE
    content: str
    duration: float
    sync: typing.List[float]
    questions: typing.List[Question]

    def __init__(self, **kwargs):
        super(Document, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, dic):
        questions = dic["questions"]
        obj = cls(**dic)
        obj.questions = [Question.from_dict(d) for d in questions]
        return obj


class Answer(dict, metaclass=_DictModel):
    choice: str
    correct: bool
    response_time: float

    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, dic):
        if "respone_time" in dic:
            dic["response_time"] = dic.pop("respone_time")
        return cls(**dic)


class Section(dict, metaclass=_DictModel):
    doc_id: ID_TYPE
    disp_type: str
    audio_file: str
    answers: typing.List[Answer]
    completed: bool
    completed_at: str

    def __init__(self, **kwargs):
        super(Section, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, dic):
        answers = dic.get("answers", [])
        obj = cls(**dic)
        obj.answers = [Answer.from_dict(d) for d in answers]
        return obj


class Experiment(dict, metaclass=_DictModel):
    id: ID_TYPE
    participant_id: ID_TYPE
    sections: typing.List[Section]
    started_at: str

    def __init__(self, **kwargs):
        super(Experiment, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, dic):
        sections = dic["sections"]
        obj = cls(**dic)
        obj.sections = [Section.from_dict(d) for d in sections]
        return obj
