import pandas as pd
import csv
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import datetime
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

def csv_to_list(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)[0]  # Convert the first row to a list

    return data

# Call the function
urls = csv_to_list('urls.csv')

test_url = ['https://www.booking.com/hotel/at/salzburger-hof-bad-gastein.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaDuIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4AsLX5pkGwAIB0gIkYmE2YTVhZjYtNTkyMS00NzAzLWJhOGUtZDc5ZWYwMGMzNjI12AIG4AIB&sid=c412bfc9ac6767f79964c27d84f4576f&aid=304142&ucfs=1&arphpl=1&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=2&hapos=2&sr_order=popularity&srpvid=77b26babeab70030&srepoch=1664723928&from_sustainable_property_sr=1&from=searchresults#hotelTmpl']

review_main = []

for link in test_url:
    driver.get(link)
    try:
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(., 'Guest reviews')]"))).click()
    except: continue

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'onetrust-accept-btn-handler'))).click()
    except: pass

   
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'review_sort'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[contains(., 'Newest first')]"))).click()

    reviews_dfs = []
     
    while True:
         try:
             time.sleep(3)
             page += 1
             
             # WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Show translation')]")))  
             translators = driver.find_elements(By.XPATH, "//a[contains(., 'Show translation')]")
             
             for t in translators:  
                 time.sleep(0.3)
                 try:
                      t.location_once_scrolled_into_view
                      t.click()
                 except:
                      driver.execute_script("arguments[0].click()",t)
                   
             time.sleep(0.5)
         
             soup = BeautifulSoup(driver.page_source, 'html.parser')
             
            #  script_data = json.loads(soup.find('script', {'data-capla-store-data' : 'apollo'}).text)
            #  hid = script_data[list(script_data.keys())[0]]['hotelId']
  
             
             URL, name, country, room_type, stay_date, traveller_type, review_score ,review , review_date = ([] for i in range(9))
             
             
             for item in soup.find_all('div', class_= 'bui-grid__column-3 c-review-block__left'):
    
                 try:
                     name.append(item.find('span', class_ = 'bui-avatar-block__title').text.strip())
                 except: name.append(None)
                 try:
                     country.append(item.find('span',class_ = 'bui-avatar-block__subtitle').text.strip())
                 except: country.append(None)
                 try:
                     room_type.append(item.find('a', class_ = 'c-review-block__room-link').text.strip())
                 except: room_type.append(None)
                 try:
                     stay_date.append(item.find('span', class_ ='c-review-block__date').text.strip())
                 except: stay_date.append(None)
                 try:
                     traveller_type.append(item.find('ul', class_ = 'bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row').text.strip())
                 except: traveller_type.append(None)
        
             
             for score in soup.find_all('div', class_ = 'bui-review-score__badge'):
                 try:
                     review_score.append(score.text)
                 except: review_score.append(None)
           
             for items in soup.find_all('div', class_ = 'bui-grid__column-9 c-review-block__right'):
                  for date in items.find('span',class_ = 'c-review-block__date'):
                      try:
                          review_date.append(date.text)
                      except: review_date.append(None)
           
             length = len(name)
           
             
             
             review_list = driver.find_element(By.XPATH,"//ul[@class = 'review_list']")
             review_list = review_list.get_attribute('innerHTML')
             soup = BeautifulSoup(review_list, 'html.parser')
             
             for r in soup.find_all('div', class_ = 'c-review'):
                  output = ''
                  for t in r.find_all('span',text=True):
                      output += '{}: {}\n\n\n'.format(t.get('class'),t.text)
                     
                  review.append(output)
           
             
            #  hotel_id = [hid for i in range(len(name))]
             URL = [link for i in range(len(name))]
                 
             d = {
                 'url' : URL,
                #  'hotel_id': hotel_id,
                 'name': name,
                 'country': country,
                 'room_type' : room_type,
                 'stay_date': stay_date,
                 'traveller_type' : traveller_type,
                 'review_score': review_score,
                 'review' : review,
                 'review_date' : review_date
                  }
             
             x = pd.DataFrame.from_dict(d)
           
             reviews_dfs.append(x)
             
             # time.sleep(10)
             if review_date[-1].strip()[-4:] == '2022' :
                 break
             else:
             # time.sleep(10)
                 try:
                     WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a'))).click()
                 except:
                     driver.execute_script("arguments[0].click()", WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a'))).click())
         except TimeoutException:
             break
             
   
    review_main.append(pd.concat(reviews_dfs, ignore_index = True))


# Combine DataFrames into one DataFrame
combined_df = pd.concat(review_main)

# Export DataFrame as CSV
combined_df.to_csv('reviews.csv', index=False)