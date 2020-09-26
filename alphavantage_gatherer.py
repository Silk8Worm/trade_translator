import requests
import pandas as pd
import ta
from ta import add_all_ta_features
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.trend import MACD

# ta documentation
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#volatility-indicators

API_KEY = 'PK4W268R10HW802W8SN9'  # keys from alpaca
SECRET_API_KEY = 'oFK1SOul4uEqwj4phpdFBAZG0CZqRraijzYQUkZH'

MARKET_URL = 'https://data.alpaca.markets'


def get_technical(ticker: str, indicator: str, start_date: str = None, end_date: str = None):

    # Get Data
    time_frame = '1D'

    bars_url = MARKET_URL + '/v1/bars/' + time_frame + '?symbols=' + ticker
    if start_date is not None:
        bars_url = bars_url + '&start=' + start_date
    if end_date is not None:
        bars_url = bars_url + '&end=' + end_date

    r = requests.get(bars_url, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    r = r.json()
    r = r[ticker]

    # Get Technical
    # Pricing Bar Data
    open = r[len(r)-1]['o']  # [len(r)-1] references most recent day
    high = r[len(r)-1]['h']
    low = r[len(r)-1]['l']
    close = r[len(r)-1]['c']
    volume = r[len(r)-1]['v']

    # Creating Dataframe from Pricing Bar Values
    d = {'Open': [], 'High': [], 'Low': [], 'Close': [], 'Volume': []}
    for day in r:
        d['Open'].append(day['o'])
        d['High'].append(day['h'])
        d['Low'].append(day['l'])
        d['Close'].append(day['c'])
        d['Volume'].append(day['v'])

    df = pd.DataFrame(data=d)

    if indicator == 'open':
        return open

    elif indicator == 'close':
        return close

    elif indicator == 'high':
        return high

    elif indicator == 'low':
        return low

    elif indicator == 'volume':
        return volume

    elif indicator == 'BB':  # Bollinger Band
        # indicator_bb = BollingerBands(close=df["Close"], n=len(r), ndev=2)

        bb_low = ta.volatility.bollinger_lband(df["Close"], n=len(r), ndev=2, fillna=True)
        bb_low = bb_low[len(r) - 1]

        bb_high = ta.volatility.bollinger_hband(df["Close"], n=len(r), ndev=2, fillna=True)
        bb_high = bb_high[len(r)-1]

        return bb_low, bb_high

    elif indicator == 'ATR':  # Average True Range
        output = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], n=len(r), fillna=True)
        return output[len(r)-1]

    elif indicator == 'RSI':  # Relative Strength Index
        output = ta.momentum.rsi(df["Close"], n=len(r), fillna=True)
        return output[len(r)-1]

    elif indicator == 'OBV':  # On-Balance Volume
        output = ta.volume.on_balance_volume(df["Close"], df["Volume"], fillna=True)
        return output[len(r)-1]

    elif indicator == 'MACD':  # Moving Average Convergence Divergence
        macd_proper = ta.trend.macd(df["Close"], n_fast=len(r), n_slow=len(r), fillna=True)
        macd_signal = ta.trend.macd_diff(df["Close"], n_fast=len(r), n_slow=len(r), fillna=True)
        macd_divergence = ta.trend.macd_signal(df["Close"], n_fast=len(r), n_slow=len(r), fillna=True)
        return macd_proper[len(r)-1], macd_signal[len(r)-1], macd_divergence[len(r)-1]

if __name__ == '__main__':
    x = get_technical('TSLA', 'MACD', '2020-09-21T09:30:00-04:00', '2020-09-25T09:30:00-04:00')
    print(x)
    print('signal: ', x[1])
    print('divergence: ', x[2])
