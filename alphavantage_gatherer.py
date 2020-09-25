import requests
import alpaca_trade_api as tradeapi

API_KEY = 'PK4W268R10HW802W8SN9'  # keys from alpaca
SECRET_API_KEY = 'oFK1SOul4uEqwj4phpdFBAZG0CZqRraijzYQUkZH'

MARKET_URL = 'https://data.alpaca.markets'


def get_technical(ticker: str, indicator: str = None, startDate: str = None, endDate: str = None):

    bars_url = ('{}/v1/bars/minute?symbols=' + ticker + '&limit=1').format(MARKET_URL)
    r = requests.get(bars_url, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    r = r.json()
    r = r[ticker]

    # Pricing Bar Data
    open = r[0]['o']
    high = r[0]['h']
    low = r[0]['l']
    close = r[0]['c']
    volume = r[0]['v']

    print('open: \t', open)
    print('high: \t', high)
    print('low: \t', low)
    print('close: \t', close)
    print('volume: \t', volume)

    pass

    if indicator == 'average daily volume':
        pass

    elif indicator == 'basic earnings per share':
        pass

    elif indicator == 'book value per share':
        pass

    elif indicator == 'dividend yield':
        pass

    elif indicator == 'ebitda growth':
        pass

    elif indicator == 'eps growth':
        pass

    elif indicator == '52 week high':
        pass

    elif indicator == '52 week low':
        pass

    elif indicator == 'forward dividend rate':
        pass

    elif indicator == 'leverage ratio':
        pass

    elif indicator == 'net debt to ebitda':
        pass

    elif indicator == 'operating margin':
        pass

    elif indicator == 'price to book value':
        pass

    elif indicator == 'price to earnings':
        pass

    elif indicator == 'price to next year forecasted earnings':
        pass

    elif indicator == 'price to revenue':
        pass

    elif indicator == 'revenue growth':
        pass

    elif indicator == 'short interest':
        pass

if __name__ == '__main__':
    get_technical('AAPL')