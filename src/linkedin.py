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
        url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
        self.driver.get(url)
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

                            # Store job details in the dictionary
                            if companyName not in self.appliedJobs:
                                self.appliedJobs[companyName] = [(role_element,applied_date,location)]
                            else:
                                self.appliedJobs[companyName].append((role_element,applied_date,location))
                            if companyName not in self.companyNames:
                                self.companyNames[companyName] = originalCompName
                            self.numofJobs += 1
                        except Exception as e:
                            print("Exception in element processing: ", e)
                            self.exceptionOccured = True
                            break
                    try:
                        if self.exceptionOccured:
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
            for i,(role,date,loc) in enumerate(self.appliedJobs[companyName]):
                print("{}. Applied role: {}\t Applied time: {}\t Location: {}".format(i+1,role,date,loc))
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