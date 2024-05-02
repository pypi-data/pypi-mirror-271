#TODO: add Skill and Media classes

from dataclasses import dataclass


@dataclass
class Position:
    start_date: str
    end_date: str
    description: str

