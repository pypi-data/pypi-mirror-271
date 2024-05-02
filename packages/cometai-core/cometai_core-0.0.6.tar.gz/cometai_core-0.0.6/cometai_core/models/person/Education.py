from dataclasses import dataclass
from models.person.common import Position


@dataclass
class Education(Position):
    school: str
    degree: str
    field_of_study: str
    grade: str
    activities_and_societies: str
