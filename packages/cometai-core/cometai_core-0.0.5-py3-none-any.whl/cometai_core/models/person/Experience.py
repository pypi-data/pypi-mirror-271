from dataclasses import dataclass
from enum import Enum
from models.person.common import Position
from company import Company

@dataclass
class LocationTypeEnum(Enum):
    ON_SITE = "On-site"
    HYBRID = "Hybrid"
    REMOTE = "Remote"

@dataclass
class Location:
    location: str
    location_type: LocationTypeEnum

@dataclass
class EmploymentTypeEnum(Enum): 
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    SELF_EMPLOYED = "Self-employed"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    SEASONAL = "Seasonal"
    FREELANCE = "Freelance"
    APPRENTICESHIP = "Apprenticeship"

@dataclass
class Experience(Position):
    title: str
    employment_type: EmploymentTypeEnum
    company: Company
    location: Location
    currently_working: bool
    start_date: str
    end_date: str
    description: str
    profile_headline: str
    pass
