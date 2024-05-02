from dataclasses import dataclass
from enum import Enum

@dataclass
class CompanyTypeOptionEnum(Enum):
    EDUCATIONAL = "Educational"
    GOVERNMENT_AGENCY = "Government Agency"
    NON_PROFIT = "Non Profit"
    PARTNERSHIP = "Partnership"
    PRIVATE = "Privately Held"
    PUBLIC = "Public Company"
    SELF_EMPLOYED = "Self Employed"
    SELF_OWNED = "Self Owned"



@dataclass
class CompanySizeOptionEnum(Enum):
    SMALL = "1-10 employees"
    MEDIUM = "11-50 employees"
    LARGE = "51-200 employees"
    VERY_LARGE = "201-500 employees"
    HUGE = "501-1000 employees"
    VERY_HUGE = "1001-5000 employees"
    MASSIVE = "5001-10000 employees"
    VERY_MASSIVE = "10001+ employees"

@dataclass
class Company:
    name: str
    linkedin_url: str
    tagline: str
    description: str
    industry: str
    company_size: CompanySizeOptionEnum
    company_type: CompanyTypeOptionEnum
    phone: str
    year_founded: int
    location: str #not sure what to do with this
    website: str #has to be scraped somehow
