# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def start_browser():
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.propertyguru.com.sg/property-for-sale")
    time.sleep(5)  # Give time for page to load

    print("Page Title:", driver.title)
    print("Current URL:", driver.current_url)

    driver.quit()


if __name__ == "__main__":
    start_browser()
