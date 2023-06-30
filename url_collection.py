import pandas as pd
import csv
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def prepare_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def fill_form(driver, place):
    '''Receives a search_argument to insert it in the search bar and
    then clicks the search button.'''
   
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'onetrust-accept-btn-handler'))).click()
    except: pass

    search_field = driver.find_element(By.ID,':Ra9:')

    # search_field.send_keys(place)
    search_field.send_keys(place)

    # We look for the search button and click it
    driver.find_element(By.XPATH,'//*[@id="indexsearch"]/div[2]/div/div/form/div[1]/div[4]/button').click()
    time.sleep(5)


def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''

    accommodations_urls = []
    # accommodations_data = list()
   
    # Get the accommodations links
    for accomodation_title in driver.find_elements(By.CLASS_NAME,'a4225678b2'):
        # close sign-in prompt
        try: 
            driver.find_element(By.XPATH,'//*[@id="b2searchresultsPage"]/div[25]/div/div/div/div[1]/div[1]/div/button').click()
        except: pass
        accommodations_urls.append(accomodation_title.find_element(By.CLASS_NAME,
            'e13098a59f').get_attribute('href'))

    return accommodations_urls
       
       
def next_page(driver):
   
    accomodations_urls = []
 
    accomodations_urls.append(scrape_results(driver))
   
    while True:
        try:
            time.sleep(6)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search_results_table"]/div[2]/div/div/div[4]/div[2]/nav/div/div[3]/button'))).click()
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next page'))).click()
            time.sleep(6)
            accomodations_urls.append(scrape_results(driver))
        except TimeoutException:
            break
   
    accomodations_urls = [item for sublist in accomodations_urls for item in sublist]
   
    return accomodations_urls

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

driver = prepare_driver('https://www.booking.com/')
fill_form(driver, 'Magdeburg')

urls = []
urls.append(next_page(driver))
urls = [item for sublist in urls for item in sublist]
export_to_csv(urls, 'urls.csv')