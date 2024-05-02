from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import traceback
import time
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

class Browser:
    def __init__(self,username,password):
        start = time.time()
        chrome_options = Options(
        )
        chrome_options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
        
        prefs = {
            "download_restrictions": 3,
        }
        chrome_options.add_experimental_option(
            "prefs", prefs
        )
        chrome_options.page_load_strategy = 'none'  # Load pages without waiting for all resources
        chrome_options.add_argument("--disable-javascript")
        driver = webdriver.Chrome(options = chrome_options)
        
        self.driver=driver          
        self.username=username
        self.password=password
        self.login()
        end = time.time()
        print(f"Time taken to login: {end - start} seconds")

    def get_driver(self):
        return self.driver
        
    def login(self):
        self.driver.get('https://www.linkedin.com/sales/login')

        try:
            print("trying to load cookie if available")
            self.loadcookie()
            return
        except:
            print("some problem with cookie or its not available")
            traceback.print_exc()
            

        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "authentication-iframe")))

        username = self.driver.find_element(By.ID, 'username')
        username.send_keys(os.environ.get('LINKED_IN_LOGIN_EMAIL'))

        password = self.driver.find_element(By.ID, 'password')
        password.send_keys(os.environ.get('LINKED_IN_LOGIN_PASSWORD'))
        password.send_keys(Keys.RETURN)


        self.savecookies()

    def loadcookie(self):
        print("loading cookie")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        print(cookies)
        self.driver.add_cookie(cookies)
        print('loaded cookie')


    def savecookies(self):
        print("saving cookie")
        time.sleep(10)
        cookies=self.driver.get_cookies()
        for cookie in cookies:
            if(cookie['name']=='li_at'):
                cookie['domain']='.linkedin.com'
                x={
                'name': 'li_at',
                'value': cookie['value'],
                'domain': '.linkedin.com'
                }
                break
        pickle.dump(x , open("cookies.pkl","wb"))
        print('cookies saved')