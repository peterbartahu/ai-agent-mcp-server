from dataclasses import dataclass
from typing import List

@dataclass
class StudyMaterial:
    topic: str
    summary: str
    key_points: List[str]
    questions: List[str]
    answers: List[str]