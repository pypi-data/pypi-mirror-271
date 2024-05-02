from dataclasses import dataclass
from typing import List

@dataclass
class Post:
    post_id: int
    links: List[str]
    content: str
    date: str
    interactions: int #TODO: could be more granular about the type of interaction here
    comments: int
    shares: int
    hashtags: List[str]
    pass