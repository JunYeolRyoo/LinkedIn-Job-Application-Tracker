from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time

class LinkedIn():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")  # Set the window size
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , options=chrome_options)
        self.appliedJobs = {}
        self.numofJobs = 0
        self.first = True
    
    def get_updated_data(self):
        url = "https://www.linkedin.com/my-items/saved-jobs/"
        self.driver.get(url)
        while True:
            if url in self.driver.current_url:   # Check if the current url is indeed "https://www.linkedin.com/my-items/saved-jobs/..."
                if self.first:
                    curT = time.time()
                try:
                    if self.first:   # Implicitly wait at the first time to get list of applied jobs
                        self.driver.implicitly_wait(10)
                        self.first = False

                    # Get all applied jobs showing on the current page (10 applied jobs per page)
                    elements = self.driver.find_elements(By.CSS_SELECTOR,"ul.reusable-search__entity-result-list li.reusable-search__result-container")

                    for ele in elements:
                        try:
                            companyName= ele.find_element(By.CSS_SELECTOR,"div.entity-result__primary-subtitle.t-14.t-black.t-normal").text.strip().lower()
                            role_element = ele.find_element(By.CSS_SELECTOR, "span.entity-result__title-text.t-16 a.app-aware-link").text.strip().lower()
                            applied_date = ele.find_element(By.CSS_SELECTOR, "span.reusable-search-simple-insight__text.reusable-search-simple-insight__text--small").text.strip().lower()
                            # print(applied_date)
                            if companyName not in self.appliedJobs:
                                self.appliedJobs[companyName] = [role_element]
                            else:
                                self.appliedJobs[companyName].append(role_element)
                            self.numofJobs += 1
                        except Exception as e:
                            print("Error: ", e)
                    try:
                        button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.artdeco-pagination__button--next'))
                        )
                        if button.is_enabled():
                            self.driver.execute_script("arguments[0].click();", button)
                        else:
                            break   # If the "Next" button is no more available, break the loop
                    except Exception as e:
                        print("Error: ", e)
                        
                except Exception as e:
                    print("Error: ", e)
        endT = time.time()
        print(endT-curT)
        print(self.numofJobs)

    def get_application_info(self, companyName):
        if companyName in self.appliedJobs:
            print("\nYou have applied to jobs at {} {} times.".format(companyName,len(self.appliedJobs[companyName])))
            for i,role in enumerate(self.appliedJobs[companyName]):
                print("{}. Applied role: {}\t".format(i+1,role))
            print()
        else:
            print("\nYou haven't applied to any jobs at the company {}.\n".format(companyName))
    
    def get_applied_date(self, application):
        ## formats:
        ## Applied (Xmo, Xw, Xd) ago, Applied on Company Website (Xmo, Xw, Xd) ago.
        print(re.findall(r"applied.*\b(\d+(?:d|w|mo|y)\sago)",applied_date))
        
