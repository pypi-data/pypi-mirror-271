from dataclasses import dataclass
from Experience import Experience
from typing import List
from Education import Education
from Post import Post
from InterestInfo import InterestInfo

@dataclass
class PersonalLocation:
    city: str
    postal_code: str
    country: str

@dataclass
class Name:
    first: str
    last: str
    addiional: str

@dataclass
class BasicInfo:
    name: Name
    headline: str
    # current_position: Experience #Not really sure what this dropdown is pulling from


@dataclass
class Person:
    about: str
    basic: BasicInfo
    industry: str
    education: str
    location: PersonalLocation
    contact_info: str
    interest_info: InterestInfo
    posts: List[Post]
    experiences: List[Experience]

