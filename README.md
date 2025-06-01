# 🏡 PropertyGuru Singapore Listing Scraper

A Python-powered real estate scraper using Selenium to extract property listings from [PropertyGuru Singapore](https://www.propertyguru.com.sg).  
It collects listing details like price, location, floor area, and more, and saves them into a structured CSV file.

---

## 📦 Features

- 🔄 **Rotating User Agents** to reduce bot detection
- 🧠 **Human-like delays** with randomized wait times
- 🔎 Extracts:
  - Title
  - Price
  - Location
  - Bedrooms
  - Bathrooms
  - Floor Area
  - Price per sqft
  - Listing URL
- 📄 Exports all data to `output/propertyguru_listings.csv`
- 🚫 Ignores listings that fail to load — the scraper continues
---

## 🛠️ Setup Instructions (Terminal)

### 1. Clone the Repository
git clone https://github.com/stevenpyae/propertyguru_scraper.git  
cd propertyguru_scraper

### 2. Create Virtual Environment (Optional but Recommended)
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run the Python script
python scraper.py

### 5. Check output 
Successful Extraction : [INFO] Saved 400 records to output/books.csv  
Check output/books.csv

### 6. Review
Current set for 20 pages, Modify the below data to your desired outcome  
--scraper.py Line 74: book_data = scrape_books(max_pages=20)  # Scrape up to 20 pages (400 books max)