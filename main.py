# Import the RealEstateScraper class from scraper.py
from scraper import RealEstateScraper

# This is the main entry point of the program
if __name__ == "__main__":
    # Create an instance of the scraper
    scraper = RealEstateScraper()

    # Run the scraping process
    scraper.run()
