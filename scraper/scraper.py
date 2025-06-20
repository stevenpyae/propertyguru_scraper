import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- Load Rotating User Agents ----------


def load_user_agents(filename="C:\\Users\\Steven\\propertyguru_scraper\\scraper\\user_agents.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


user_agents = load_user_agents()
listing_data = []
max_pages = 3

# ---------- Scraping Function ----------


def scrape_page(page_url, page_number):
    selected_agent = random.choice(user_agents)
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={selected_agent}")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"""
    })

    records_scraped = 0
    next_page_url = None

    try:
        print(f"Navigating to page {page_number}: {page_url}")
        driver.get(page_url)
        time.sleep(random.uniform(5, 8))

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.listing-card-root"))
        )

        listings = driver.find_elements(
            By.CSS_SELECTOR, "div.listing-card-root")
        print(f"🔍 Found {len(listings)} listings.")

        for idx, card in enumerate(listings, 1):
            try:
                link_elem = card.find_element(
                    By.CSS_SELECTOR, "a.listing-card-link")
                title = link_elem.get_attribute("title")
                url = link_elem.get_attribute("href")
                price = card.find_element(
                    By.CSS_SELECTOR, "div.listing-price").text.strip()
                location = card.find_element(
                    By.CSS_SELECTOR, "div.listing-address").text.strip()

                feature_list = card.find_elements(
                    By.CSS_SELECTOR, "ul.listing-feature-group li.info-item span.info-value"
                )
                feature_texts = [f.text.strip()
                                 for f in feature_list if f.text.strip()]

                features = {
                    "Bedrooms": feature_texts[0] if len(feature_texts) > 0 else "N/A",
                    "Bathrooms": feature_texts[1] if len(feature_texts) > 1 else "N/A",
                    "Floor Area": feature_texts[2] if len(feature_texts) > 2 else "N/A",
                    "Price per sqft": feature_texts[3] if len(feature_texts) > 3 else "N/A"
                }

                listing_data.append({
                    "Title": title,
                    "URL": url,
                    "Price": price,
                    "Location": location,
                    "Bedrooms": features["Bedrooms"],
                    "Bathrooms": features["Bathrooms"],
                    "Floor Area": features["Floor Area"],
                    "Price per sqft": features["Price per sqft"]
                })

                records_scraped += 1
                print(f"✅ Listing {idx}: {title[:50]}...")

            except Exception as e:
                print(f"⚠️ Error on listing {idx}: {e}")

        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR, "a[da-id='hui-pagination-btn-next']")
            if "disabled" not in next_button.get_attribute("class"):
                next_page_url = next_button.get_attribute("href")
        except:
            next_page_url = None

    except Exception as e:
        print(f"🚨 Error scraping page {page_number}: {e}")
    finally:
        driver.quit()

    return records_scraped, next_page_url


# ---------- Main Scraping Loop ----------
current_url = "https://www.propertyguru.com.sg/property-for-sale"
page_num = 1
total_records = 0
max_records = 200

while total_records < max_records:
    records_scraped, next_url = scrape_page(current_url, page_num)
    total_records += records_scraped
    print(f"📦 Total listings collected: {total_records}")
    current_url = next_url
    page_num += 1
    #  To trick the website into thinking we are a human, we will wait for a random time between 10 to 15 seconds before scraping the next page.
    time.sleep(random.uniform(10, 15))

# ---------- Save Results ----------
csv_file = "output/propertyguru_listings.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "Title", "URL", "Price", "Location", "Bedrooms", "Bathrooms", "Floor Area", "Price per sqft"])
    writer.writeheader()
    writer.writerows(listing_data)

print(f"✅ Done. Saved {len(listing_data)} listings to '{csv_file}'")
