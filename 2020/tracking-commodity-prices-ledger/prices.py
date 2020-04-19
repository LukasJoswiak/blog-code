from datetime import datetime, timedelta
import json
import os
import requests
import sys

SYMBOLS = ['VTSAX']
API_KEY = 'YOUR_API_KEY_HERE'  # get your API key at https://www.alphavantage.co/support/#api-key
PRICES_FILE = '/path/to/prices.db'

def query_data(symbol):
    # Pull price data
    url = 'https://www.alphavantage.co/query'
    payload = {'function': 'GLOBAL_QUOTE', 'symbol': symbol, 'apikey': API_KEY}
    r = requests.get(url, params=payload)
    return r.json()


def output(symbol, prices):
    data = query_data(symbol)

    if 'Global Quote' not in data:
        print('no data found, exiting (probably got rate limited)...')
        sys.exit(0)

    data = data['Global Quote']
    symbol = data['01. symbol']
    current_price = data['05. price']
    date = data['07. latest trading day']
    if not symbol or not current_price or not date:
        print('correct data not found, exiting...')
        sys.exit(0)

    date = datetime.strptime(date, '%Y-%m-%d').date()

    for price in prices:
        if len(price) != 4:
            continue

        parsed_date = datetime.strptime(price[1], '%Y/%m/%d').date()
        parsed_symbol = price[2]

        if parsed_symbol == symbol and parsed_date == date:
            print(f'existing price found for {symbol} on {date}: {price[3]} (${current_price})')
            return None

    date = date.strftime('%Y/%m/%d')
    output = f'P {date} {symbol} ${current_price}\n'
    return output


if __name__ == '__main__':
    datetime = datetime.now()
    # For logging purposes
    print(datetime)

    with open(PRICES_FILE) as f:
        prices = f.readlines()
    prices = [x.strip().split() for x in prices]

    lines = []
    for symbol in SYMBOLS:
        line = output(symbol, prices)
        if line:
            lines += [line]

    if len(lines) > 0:
        with open(PRICES_FILE) as f:
            f.write('\n')
            for line in lines:
                print(f'writing {line.strip()}')
                f.write(line)
