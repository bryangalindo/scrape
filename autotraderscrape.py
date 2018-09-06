#!/usr/bin/env python3
# title           :autotraderscrape.py
# description     :Program scrapes multiple used cars' profiles for features
# author          :Bryan Galindo
# date            :08/13/18
# version         :1.0
# usage           :python3 autotraderscrape.py
# notes           :
# python_version  :3.6.4
# ==============================================================================

import requests, re, csv
from bs4 import BeautifulSoup
from selenium import webdriver


def make_soup(url):
    ''' Retrieves html code from url '''
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                             ' Version/11.1.2 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pass
    else:
        print('Oops, you\'ve come across status code error: %s' % str(response.status_code))
    return BeautifulSoup(response.content, features='html.parser')


def get_autotrader_links(page_url):
    ''' Retrieves a list of the anchor tags '''
    soup_links = make_soup(page_url)
    tags = soup_links('a', {'href': re.compile("^/cars-for-sale/vehicledetails")})
    listings = [tag.get('href') for tag in tags]
    return listings


def get_carfax_links(page_url):
    ''' Retrieves a list of carfax reports from respective car '''
    soup_carfax = make_soup(page_url)
    carfax_links = soup_carfax('a', {'href': re.compile("^http://www\.carfax\.com")})
    carfax = [carfax_link.get('href') for carfax_link in carfax_links]
    return carfax


def get_carfax_info(carfax_url):
    ''' Extract from car listings' car fax report whether car in accident'''
    browser = webdriver.Chrome('/Users/bryangalindo/PycharmProjects/usedcars/chromedriver')
    browser.get(carfax_url)
    accident_elements = browser.find_elements_by_xpath('//*[@id="accidentIndicatorCheckTalkingCarBlurb"]')
    accident_report = [x.text for x in accident_elements]
    if accident_report[0].find('No') == -1:
        accident = '1'
    else:
        accident = '0'
    return {'Accidents': accident}


def get_auto_info(auto_url):
    ''' Retrieves a dictionary of car characteristics (e.g. price) '''
    soup_info = make_soup(auto_url)
    listing_id = re.findall(r"\D(\d{9})\D", auto_url)
    title = soup_info.find('h1')
    components = title.text.rsplit(' ')
    condition = components[0]
    year = components[1]
    make = components[2]
    model = components[3]
    trim = components[4]
    price = soup_info.find('div', {'class':'text-success text-size-30 margin-right-auto'})
    features = soup_info.findAll('div', {'class':'text-base text-bold'})
    engine = features[2].text
    mileage = features[0].text
    exterior = features[6].text
    return{'Listing ID': listing_id[0], 'Condition': condition,
           'Year': year, 'Make': make,
           'Model': model, 'Trim': trim, 'Engine': engine,
           'Exterior': exterior, 'Price': price.text,
           'Mileage': mileage}


if __name__ == '__main__':
    BASE_AUTOTRADER_URL = 'https://www.autotrader.com'
    page_url = BASE_AUTOTRADER_URL + '/cars-for-sale/searchresults.xhtml?zip=77002&maxPrice=20000&startYear=2010&' \
               'endYear=2019&vehicleStyleCodes=SEDAN&makeCodeList=HONDA&listingTypes=CERTIFIED%2CUSED&searchRadius=75&' \
               'modelCodeList=ACCORD&sortBy=relevance&numRecords=25&firstRecord=0'
    autotrader_links = get_autotrader_links(page_url)
    carfax_links = get_carfax_links(page_url)
    car_data = []
    accidents = []
    for link in autotrader_links:
        url = BASE_AUTOTRADER_URL + str(link)
        car_data.append(get_auto_info(url))

    for link in carfax_links:
        accidents.append(get_carfax_info(link))

    with open('autodatatest.csv', 'w') as f:
        keys = ['Listing ID', 'Condition', 'Year', 'Make', 'Model',	'Trim',
                'Engine', 'Exterior', 'Mileage', 'Price', 'Accidents']
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(car_data)
        w.writerows(accidents)
