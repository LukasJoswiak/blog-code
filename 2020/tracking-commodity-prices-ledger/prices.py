#!/usr/bin/env python3

from datetime import datetime, timedelta
import json
import os
import requests
import sys

SYMBOLS = ['VTSAX']  # add more symbols here
API_KEY = 'YOUR_API_KEY_HERE'  # get your API key at https://api.tiingo.com
PRICES_FILE = '/path/to/prices.db'

def query_data(symbol):
    # Pull price data
    url = f'https://api.tiingo.com/tiingo/daily/{symbol}/prices'
    payload = {'token': API_KEY}
    r = requests.get(url, params=payload)
    return r.json()


def output(symbol, prices):
    data = query_data(symbol)

    # Failure response is a string. Data response is an array.
    if not isinstance(data, list):
        print('no data found, exiting (probably got rate limited)...')
        sys.exit(0)

    data = data[0]

    adjusted_close = data['adjClose']
    date = data['date']
    if not adjusted_close or not date:
        print('data not found in response, exiting...')
        sys.exit(0)

    # Convert date string to date object.
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date()

    # Look through existing entries to make sure a price for this date doesn't
    # already exist.
    for price in prices:
        if len(price) != 4:
            continue

        # Grab date and symbol from existing entry.
        parsed_date = datetime.strptime(price[1], '%Y/%m/%d').date()
        parsed_symbol = price[2]

        if parsed_symbol == symbol and parsed_date == date:
            print(f'existing price found for {symbol} on {date}: {price[3]} (${adjusted_close})')
            return None

    date = date.strftime('%Y/%m/%d')
    output = f'P {date} {symbol} ${adjusted_close}\n'
    return output


if __name__ == '__main__':
    datetime = datetime.now()
    # For logging purposes
    print(datetime)

    with open(PRICES_FILE, 'r') as f:
        prices = f.readlines()
    prices = [x.strip().split() for x in prices]

    lines = []
    for symbol in SYMBOLS:
        line = output(symbol, prices)
        if line:
            lines += [line]

    if len(lines) > 0:
        with open(PRICES_FILE, 'a') as f:
            f.write('\n')
            for line in lines:
                print(f'writing {line.strip()}')
                f.write(line)
