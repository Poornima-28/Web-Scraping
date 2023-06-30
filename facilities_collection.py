import pandas as pd
import requests
import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def csv_to_list(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)[0]  # Convert the first row to a list

    return data


# import accommodation urls
urls = csv_to_list('urls.csv')


hotels = pd.DataFrame(columns = ['url','hotel_name','hotel_address','facilities','overall','number_of_reviews','scores'])
# facilities_df = pd.DataFrame(columns = ['hotel_id','facilities'])


for url in urls[:3]:

    # hotel Deatailed data
    page = requests.get(url)
    item = BeautifulSoup(page.text, 'html.parser')
    # try: 
    #     hotel_type = item.find('span', {'data-testid': 'property-type-badge'}).text
    #     script_data = json.loads(item.find('script', {'data-capla-store-data' : 'apollo'}).text)
    #     hotel_id = script_data[list(script_data.keys())[0]]['id']
    #     star_rating = script_data['StarRating:{}']['value']
    #     rating_type = script_data['StarRating:{}']['symbol']
    # except: pass  
    try:
        hotel_name = item.find('h2',class_ = 'd2fee87262 pp-header__title').text
        hotel_address = item.find('span', class_ = 'hp_address_subtitle js-hp_address_subtitle jq_tooltip').text
    except:pass
    try:
        number_of_reviews = float(item.find('a', {'data-target' : 'hp-reviews-sliding'}).text.split(" ")[2].replace(")","").replace("(","").replace(",",""))
        overall = float(item.find('div', class_ = 'b5cd09854e d10a6220b4').text)
        scores = {}
        for score in item.find_all('div',class_ = 'c-score-bar'):
            title = score.find('span',class_ = 'c-score-bar__title').text.strip()
            value = float(score.find('span',class_ = 'c-score-bar__score').text)
            scores[title] = value
    except: pass

    #hotel faciltiies 
    facilities = {}
    for category in item.find_all('div',class_ = 'f1e6195c8b'):
        title_text = category.find('div',class_= 'a432050e3a').text.strip()

        facility_list = []
        for li in category.find_all('span', class_= 'db312485ba'):
            facility_list.append(li.text.strip())
       
        facilities[title_text] = facility_list

    df_length = len(hotels)
    # hotel_id,hotel_type, star_rating, rating_type -additional columns
    hotels.loc[df_length] = [url,hotel_name,hotel_address,facilities,overall,number_of_reviews,scores]
  
            

hotels = hotels.join(pd.json_normalize(hotels.pop('scores')))
hotels.to_csv('facilities.csv', index = False)