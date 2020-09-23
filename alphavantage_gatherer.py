from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData

api_key = 'EWWCPP3EGVVECDSZ'  # api key from alpha vantage


def get_technical(ticker: str, indicator: str, startDate: str = None, endDate: str = None):

    # date takes form: 'yyyy-mm-dd'

    ts = TimeSeries(key=api_key)
    ti = TechIndicators(key=api_key)

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
    ts = TimeSeries(key=api_key)
    ti = TechIndicators(key=api_key)
    fd = FundamentalData(key=api_key)

    data, meta_data = fd.get_balance_sheet_annual(symbol="AAPL")

    print(data)
    print('')
    print(meta_data)
