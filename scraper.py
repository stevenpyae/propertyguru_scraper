# Import necessary modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from html_parser import parse_listings  # We'll define this function next

class RealEstateScraper:
    def __init__(self):
        # Setup options for Chrome (headless = no browser window opens)
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Use the latest headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the Chrome driver with the configured options
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

        # Base URL to scrape from
        self.base_url = "https://www.propertyguru.com.sg/property-for-sale"

        # List to store all listings
        self.results = []

    def run(self):
        # Open the starting URL
        self.driver.get(self.base_url)
        total = 0  # Count of listings collected

        while total < 100:  # Keep going until we collect at least 100 listings
            time.sleep(2)  # Wait for JavaScript on the page to load

            print(f"Scraping page: {self.driver.current_url}")

            # Get the full HTML of the page
            html = self.driver.page_source

            # Extract listings from the HTML using a separate function
            parsed_data = parse_listings(html)

            # Add extracted listings to our results list
            self.results.extend(parsed_data)

            total = len(self.results)
            print(f"Total listings collected: {total}")

            try:
                # Try to find the "Next" button and click it
                next_btn = self.driver.find_element(By.CSS_SELECTOR, "a.pagination__next")

                # If it's disabled, we've reached the last page
                if "disabled" in next_btn.get_attribute("class"):
                    break

                next_btn.click()  # Go to the next page
            except Exception as e:
                # If button is not found or there's another error, stop scraping
                print("No more pages or error:", e)
                break

        # Close the browser when done
        self.driver.quit()

        # Save the data as a CSV file in the output folder
        df = pd.DataFrame(self.results)
        df.to_csv("output/listings.csv", index=False)
        print("Saved listings to output/listings.csv")
