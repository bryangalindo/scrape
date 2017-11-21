#!/usr/bin/env python
# title           :ebayscrape.py
# description     :Program scrapes multiple auction item's profile
# author          :Bryan Galindo
# date            :11/20/2017
# version         :1.0
# usage           :python ebayscrape.py
# notes           :
# python_version  :2.7.13
# ==============================================================================


from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import csv


def make_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'lxml')


def scrape_auctions(ebay_url):

    # extract html for ebay webpage
    soup = make_soup(ebay_url)
    listings = soup.find_all("div", id="ResultSetItems")
    data_list = []
    bid_list = []
    numbid_list = []
    percent_list = []
    rating_list = []
    bids_list = []
    endTimes_list = []
    startTimes_list = []

    for listing in listings:
        # extracts product links
        links = [h3.a['href'] for h3 in listing.findAll('h3', 'lvtitle')]

        # extracts winning bid price
        for item in listing.find_all("span", class_="bold bidsold"):
            bid = item.get_text().split('$')
            bid_list.append(bid[1])

        # extracts number of bids in auction
        for item in listing.find_all("li", class_="lvformat"):
            raw_numbid = item.get_text().strip()
            numbid = raw_numbid.split(' ')
            numbid_list.append(numbid[0])

        # extracts shipping fee if any
        for item in listing.find_all("span", class_="ship"):
            shipping = re.findall('[0-9]*\.[0-9]*', item.get_text())
            data_list.append(shipping)

    for link in links:
        # creates url for bid times
        base_url = 'https://www.ebay.com/bfl/viewbids/'
        items = link.split('/')[5]
        id = items.split('?')[0]
        bidlisturl = base_url + id
        bids_list.append(bidlisturl)

        # extracts html for product links
        soup3 = make_soup(link)

        # extracts starting times for auctions
        startTimes = soup3.find_all('span', 'endedDate')

        # time raw form is in 24hr format, need to convert to 12hr format
        for time in startTimes:
            rawTime = time.get_text().strip().split('PST')
            tempTime = datetime.strptime(rawTime[0], '%H:%M:%S ')
            finalTime = tempTime.strftime('%I:%M:%S%p')
            startTimes_list.append(finalTime)

        # extracts seller profile links
        sellers = [div.a['href'] for div in soup3.findAll('div', class_='mbg vi-VR-margBtm3')]

        # some lists have two entries, only need first entry
        if len(sellers) == 1:
            for seller in sellers:
                soup4 = make_soup(seller)
                profiles = soup4.find_all("div", id="user_info")

                for profile in profiles:
                    # collects rating percentage
                    for item in profile.find_all('div', class_='perctg'):
                        percent = item.get_text().strip().split('%')
                        if percent[0] != '':
                            percent_list.append(percent[0])
                        else:
                            percent_list.append('0')

                    # collects rating score
                    if len(profile.find_all('i', class_='gspr')) != 0:
                        for item in profile.find_all('i', class_='gspr'):
                            newitem = str(item).rsplit()
                            rating = re.findall('[0-9]+', newitem[5])
                            rating_list.append(rating)
                    else:
                        rawrating = profile.find_all('a')
                        if len(rawrating) == 1:
                            rating_list.append('0')
                        else:
                            lowrating = rawrating[1].get_text().split()
                            if len(lowrating) != 0:
                                rating_list.append(lowrating[2])
                            else:
                                rating_list.append('0')

        else:
            sellers.remove(sellers[1])
            for seller in sellers:
                soup4 = make_soup(seller)
                profiles = soup4.find_all("div", id="user_info")

                for profile in profiles:
                    # collects rating percentage
                    for item in profile.find_all('div', class_='perctg'):
                        percent = item.get_text().strip().split('%')
                        if percent[0] != '':
                            percent_list.append(percent[0])
                        else:
                            percent_list.append('0')

                    # collects rating score
                    if len(profile.find_all('i', class_='gspr')) != 0:
                        for item in profile.find_all('i', class_='gspr'):
                            newitem = str(item).rsplit()
                            rating = re.findall('[0-9]+', newitem[5])
                            rating_list.append(rating)
                    else:
                        rawrating = profile.find_all('a')
                        if len(rawrating) == 1:
                            rating_list.append('0')
                        else:
                            lowrating = rawrating[1].get_text().split()
                            if len(lowrating) != 0:
                                rating_list.append(lowrating[2])
                            else:
                                rating_list.append('0')

    # extract winning bid's time
    for bid in bids_list:
        soup5 = make_soup(bid)
        times = soup5.find_all('span')
        for time in times:
            if time.get_text().endswith('PST'):
                tuna = [time.get_text()]
                tuna = tuna[0].split()
                win_time = tuna[4]
                endTimes_list.append(win_time)
                break

    # creates csv file with extracted info
    with open('ebaylinks.csv', 'wb') as file:
        writer = csv.writer(file)
        writer.writerow(bid_list)
        for row in data_list:
            writer.writerow(row)
        writer.writerow(numbid_list)
        writer.writerow(percent_list)
        for row in rating_list:
            writer.writerow(row)
        writer.writerow(startTimes_list)
        writer.writerow(endTimes_list)
        writer.writerow(bids_list)
        writer.writerow(links)


if __name__ == '__main__':
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_Complete=1&LH_Sold=1&LH_Auction=1&_nkw=ipod+nano+7th+generation&_ipg=100&rt=nc'
    # str(raw_input("Please input Ebay URL: "))
    scrape_auctions(url)
