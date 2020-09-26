import requests


API_KEY = 'PK4W268R10HW802W8SN9'  # keys from alpaca
SECRET_API_KEY = 'oFK1SOul4uEqwj4phpdFBAZG0CZqRraijzYQUkZH'

MARKET_URL = 'https://data.alpaca.markets'


def get_technical(ticker: str, indicator: str = None, startDate: str = None, endDate: str = None):

    timeframe = 'minute'
    bars_url = MARKET_URL + '/v1/bars/' + timeframe + '?symbols=' + ticker + '&limit=1'
    # bars_url = ('{}/v1/bars/minute?symbols=' + ticker + '&limit=1').format(MARKET_URL)

    r = requests.get(bars_url, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    r = r.json()
    r = r[ticker][0]

    # Pricing Bar Data
    open = r['o']
    high = r['h']
    low = r['l']
    close = r['c']
    volume = r['v']

    print('open: \t', open)
    print('high: \t', high)
    print('low: \t', low)
    print('close: \t', close)
    print('volume: \t', volume)

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

    elif indicator == 'moving average':
        pass

    elif indicator == 'exponential moving average':
        pass

    elif indicator == 'bollinger band':
        pass

    elif indicator == 'ATR':
        pass

    elif indicator == 'RSI':
        pass

    elif indicator == 'OBV':
        pass

    elif indicator == 'MACD':
        pass


if __name__ == '__main__':
    get_technical('TSLA')
