"""
This is to gather data from the IEX Cloud related to technical indicators, etc.
that may be used to initiate trades within a trading algorithm.
"""

from typing import Optional
import requests

SANDBOX = True

if SANDBOX:
    sand = 'sandbox'
else:
    sand = 'cloud'

def get_technical(api_key: str, ticker: str, indicator: str, range: Optional[str] = '1m'):
    """
    #TODO Should I return the first and last dates of the range to compare?
    Used for indicators:
    - sma
    - ema
    - bbands
    - atr
    - rsi
    - obv
    - macd
    """

    url = f'https://{sand}.iexapis.com/stable/stock/{ticker}/indicator/{indicator}?range={range}&token={api_key}'
    r = requests.get(url)
    print(url)
    return r.json()['chart']

def get_price_data(api_key: str, ticker: str, date_value: str):
    """
    Date formatted as 20190220

    Used for:
    - open
    - close
    - high
    - low
    - volume
    """

    url = f'https://{sand}.iexapis.com/stable/stock/{ticker}/chart/date/{date_value}?token={api_key}'
    r = requests.get(url)
    print(url)
    ret = {}
    ret['open'] = r.json()[0]['open']
    ret['close'] = r.json()[-1]['close']
    ret['high'] = max([i['high'] for i in r.json() if i['high'] is not None])
    ret['low'] = min([i['low'] for i in r.json() if i['low'] is not None])
    ret['volume'] = sum([i['volume'] for i in r.json() if i['volume'] is not None])
    return ret


# print(get_technical("Tpk_6ef4a75d2a6f4d95be047b5629cf964f", "aapl", "macd"))
# print(get_price_data("Tpk_6ef4a75d2a6f4d95be047b5629cf964f","aapl","20200810"))
