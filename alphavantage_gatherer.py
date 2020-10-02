import requests
import datetime
import numpy as np
import pandas as pd
from pandas import Series
import ta
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.trend import MACD

# ta documentation
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#volatility-indicators

API_KEY = 'PK4W268R10HW802W8SN9'  # keys from alpaca
SECRET_API_KEY = 'oFK1SOul4uEqwj4phpdFBAZG0CZqRraijzYQUkZH'
MARKET_URL = 'https://data.alpaca.markets'

TECHNICAL_DATABASE = {}  # dictionaries allow you to assume a key already exists
#  TECHNICAL_DATABASE[ticker][indicator][date][value] <- whats being used
#  TODO: Make pull_data search Database first
#  TODO: Make Database behave well with holidays
#  Alpaca does not not behave well with stock splits


def pull_data(ticker: str, indicator: str, indicator_range_specification: int, startdate: str, enddate: str):

    time_frame = '1D'

    # Create Datetime's
    startdate = datetime.date(int(startdate[6:]), int(startdate[3:5]), int(startdate[:2]))
    enddate = datetime.date(int(enddate[6:]), int(enddate[3:5]), int(enddate[:2]))
    duration = np.busday_count(startdate, enddate) + 1
    # print(duration)

    # Create URL
    bars_url = MARKET_URL + '/v1/bars/' + time_frame + '?symbols=' + ticker
    #  Obtain extra days of data; some indicators calculate from previous day and duration is off by one
    bars_url = bars_url + '&limit=' + str(indicator_range_specification + duration + 2)
    bars_url = bars_url + '&end=' + enddate.isoformat() + "T09:30:00-04:00"
    # print(bars_url)

    # Request Data
    r = requests.get(bars_url, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    r = r.json()
    r = r[ticker]

    # Print obtained data
    # for d in r:
    # print(d)

    # Get Bars
    # Creating Dataframe from Pricing Bar Values
    d = {'Open': [], 'High': [], 'Low': [], 'Close': [], 'Volume': []}
    for day in r:
        d['Open'].append(day['o'])
        d['High'].append(day['h'])
        d['Low'].append(day['l'])
        d['Close'].append(day['c'])
        d['Volume'].append(day['v'])

    output = get_technical(indicator, indicator_range_specification, duration, d, startdate)

    # Update Database
    if ticker not in TECHNICAL_DATABASE:
        TECHNICAL_DATABASE[ticker] = {}

    TECHNICAL_DATABASE[ticker][indicator + ", " + str(indicator_range_specification)] = output
    return output


# def get_technical(indicator: str, period: int, startdate: str, enddate: str):
def get_technical(indicator: str, period: int, duration: int, d: dict, startdate: datetime):

    df = pd.DataFrame(data=d)

    # Get Technical Indicator
    if indicator == 'open':
        output = d['Open'][len(d['Open'])-duration:]

    elif indicator == 'close':
        output = d['Close'][len(d['Open']) - duration:]

    elif indicator == 'high':
        output = d['High'][len(d['Open']) - duration:]

    elif indicator == 'low':
        output = d['Low'][len(d['Open']) - duration:]

    elif indicator == 'volume':
        output = d['Volume'][len(d['Open']) - duration:]

    elif indicator == 'low BB' or indicator == 'BB low':  # Lower Bollinger Band
        bb_low = ta.volatility.bollinger_lband(df["Close"], n=period, ndev=2, fillna=True)
        output = bb_low[len(bb_low)-duration:]

    elif indicator == 'high BB' or indicator == 'BB high':  # Higher Bollinger Band
        bb_high = ta.volatility.bollinger_hband(df["Close"], n=period, ndev=2, fillna=True)
        output = bb_high[len(bb_high) - duration:]

    elif indicator == 'ATR':  # Average True Range
        atr = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], n=period, fillna=True)
        output = atr[len(atr)-duration:]

    elif indicator == 'RSI':  # Relative Strength Index
        rsi = ta.momentum.rsi(df["Close"], n=period, fillna=True)
        output = rsi[len(rsi)-duration:]

    elif indicator == 'OBV':  # On-Balance Volume
        obv = ta.volume.on_balance_volume(df["Close"], df["Volume"], fillna=True)
        output = obv[len(obv)-duration:]

    elif indicator == 'MACD':  # Moving Average Convergence Divergence
        macd_proper = ta.trend.macd(df["Close"], n_fast=period, n_slow=period, fillna=True)
        output = macd_proper[len(macd_proper) - duration:]

    elif indicator == 'signal MACD' or indicator == 'MACD signal':
        macd_signal = ta.trend.macd_diff(df["Close"], n_fast=period, n_slow=period, fillna=True)
        output = macd_signal[len(macd_signal) - duration:]

    elif indicator == 'divergent MACD' or indicator == 'MACD divergent':
        macd_divergence = ta.trend.macd_signal(df["Close"], n_fast=period, n_slow=period, fillna=True)
        output = macd_divergence[len(macd_divergence) - duration:]

    # Return in dictionary with mapping [date:value]
    data = {}

    if isinstance(output, Series):
        # <output> is a series
        output = Series.tolist(output)
    # <output> is a list
    key = startdate
    friday = False
    for i in range(0, len(output)):
        left = np.busday_offset(key, 1, roll='backward')
        right = key + datetime.timedelta(days=1)
        if not (left == right):
            # <key is a friday>
            friday = True
        # keys are strings, if you want datetime object as key then remove .isoformat()
        data[key.isoformat()] = output[i]
        key = key + datetime.timedelta(days=1)
        if friday:
            # key = np.busday_offset(key, 1, roll='backward')
            key = key + datetime.timedelta(days=2)
            friday = False

    return data

if __name__ == '__main__':
    x = pull_data('TSLA', 'BB high', 7, "21-09-2018", "01-10-2020")
    print(x)

