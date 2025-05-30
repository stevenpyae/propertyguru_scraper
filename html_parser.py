from bs4 import BeautifulSoup


def parse_listings(html):
    """
    Parses the PropertyGuru HTML page source and extracts a list of property listings.
    
    Args:
        html (str): HTML source from the current page loaded by Selenium.
    
    Returns:
        list[dict]: A list of dictionaries with property details.
    """
    soup = BeautifulSoup(html, 'html.parser')

    listings = []

    # Property listings are wrapped inside this tag/class
    cards = soup.select("div[data-testid='listing-card']")

    for card in cards:
        try:
            # Extract title
            title_tag = card.select_one("h3[data-testid='listing-title']")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            # Extract price
            price_tag = card.select_one("span[data-testid='listing-price']")
            price_text = price_tag.get_text(strip=True).replace(
                ",", "").replace("S$", "") if price_tag else "0"
            try:
                price = float(price_text)
            except ValueError:
                price = 0.0

            # Extract location
            location_tag = card.select_one(
                "span[data-testid='listing-location']")
            location = location_tag.get_text(
                strip=True) if location_tag else "N/A"

            # Extract listing URL
            link_tag = card.select_one("a[data-testid='listing-card-link']")
            url = f"https://www.propertyguru.com.sg{
                link_tag['href']}" if link_tag and 'href' in link_tag.attrs else "N/A"

            # Save the listing as a dictionary
            listings.append({
                "title": title,
                "price_sgd": price,
                "location": location,
                "url": url
            })

        except Exception as e:
            print(f"Error parsing listing: {e}")
            continue

    return listings
