from selenium import webdriver
import csv


def scrape_carfax():
    browser = webdriver.Chrome('/Users/bryangalindo/PycharmProjects/usedcars/chromedriver')
    noaccident_url = 'https://www.carfax.com/VehicleHistory/p/Report.cfx?make=HONDA&vin=-90%7C83%7C-126%7C-127%7C12%' \
                     '7C-13%7C102%7C-93%7C87%7C111%7C38%7C-30%7C32%7C-113%7C80%7C82%7C-33%7C126%7C57%7C-110%7C-29%' \
                     '7C-113%7C74%7C-4%7C&dealer_id=71168047&car_id=490454139&partner=ATD_W'
    accident_url = 'https://www.carfax.com/VehicleHistory/p/Report.cfx?make=HONDA&vin=-127%7C104%7C-16%7C90%7C77%' \
                   '7C-17%7C65%7C-74%7C29%7C-39%7C108%7C48%7C124%7C-90%7C-102%7C29%7C-65%7C62%7C-118%7C56%7C103%' \
                   '7C-50%7C-19%7C8%7C&dealer_id=595943&car_id=492023702&partner=ATD_U'
    browser.get(accident_url)
    accident_elements = browser.find_elements_by_xpath('//*[@id="accidentIndicatorCheckTalkingCarBlurb"]')
    accident_report = [x.text for x in accident_elements]
    browser.close()
    if accident_report[0].find('No') == -1:
        accident = '1'
    else:
        accident = '0'
    return {'Accidents': accident}


if __name__ == '__main__':
    accidents = []
    accidents.append(scrape_carfax())

    with open('autodatatest.csv', 'w') as f:
        keys = accidents[0].keys()
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(accidents)
