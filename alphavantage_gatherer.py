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


def get_technical(ticker: str, indicator: str, date: str = None, period: int = 1):
    # TODO: Closing prices and volume don't match online values
    # Get Data
    time_frame = '1D'

    bars_url = MARKET_URL + '/v1/bars/' + time_frame + '?symbols=' + ticker
    #  Obtain an additional day of data; some indicators calculate from previous day
    bars_url = bars_url + '&limit=' + str(period+1)
    if date is not None:
        bars_url = bars_url + '&end=' + date

    r = requests.get(bars_url, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    r = r.json()
    r = r[ticker]

    # Print obtained data
    for d in r:
        print(d)

    pass

    # Get Technical
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
        return r[len(r)-1]['o']

    elif indicator == 'close':
        return r[len(r)-1]['c']

    elif indicator == 'high':
        return r[len(r)-1]['h']

    elif indicator == 'low':
        return r[len(r)-1]['l']

    elif indicator == 'volume':
        return r[len(r)-1]['v']

    elif indicator == 'BB':  # Bollinger Band
        # indicator_bb = BollingerBands(close=df["Close"], n=len(r), ndev=2)

        bb_low = ta.volatility.bollinger_lband(df["Close"], n=len(r)-1, ndev=2, fillna=True)
        bb_low = bb_low[len(r) - 1]

        bb_high = ta.volatility.bollinger_hband(df["Close"], n=len(r)-1, ndev=2, fillna=True)
        bb_high = bb_high[len(r)-1]

        return bb_low, bb_high

    elif indicator == 'ATR':  # Average True Range
        output = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], n=period, fillna=True)
        return output[len(r)-1]

    elif indicator == 'RSI':  # Relative Strength Index
        output = ta.momentum.rsi(df["Close"], n=len(r)-1, fillna=True)
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
    x = get_technical('MSFT', 'ATR', '2020-09-25T09:30:00-04:00', 14)
    print('atr')
    print(x)

