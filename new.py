from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")  # Set the window size

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , options=chrome_options)

url = "https://www.linkedin.com/my-items/saved-jobs/"
driver.get(url)

dic = {}

buttonClicked = False
addedElem = 0
first = True

while True:
    if url in driver.current_url:   # Check if the current url is indeed "https://www.linkedin.com/my-items/saved-jobs/..."
        try:
            if first:   # Implicitly wait at the first time to get list of applied jobs
                driver.implicitly_wait(10)
                first = False

            # Get all applied jobs showing on the current page (10 applied jobs per page)
            elements = driver.find_elements(By.CSS_SELECTOR,"ul.reusable-search__entity-result-list li.reusable-search__result-container")

            for i in elements:
                try:
                    companyName= i.find_element(By.CSS_SELECTOR,"div.entity-result__primary-subtitle.t-14.t-black.t-normal")
                    role_element = i.find_element(By.CSS_SELECTOR, "span.entity-result__title-text.t-16 a.app-aware-link")

                    if companyName.text not in dic:
                        dic[companyName.text] = [role_element.text]
                    else:
                        dic[companyName.text].append(role_element.text)
                    addedElem += 1
                except Exception as e:
                    print("Error: ", e)
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.artdeco-pagination__button--next'))
                )
                if button.is_enabled():
                    driver.execute_script("arguments[0].click();", button)
                    # time.sleep(3)
                else:
                    break   # If the "Next" button is no more available, break the loop
            except Exception as e:
                print("Error: ", e)
                
        except Exception as e:
            print("Error: ", e)

print(addedElem)
driver.quit()
