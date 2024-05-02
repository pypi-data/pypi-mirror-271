from dataclasses import dataclass
from typing import List
from Person import Person
from company import Company

@dataclass
class InterestInfo: #TODO: make objects for all of these
    top_voices: List[Person]
    companies: List[Company]
    groups: List[str]
    newsletters: List[str]
    schools: List[str]
    pass