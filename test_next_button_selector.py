from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import time

chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.propertyguru.com.sg/property-for-sale"
driver.get(url)
time.sleep(10)

while True:
    print("Current Page:", driver.current_url)
    print("Page Title:", driver.title)

    try:
        # Wait for the "next" button to be present
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[da-id='hui-pagination-btn-next']"))
        )

        # Scroll to the button to make it visible
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(1)  # Allow time for scroll effects/animations

        # Wait until clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[da-id='hui-pagination-btn-next']"))
        )

        try:
            next_button.click()
            print("Clicked next button\n")
        except ElementClickInterceptedException:
            print("Click intercepted. Retrying after scrolling again.")
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", next_button)
            time.sleep(2)
            next_button.click()

        time.sleep(5)

    except (NoSuchElementException, TimeoutException):
        print("No more pages or next button not found.")
        break

driver.quit()
