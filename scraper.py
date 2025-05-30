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

for idx, listing in enumerate(listings[:5], 1):
    try:
        anchor = listing.find_element(By.CSS_SELECTOR, "a.listing-card-link")
        url = anchor.get_attribute("href")
        title = anchor.get_attribute("title")

        img = listing.find_element(By.CSS_SELECTOR, "img.hui-image-root")
        image_url = img.get_attribute("src")

        print(f"\n{idx}. {title}")
        print(f"   🔗 URL: {url}")
        print(f"   🖼️ Image: {image_url}")
    except Exception as e:
        print(f"⚠️ Listing {idx} skipped: {e}")

driver.quit()
