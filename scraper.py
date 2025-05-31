from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=chrome_options)
start_url = "https://www.propertyguru.com.sg/property-for-sale"
driver.get(start_url)

# Let Cloudflare challenge pass
time.sleep(10)

print("Title:", driver.title)

# Cloudflare detection
if "Just a moment" in driver.title:
    print("⚠️ Still stuck behind Cloudflare. Manually finish it in the browser.")
    input("✅ Press Enter once the page fully loads...")

# Find listing blocks
listings = driver.find_elements(By.CSS_SELECTOR, "div.listing-card-root")
print(f"✅ Found {len(listings)} listings on this page.")

# Extract data from each card
for idx, card in enumerate(listings[:10], 1):  # Limit to first 10 for now
    try:
        
        # Extracting title and URL
        link_elem = card.find_element(By.CSS_SELECTOR, "a.listing-card-link")
        title = link_elem.get_attribute("title")
        url = link_elem.get_attribute("href")
        # Extracting price 
        price_elem = card.find_element(
            By.CSS_SELECTOR, "div.listing-price")
        price = price_elem.text.strip()
        # Extracting location
        location_elem = card.find_element(
            By.CSS_SELECTOR, "div.listing-address")
        location = location_elem.text.strip()
        # Get feature list
        feature_list = card.find_elements(
            By.CSS_SELECTOR, "ul.listing-feature-group li.info-item span.info-value")
        feature_texts = [f.text.strip()
                         for f in feature_list if f.text.strip()]
        # If no features found, use a placeholder
        if not feature_texts:
            feature_texts = ["No features listed"]  

            # Map features with labels based on order
        features = {
            "Bedrooms": feature_texts[0] if len(feature_texts) > 0 else "N/A",
            "Bathrooms": feature_texts[1] if len(feature_texts) > 1 else "N/A",
            "Floor Area": feature_texts[2] if len(feature_texts) > 2 else "N/A",
            "Price per sqft": feature_texts[3] if len(feature_texts) > 3 else "N/A"
        }

        # Extract floor area (usually contains 'sqft')
        floor_area = next((f for f in feature_texts if 'sqft' in f), "N/A")
        num_features = len(feature_texts)

        print(f"{idx}. {title}")
        print(f"   🔗 {url}")
        print(f"   💰 {price}")
        print(f"   📍 {location}\n")
        print(f"   📐 Floor Area: {floor_area}")
        print(f"   🧩 Features Count: {num_features}")
        for key, value in features.items():
            print(f"   {key}: {value}")
        print()


    except Exception as e:
        print(f"{idx}. ⚠️ Error extracting data: {e}")

driver.quit()
