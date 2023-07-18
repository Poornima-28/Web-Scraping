# Web-Scraping
Booking.com data scraping

Project Overview
The goal of this project is to collect data from Booking.com website and provide valuable insights for analysis. The three scrapers included in this project are tailored to specific types of data:

1. The Accommodation Scraper retrieves information about available accommodations in a given location.
2. The Hotel Details Scraper collects detailed information about individual hotels, such as amenities, ratings, address etc.
3. The Hotel Reviews Scraper extracts customer reviews and ratings for selected hotels.
   
Dependencies:
• Python 3.x
• Beautiful Soup
• Selenium
• Chrome WebDriver (for Selenium)

Installation
• Clone this repository to your local machine.
• Ensure you have Python 3.x installed.
Install the required dependencies using pip:

```bash
pip install beautifulsoup4
pip install selenium
```

Download the appropriate Chrome WebDriver for your operating system and place it in the project directory.

Usage
To use the scrapers, follow these steps:

Configure the input parameters in each scraper file to specify the desired location, hotel name, or other relevant details.
Run each scraper individually using Python:

```bash
python url_collection.py
python facilities_collection.py
python review_collection.py
```

The scrapers will start collecting data from the respective websites and save the extracted information in CSV

### Rating Correlation Analysis
https://tinyurl.com/poornima-hotel-rating-analysis
