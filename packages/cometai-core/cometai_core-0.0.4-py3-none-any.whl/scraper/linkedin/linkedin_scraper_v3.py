from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from typing import Dict, List
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse, parse_qs
import os
import urllib.parse
import time
from bs4 import BeautifulSoup
from .Browser import Browser
from requests_html import HTMLSession
import pickle
from .utils import parse_profile_page

BASE_URL="https://www.linkedin.com"

load_dotenv()

SCROLL_PAUSE_TIME = 0.5
SCROLL_INCREMENT = 500



# options = webdriver.ChromeOptions()
# options.add_experimental_option(
#         "prefs", {
#             # block image loading
#             "profile.managed_default_content_settings.images": 2,
#         }
#     )

# driver = webdriver.Chrome(
#         options=options
#     )


class LinkedInScraper:
    def __init__(self, username: str, password: str):
        self.browser = Browser(username, password)
        self.driver = self.browser.get_driver()

    def scroll_to_bottom_of_element(driver: ChromiumDriver, element_id: str):
        # Find the element
        scrollable_element =  WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, element_id))
    )

        # Get the initial scroll height
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

        while True:
            # Scroll down within the element
            driver.execute_script(f"arguments[0].scrollTop += {SCROLL_INCREMENT};", scrollable_element)

            # Wait for the page to load
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
            print("New Height:", new_height)  # Print the current bottom of the element

            # Check if the bottom has been reached
            if new_height == last_height:
                break
            last_height = new_height
            
    def login():
        pass

    def scrape_profile_page():
        pass

    def scrape_lead_search_page():
        pass

    def get_profiles(self, search_str: str):

        start = time.time()

        browser = self.browser

        driver = browser.get_driver()
    
        # # After successfully logging in
        # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

        # # At the start of a new session, before navigating to the login page
        # cookies = pickle.load(open("cookies.pkl", "rb"))
        # for cookie in cookies:
        #     driver.add_cookie(cookie)

        search_url = f'{BASE_URL}/sales/search/people'
        params = {
        'query': f'(spellCorrectionEnabled:true,keywords:{search_str})'
        }

        encoded_params = urllib.parse.urlencode(params)

        full_search_url = f"{search_url}?{encoded_params}"


        driver.get(full_search_url)

        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'search-results-container')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all 'a' tags with class 'ember-view'
        with open('search.html', 'w') as f:
            f.write(str(soup))

        divs = soup.find_all('div', attrs={'data-scroll-into-view': True})

        # List to hold the extracted URNs
        urns = []

        for div in divs:
            # Extract the value of 'data-scroll-into-view'
            urn = div['data-scroll-into-view']
            # Assuming the format always includes the URN inside parentheses
            urn = urn.split('(')[1].rstrip(')')
            urns.append(urn)

        results = []
        profiles = []


        for urn in urns:
            driver.get(f"{BASE_URL}/sales/lead/{urn}")
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'content-main')))
            profile_soup = BeautifulSoup(driver.page_source, 'html.parser')
            profile = parse_profile_page(profile_soup)
            with open('profiles.html', 'a') as f:
                f.write(profile_soup.prettify() + "\n\n\n")
            results += profile_soup
            profiles.append(profile)
        

        end = time.time()
        print(f"Time taken: {end - start} seconds")

        return profiles


        # for url in profile_urls:
        #     driver.get(url)
        #     WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'profile-content')))

        #     profile_soup = BeautifulSoup(driver.page_source, 'html.parser')
        #     profile_urls_html.append(profile_soup)

        # with open('profiles.html', 'w') as f:
        #     f.write(str(profile_urls_html))



        # scroll_to_bottom_of_element(driver, 'search-results-container')

        # try:
        #     anchors = WebDriverWait(driver, 10).until(
        #         EC.presence_of_all_elements_located((By.XPATH, "//a[@data-control-name='view_lead_panel_via_search_lead_name']"))
        #     )
        #     for anchor in anchors:
        #         print(f"Link: {anchor.get_attribute('href')}, Text: {anchor.text}")
        # except Exception as e:
        #     print(f"An error occurred: {e}")

        # print("ANCHORS", anchors)






        # driver.find_element(By.CSS_SELECTOR, 'global-typeahead__input-label').click() #search bar
        
        # driver.switch_to.active_element.send_keys(args + Keys.RETURN)  # Adding RETURN for demonstration


        input("Press ENTER to continue")



if __name__ == '__main__':
    scraper = LinkedInScraper(os.environ.get('LINKED_IN_LOGIN_EMAIL'), os.environ.get('LINKED_IN_LOGIN_PASSWORD'))
    profiles = scraper.get_profiles('python developer')
    print("PROFILES", profiles)

