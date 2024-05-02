from bs4 import BeautifulSoup
import re
from models import Person, BasicInfo, PersonalLocation, Experience, Post
from types import List


def parse_experience_entry(experience_entry: BeautifulSoup) -> Experience:

    if (job_title_tag:= experience_entry.find('h3', {'data-anonymize': 'job-title'})) is not None:
        job_title = job_title_tag.get_text(strip=True)
    else:
        job_title = ""

    if (company_name_tag := experience_entry.find('span', {'data-anonymize': 'company-name'})) is not None:
        company_name = company_name_tag.get_text(strip=True)
    else:
        company_name = ""
    
    #TODO: Find a way to get company_link

    if (person_blurb_tag := experience_entry.find('div', {'data-anonymize': 'person-blurb'})) is not None:
        person_blurb = person_blurb_tag.get_text(strip=True)
    else:
        person_blurb = ""

    # Extracting time period
    if (time_period_tag := experience_entry.find('span', {'data-anonymize': 'time-period'})) is not None:
        time_period = time_period_tag.get_text(strip=True)
    else:
        time_period = ""

    if (location_tag := experience_entry.find('span', {'data-anonymize': 'location'})) is not None:
        location = location_tag.get_text(strip=True)
    else:
        location = ""

    if (job_description_tag := experience_entry.find('div', {'data-anonymize': 'job-description'})) is not None:
        job_description = job_description_tag.get_text(strip=True)
    else:
        job_description = ""

    # Append to experiences list
    experience = Experience(job_title, company_name, time_period, location, person_blurb, job_description)

    return experience


def parse_profile_page(soup: BeautifulSoup) -> Person:

    # Extracting specific information
    # Name and additional info (e.g., professional titles)
    if (name_tag := soup.find('p', {'data-anonymize': 'person-name'})) is not None:
        name = name_tag.get_text(strip=True)
    else: 
        name = ""

    if (headline_tag := soup.find('p', {'data-anonymize': 'headline'})) is not None:
        headline = headline_tag.get_text(strip=True)
    else:
        headline = ""

    experience_lst = soup.find("div", {"id": "experience-section"}).find('ul')
    experiences: List[Experience] = []

    for li in experience_lst.find_all('li'):
        experiences.append(parse_experience_entry(li))
    
    # pattern = re.compile(r'.*\b_current-role-item_\b.*')  # ensures the class name contains '_current-role-item_'
    # role_items = soup.find_all('p', class_=pattern)

    # Location
    if (location_tag := soup.select_one('EzlYHbcfhKpSiteJvPPqZaMLmlAeyUkcBi')) is not None:
        location_text = location_tag.get_text(strip=True)
        city, country = location_text.split(', ')[0], location_text.split(', ')[-1]
    else:
        location_text = ""
        city, country = "", ""
    

    # Contact Information
    # This might be more complex depending on how it's structured in the HTML. This is an example:
    contact_info = "Not directly available"

    # Interest information
    # This also needs to be extracted based on specific identifiers or classes in the HTML
    interest_info = "Needs specific identifiers"

    # Output
    print(f"Name: {name}")
    print(f"City: {city}, Country: {country}")
    print("Experiences:", experiences)

    basic_info = BasicInfo(name, headline)
    personal_location = PersonalLocation(city, "", country)

    profile = Person("", basic_info, "", "", personal_location, "", "", [], experiences)

    return profile
