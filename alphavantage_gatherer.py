from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData

import requests

api_key = 'UD9DGIGLSXX7YVK7'  # api key from alpha vantage


def get_technical(ticker: str, indicator: str, startDate: str = None, endDate: str = None):

    # date takes form: 'yyyy-mm-dd'

    url = 'https://www.alphavantage.co/query?'

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
        url += "function=OVERVIEW"
        url += "&symbol=" + ticker
        url += "&apikey=" + api_key

        r = requests.get(url)
        return r.json()['52WeekHigh']

    elif indicator == '52 week low':
        url += "function=OVERVIEW"
        url += "&symbol=" + ticker
        url += "&apikey=" + api_key

        r = requests.get(url)
        return r.json()['52WeekLow']

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
    ts = TimeSeries(key=api_key)
    ti = TechIndicators(key=api_key)
    fd = FundamentalData(key=api_key)

    # r = requests.get('https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=close&apikey=UD9DGIGLSXX7YVK7')
    # r = requests.get('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=GOOGL&apikey=UD9DGIGLSXX7YVK7')
    # r = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=UD9DGIGLSXX7YVK7')
    # print(r.json())

    # print(r.json['EBITDA'])

    print(get_technical('IBM', '52 week high'))
    print(get_technical('IBM', '52 week low'))

