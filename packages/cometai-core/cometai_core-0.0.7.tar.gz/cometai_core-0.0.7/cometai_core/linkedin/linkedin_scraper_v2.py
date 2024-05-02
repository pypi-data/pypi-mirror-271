# Use site:linkedin.com

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from typing import Dict, List
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse, parse_qs



load_dotenv()

options = webdriver.ChromeOptions()
options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
driver = webdriver.Chrome(
        options=options
    )

def construct_main_query(options: Dict[str, List[str]]):
    query = "site:linkedin.com/in/"

    keywords = options.get("keywords")

    for keyword in keywords:
        query += f" AND {keyword}"

    return query
    

def main():
    driver.get('https://www.google.com/search?q=site:linkedin.com/in/ AND "python developer" AND "London"')
    input('Press ENTER to continue')

    linkedin_links = []
    
    page_source = driver.page_source
    
    soup = BeautifulSoup(page_source, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href', '')
        parsed_url = urlparse(href)
        
        # Check if the domain is 'linkedin.com' and the path starts with '/in/'
        if parsed_url.netloc == 'www.linkedin.com' and parsed_url.path.startswith('/in/'):
            # Ensure no query or fragment is specifying 'linkedin.com/in/' misleadingly
            if 'linkedin.com/in/' not in parse_qs(parsed_url.query).values() and 'linkedin.com/in/' not in parsed_url.fragment:
                linkedin_links.append(href)
    
    print("LINKEDIN LINKS", linkedin_links)

    for link in linkedin_links:
        driver.get(link)
        linkedin_page = BeautifulSoup(driver.page_source, 'html.parser')
        with open('linkedin.txt', 'a') as f:
            f.write(linkedin_page.prettify() + "\n\n\n")


if __name__ == "__main__":
    main()
