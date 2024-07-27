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
import pickle
import os

class LinkedIn():
    """
    A class to interact with LinkedIn's applied jobs section.
    """

    def __init__(self):
        """
        Initialize the LinkedIn class by setting up the Chrome WebDriver and other attributes.
        """
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")  # Set the window size
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , options=chrome_options)
        self.companyNames = {}  # Dictionary to store company's name before parsing
        self.appliedJobs = {}   # Dictionary to store applied job details
        self.numofJobs = 0      # Counter for the number of jobs processed
        self.first = True       # Flag to indicate the first visit to the page
        self.exceptionOccured = False   # Flag to indicate if an exception occurred
    
    def get_updated_data(self):
        """
        Scrape applied job data from LinkedIn and store it in self.appliedJobs.

        The method performs the following:
        - Navigates to the LinkedIn applied jobs page.
        - Iterates through the job listings, extracting relevant information (company name, applied role, company's location, applied time).
        - Handles pagination by clicking "Next" button to load more applied jobs.
        - Uses exception handling to manage errors during scraping.
        """
        break_loop = False
        url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
        self.check_cookies(url,self.driver)
        while True:
            if url in self.driver.current_url:   # Check if we are on the correct page ("https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED")
                try:
                    if self.first:   # Implicitly wait during the first visit to get list of applied jobs
                        self.driver.implicitly_wait(10)
                        self.first = False

                    # Get all applied jobs showed on the current page (10 applied jobs per page)
                    elements = self.driver.find_elements(By.CSS_SELECTOR,"ul.reusable-search__entity-result-list li.reusable-search__result-container")

                    for ele in elements:
                        try:
                            # Extract job details
                            originalCompName = ele.find_element(By.CSS_SELECTOR,"div.entity-result__primary-subtitle.t-14.t-black.t-normal").text.strip()
                            companyName= originalCompName.lower()
                            role_element = ele.find_element(By.CSS_SELECTOR, "span.entity-result__title-text.t-16 a.app-aware-link").text.strip()
                            applied_date = self.get_applied_date(
                                ele.find_element(By.CSS_SELECTOR, "span.reusable-search-simple-insight__text.reusable-search-simple-insight__text--small").text.strip().lower()
                                )
                            location = ele.find_element(By.CSS_SELECTOR,"div.entity-result__secondary-subtitle.t-14.t-normal").text.strip()
                            job_link = self.get_href(ele.find_element(By.CSS_SELECTOR, "a.app-aware-link.scale-down").get_attribute('href').strip())

                            # Store job details in the dictionary
                            if companyName not in self.companyNames:
                                self.companyNames[companyName] = originalCompName
                            if companyName not in self.appliedJobs:
                                self.appliedJobs[companyName] = [(role_element,applied_date,location,job_link)]
                            else:
                                for elem in self.appliedJobs[companyName]:
                                    if job_link == elem[3]:
                                        break_loop = True   # Found the repetition. No need to scrape further
                                        break
                                else:
                                    self.appliedJobs[companyName].append((role_element,applied_date,location,job_link))
                            # self.numofJobs += 1
                            if break_loop: break
                        except Exception as e:
                            print("Exception in element processing: ", e)
                            self.exceptionOccured = True
                            break
                    try:
                        if self.exceptionOccured or break_loop:
                            break
                        # Click the "Next" button to load more jobs
                        button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.artdeco-pagination__button--next'))
                        )
                        if button.is_enabled():
                            self.driver.execute_script("arguments[0].click();", button)
                        else:
                            break   # If the "Next" button is no longer available, break the loop
                    except Exception as e:
                        print("Exception in clicking next button: ", e)
                        break
                except Exception as e:
                    print("General Exception: ", e)
                    break
        self.driver.quit()   # Close the browser

    def get_application_info(self, companyName):
        """
        Print the job application details for a specific company.

        Parameters:
        - companyName: The name of the company to retrieve job details for.
        """
        userInp = companyName
        companyName = userInp.lower()
        if companyName in self.appliedJobs:
            print("\nYou have applied to jobs at '{}' {} times.".format(self.companyNames[companyName],len(self.appliedJobs[companyName])))
            for i,(role,date,loc,link) in enumerate(self.appliedJobs[companyName]):
                print("{}. Applied role: {}\t Applied time: {}\t Location: {}\t Link: {}".format(i+1,role,date,loc,link))
            print()
        else:
            print("\nYou haven't applied to any jobs at the company '{}'.\n".format(userInp))
    
    def get_applied_date(self, application):
        """
        Extract and format the applied date from a string using regular expression. 
        The possible date formats from LinkedIn are as follows:
        1) Applied now
        2) Applied on Company Website now
        3) Applied (Xm, Xh, Xd, Xw, Xmo) ago
        4) Applied on Company Website (Xm, Xh, Xd, Xw, Xmo) ago

        Parameters:
        - application: The string containing the applied date.

        Returns:
        - A formatted date string or an empty string if no date is found.
        """
        res = re.findall(r"applied.*\b(\d+(?:m|h|d|w|mo|y)\sago)|(now)",application)
        if len(res) == 0: return ""
        else:
            for date in res[0]:
                if len(date) != 0: return date    
    
    def get_href(self,joblink):
        return re.findall(r"(.*)(?:\?.*)",joblink)[0]

    def check_cookies(self,url,driver):
        current_directory = os.getcwd() # Get the current working directory
        driver.get(url)
        if "linkedin_cookies.pkl" in os.listdir(current_directory):
            try:
                cookies = pickle.load(open("linkedin_cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
            except(pickle.UnpicklingError, EOFError):
                print("Cookies file is corrupted or empty. Need to recreate cookies.")
                self.create_new_cookies(driver,url)
        else:
            self.create_new_cookies(driver,url)

    def create_new_cookies(self, driver, url):
        user_input = input("Would you like to create new cookies for faster future logins? Type 'Y' to create new ones: ")
        if user_input == 'Y':
            print("Please log in manually from the opened browser.")
            while url not in driver.current_url: continue
            pickle.dump(self.driver.get_cookies(), open("linkedin_cookies.pkl", "wb"))
            print("Cookies has been created")
            print("New cookies saved successfully.\n")

    def get_applied_jobs(self):
        return self.appliedJobs
    
    def get_company_names(self):
        return self.companyNames
    
    def set_applied_jobs(self,data):
        prev_comp_name = None
        first = True
        for applic_hist in data:
            if first:   # To consume very first row (header)
                first = False
                continue
            if applic_hist[0] == None:
                comp_name = prev_comp_name
            else:
                comp_name = applic_hist[0].strip().lower()
                prev_comp_name = comp_name
            if comp_name not in self.appliedJobs:
                self.appliedJobs[comp_name] = [(applic_hist[5],applic_hist[3],applic_hist[9],applic_hist[13])]
            else:
                self.appliedJobs[comp_name].append((applic_hist[5],applic_hist[3],applic_hist[9],applic_hist[13]))
            if comp_name not in self.companyNames:
                self.companyNames[comp_name] = applic_hist[0].strip()