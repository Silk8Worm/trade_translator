import requests
import alpaca_trade_api as tradeapi

API_KEY = 'PK4W268R10HW802W8SN9'  # keys from alpaca
SECRET_API_KEY = 'oFK1SOul4uEqwj4phpdFBAZG0CZqRraijzYQUkZH'

PAPER_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(PAPER_URL)

MARKET_URL = 'https://data.alpaca.markets'
QUOTE_URL = '{}/v1/last_quote/stocks/AAPL'.format(MARKET_URL)  # quote for AAPL
STOCK = 'AAPL'
BARS_URL = ('{}/v1/bars/minute?symbols='+STOCK+'&limit=5').format(MARKET_URL)


def get_technical(ticker: str, indicator: str, startDate: str = None, endDate: str = None):

    # date takes form: 'yyyy-mm-dd'

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

    # print(ACCOUNT_URL)
    # r = requests.get(ACCOUNT_URL, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    # r = r.json()

    # print(QUOTE_URL)
    # r = requests.get(QUOTE_URL, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    # r = r.json()

    print(BARS_URL)
    r = requests.get(BARS_URL, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_API_KEY})
    r = r.json()

    # Prints the dictionary r
    # for x in r:
    #    print(x, r[x])

    i = r['AAPL']

    print('AAPL')
    for x in i:
        print(x)



