from typing import NamedTuple, List


class Participant(NamedTuple):
    id: int
    name: str
    age: int
    gender: str
    department: str
    contact: str


class Question(NamedTuple):
    problem: str
    candidates: List[str]
    answer: str


class Document(NamedTuple):
    id: int
    content: str
    audio_file: str
    duration: float
    sync: List[float]
    questions: List[Question]


class Answer(NamedTuple):
    choice: str
    correct: bool
    response_time: float


class Section(NamedTuple):
    doc_id: int
    participant_id: int
    disp_type: str
    answers: List[Answer]
    completed: bool
    completed_at: str


class Experiment(NamedTuple):
    sections: List[Section]
    started_at: str
