import pandas as pd
from selenium import webdriver
import random
import time

def convertDuration(str):
        if len(str) > 3:
        duration = int(str.split(' ')[0].replace('h', '')) * 60
        duration += int(str.split(' ')[1].replace('m', ''))
    else:
        duration = int(str.replace('m', ''))
    return duration

chrome_path = 'C:/Users/veyro/OneDrive/Desktop/chromedriver_win32/chromedriver.exe'
browser = webdriver.Chrome(chrome_path)

df_airports = pd.read_html('https://en.wikipedia.org/wiki/List_of_the_busiest_airports_in_the_United_States')[0]
airport_codes = df_airports['IATACode'][:10]
already_processed = []

df_out = {'origin': [], 'destination': [], 'price': [], 'duration': [], 'airline': []}

for origin in airport_codes:
    for destination in airport_codes:
        if destination in already_processed:
            continue
        if destination == origin:
            continue
        if random.randint(1, 3) != 1:
            continue
        browser.get(f'https://www.expedia.com/Flights-Search?flight-type=on&starDate=11%2F09%2F2019&mode=search&trip=oneway&leg1=from%3A{origin}%2Cto%3A{destination}%2Cdeparture%3A11%2F10%2F2019TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY')
        time.sleep(10)
        try:
            nonstop_box = browser.find_element_by_css_selector('input#stopFilter_stops-0')
            nonstop_box.click()
            time.sleep(2)

            used_airlines = []
            airlines_webelem = browser.find_elements_by_css_selector('span[data-test-id="airline-name"]')
            if len(airlines_webelem) == 0:
                continue
            airlines = []
            for airline_webelem in airlines_webelem:
                airlines.append(airline_webelem.text)
            durations_webelem = browser.find_elements_by_css_selector('span.duration-emphasis[data-test-id="duration"]')
            durations = []
            for duration_webelem in durations_webelem:
                durations.append(duration_webelem.text)
            prices_webelem = browser.find_elements_by_css_selector('span.full-bold.no-wrap[data-test-id="listing-price-dollars"]')
            prices = []
            for price_webelem in prices_webelem:
                prices.append(price_webelem.text)
        except:
            continue
        for i in range(0, 3 if len(set(airlines)) > 3 else len(set(airlines))):
            j = i
            while airlines[j] in used_airlines:
                j += 1
            df_out['origin'].append(origin)
            df_out['destination'].append(destination)
            df_out['price'].append(int(prices[j].replace('$', '')))
            df_out['duration'].append(convertDuration(durations[j]))
            df_out['airline'].append(airlines[j])
            used_airlines.append(airlines[j])
    already_processed.append(origin)

df_out = pd.DataFrame(df_out)
with open('flightdata.txt', 'w') as fout:
    fout.write(f'{len(df_out.index)}\n')
    for origin, destination, price, duration, airline in zip(df_out['origin'], df_out['destination'], df_out['price'], df_out['duration'], df_out['airline']):
        fout.write(f'{origin}|{destination}|{price}|{duration}|{airline}\n')



