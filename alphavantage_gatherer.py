import requests
import datetime
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from pandas import Series
import ta
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.trend import MACD
from ta.trend import EMAIndicator
import Financial_Statement_Calling as call

# ta documentation
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#volatility-indicators

API_KEY = 'PK4W268R10HW802W8SN9'  # keys from alpaca
SECRET_API_KEY = 'oFK1SOul4uEqwj4phpdFBAZG0CZqRraijzYQUkZH'
MARKET_URL = 'https://data.alpaca.markets'

TECHNICAL_DATABASE = {}  # dictionaries allow you to assume a key already exists
#  TECHNICAL_DATABASE[ticker][indicator][date][value] <- whats being used
#  TODO: Make pull_data search Database first
#  TODO: Make Database behave well with holidays
#  Alpaca does not not behave well with stock splits!!


def pull_technical_data(ticker: str, indicator: str, startdate: str, enddate: str, indicator_range_specification: int):

    # Handle dates with datetime
    startdate = datetime.datetime.strptime(startdate, '%d/%m/%Y')
    enddate = datetime.datetime.strptime(enddate, '%d/%m/%Y')
    duration = np.busday_count(startdate.isoformat()[:10], enddate.isoformat()[:10]) + 1

    # <firstdate> obtains extra days of data; some indicators calculate from preexisting values
    firstdate = np.busday_offset(startdate.isoformat()[:10], -(indicator_range_specification-1), roll='forward')
    firstdate = datetime.datetime.strptime(str(firstdate), '%Y-%m-%d')

    # Fetch with pandas data reader
    df = pdr.get_data_yahoo(ticker, firstdate, enddate)
    # print(type(df)) # pandas dataframe data type

    output = get_technical(indicator, indicator_range_specification, duration, df, startdate)

    # Update Database
    if ticker not in TECHNICAL_DATABASE:
        TECHNICAL_DATABASE[ticker] = {}

    TECHNICAL_DATABASE[ticker][indicator + ", " + str(indicator_range_specification)] = output
    return output


def get_technical(indicator: str, period: int, duration: int, df: str, startdate: datetime):

    # Get Technical Indicator
    if indicator == 'open':
        output = df['Open'][period-1:]
        print(output)

    elif indicator == 'close':
        output = df['Close'][period-1:]

    elif indicator == 'high':
        output = df['High'][period-1:]

    elif indicator == 'low':
        output = df['Low'][period-1:]

    elif indicator == 'volume':
        output = df['Volume'][period-1:]

    elif indicator in ['low BB', 'BB low']:  # Lower Bollinger Band
        bb_low = ta.volatility.bollinger_lband(df["Close"], n=period, ndev=2, fillna=True)
        output = bb_low[len(bb_low)-duration-1:]

    elif indicator in ['high BB', 'BB high']:  # Higher Bollinger Band
        bb_high = ta.volatility.bollinger_hband(df["Close"], n=period, ndev=2, fillna=True)
        output = bb_high[len(bb_high) - duration-1:]

    elif indicator == 'ATR':  # Average True Range
        atr = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], n=period, fillna=True)
        output = atr[len(atr)-duration-1:]

    elif indicator == 'RSI':  # Relative Strength Index  # TODO: verify
        rsi = ta.momentum.rsi(df["Close"], n=period, fillna=True)
        output = rsi[len(rsi)-duration-1:]

    elif indicator == 'OBV':  # On-Balance Volume
        obv = ta.volume.on_balance_volume(df["Close"][4:], df["Volume"][4:], fillna=True)  # Splice Redundant Data
        output = obv[len(obv)-duration-1:]

    elif indicator == 'EMA':  # Exponential Moving Average  # TODO: verify
        ema = ta.trend.ema_indicator(df["Close"], n=period, fillna=True)
        output = ema[len(ema)-duration-1:]

    elif indicator == 'MACD':  # Moving Average Convergence Divergence  # TODO: verify
        ema1 = ta.trend.ema_indicator(df["Close"], n=period/2, fillna=True)
        ema2 = ta.trend.ema_indicator(df["Close"], n=period, fillna=True)
        ema1 = Series.tolist(ema1)
        ema2 = Series.tolist(ema2)
        output = []
        for i in range(len(ema1)):
            output.append(ema1[i]-ema2[i])
        output = output[len(output) - duration-1:]

    elif indicator in ['proper MACD', 'MACD proper']:
        macd_proper = ta.trend.macd(df["Close"], n_fast=period, n_slow=period, fillna=True)
        output = macd_proper[len(macd_proper) - duration-1:]

    elif indicator in ['signal MACD', 'MACD signal']:
        macd_signal = ta.trend.macd_diff(df["Close"], n_fast=period, n_slow=period, fillna=True)
        output = macd_signal[len(macd_signal) - duration-1:]

    elif indicator in ['divergent MACD', 'MACD divergent']:
        macd_divergence = ta.trend.macd_signal(df["Close"], n_fast=period, n_slow=period, fillna=True)
        output = macd_divergence[len(macd_divergence) - duration-1:]

    # Return in dictionary with mapping [date:value]
    data = {}

    # TODO: Rewrite this to use the row as keys
    if isinstance(output, Series):
        output = Series.tolist(output)
    # <output> is a list
    key = startdate  # <key> is a datetime object
    friday = False
    for i in range(0, len(output)):
        left = np.busday_offset(key, 1, roll='backward')  # TODO: I think this is suppose to be 'forward'
        right = key + datetime.timedelta(days=1)
        if not (left == right):
            # <key is a friday>
            friday = True
        # keys are strings, if you want datetime object as key then remove .isoformat()
        data[key.strftime("%d/%m/%Y")] = output[i]
        key = key + datetime.timedelta(days=1)
        if friday:
            # Set key to next business day
            # key = np.busday_offset(key, 1, roll='backward')
            key = key + datetime.timedelta(days=2)  # TODO: Use <busday>, this is bad with holidays and 3-day weekends
            friday = False

    return data


def pull_fundamental_data(ticker: str, indicator: str, start_date: str, end_date: str):
    api_key = "Tpk_6ef4a75d2a6f4d95be047b5629cf964f"

    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')

    # TODO: Delete this, just temporary
    balance_sheet = call.balance_sheet(api_key, ticker, num_periods=12)
    income_statement = call.income_statement(api_key, ticker, num_periods=12)
    cash_flow_statement = call.cash_flow_statement(api_key, ticker, num_periods=12)

    bs_dict = {}
    in_dict = {}
    cf_dict = {}

    # Converting data into a dictionary with date keys
    for item in balance_sheet['balancesheet']:
        bs_dict[item['reportDate']] = item
    for item in income_statement['income']:
        in_dict[item['reportDate']] = item
    for item in cash_flow_statement['cashflow']:
        cf_dict[item['reportDate']] = item

    temp_date = start_date

    output = {}

    # Passing the appropriate dictionary of values
    while temp_date <= end_date:
        output[temp_date.strftime("%d/%m/%Y")] = get_fundamental(temp_date, indicator, bs_dict, in_dict, cf_dict)
        temp_date += datetime.timedelta(days=1)

    return output


def get_fundamental(date: datetime, indicator: str, bal, inc, cash):

    correct_bs, previous_bs, correct_is, previous_is, correct_cf, previous_cf = \
        {}, {}, {}, {}, {}, {}

    # Finding the correct financial statements for date
    for i in range(len(bal)):
        date_check = list(bal.keys())[i]
        if datetime.datetime.strptime(date_check, '%Y-%m-%d') < date:
            correct_bs = bal[date_check]
            previous_bs = bal[list(bal.keys())[i+1]]
            break
    for i in range(len(inc)):
        date_check = list(inc.keys())[i]
        if datetime.datetime.strptime(date_check, '%Y-%m-%d') < date:
            correct_is = inc[date_check]
            previous_is = inc[list(inc.keys())[i+1]]
            break
    for i in range(len(cash)):
        date_check = list(cash.keys())[i]
        if datetime.datetime.strptime(date_check, '%Y-%m-%d') < date:
            correct_cf = cash[date_check]
            previous_cf = cash[list(cash.keys())[i+1]]
            break

    # print(correct_bs)
    # print(correct_is)
    # print(correct_cf)

    #TODO: Need shares oustanding for calculations
    if indicator == "":
        return 'temporary'
    #
    # if indicator == 'EPS':
    #    return (correct_is['netIncome'] + correct_cf['dividendsPaid'])/ num_shares
    # elif indicator == 'book value/share':
    #    return (correct_bs['shareholderEquity'] - pref_equity)/ num_shares
    # elif indicator == 'dividend yield':
    #    return dividendsPaid / stock_price
    elif indicator == 'EBITDA':
        return correct_is['operatingIncome'] + correct_cf['depreciation']
    elif indicator == 'EBITDA growth':
        this_year = correct_is['operatingIncome'] + correct_cf['depreciation']
        last_year = previous_is['operatingIncome'] + previous_cf['depreciation']
        return (this_year-last_year)/last_year
    # elif indicator == 'EPS growth':
    #
    elif indicator == 'leverage ratio':
        return correct_bs['totalLiabilities']/correct_bs['shareholderEquity']
    elif indicator == 'net debt/EBITDA':
        return (correct_bs['totalLiabilities'] - correct_bs['currentCash']) / (correct_is['operatingIncome'] + correct_cf['depreciation'])
    elif indicator == 'operating margin':
        return correct_is['operatingIncome'] / correct_is['totalRevenue']
    # elif indicator == 'price/book value':
    #    return stock_price / (correct_bs['shareholderEquity'] - pref_equity)
    # elif indicator == 'price/earnings':
    #    return stock_price / ((correct_is['netIncome'] + correct_cf['dividendsPaid'])/ num_shares)
    # elif indicator == 'price/revenue':
    #    return stock_price / correct_is['totalRevenue']
    elif indicator == 'revenue growth':
        return (correct_is['totalRevenue'] - previous_is['totalRevenue']) / previous_is['totalRevenue']
    # elif indicator == 'short interest':
    #   return num_shorted_shares / num_shares
    else:
        return None


def get_data(tickers: list, indicator: str, start_date: str, end_date: str, period: int):

    data_dict = {}
    technical_indicators = ['open', 'close', 'high', 'low', 'volume', 'low BB',
                            'BB low', 'high BB', 'BB high', 'ATR', 'RSI', 'OBV',
                            'EMA', 'MACD', 'proper MACD', 'MACD proper',
                            'signal MACD', 'MACD signal', 'divergent MACD',
                            'MACD divergent']
    fundamental_indicators = ['EPS', 'book value/share',
                              'dividend yield', 'EBITDA growth', 'EPS growth',
                              'leverage ratio', 'EBITDA',
                              'net debt/EBITDA', 'operating margin',
                              'price/book value', 'price/earnings','price/revenue',
                              'revenue growth', 'short interest']

    if indicator in fundamental_indicators:
        for ticker in tickers:
            data_dict[ticker] = pull_fundamental_data(ticker, indicator, start_date, end_date)
    else:
        for ticker in tickers:
            data_dict[ticker] = pull_technical_data(ticker, indicator, start_date, end_date, period)

    output = {}

    for ticker, data in data_dict.items():
        for date, value in data.items():
            output[date] = {}

    for ticker, data in data_dict.items():
        for date, value in data.items():
            output[date][ticker] = value
    return output


if __name__ == '__main__':
    # get_data(['AAPL'], 'BB low', '09/09/2020', '25/09/2020', 5)
    # get_data(['AAPL'], 'BB high', '20/09/2020', '25/09/2020', 10)
    # get_data(['PTON'], 'ATR', '14/09/2020', '29/09/2020', 20)

    print(get_data(['AAPL', 'MSFT'], 'open', '07/10/2020', '09/10/2020', 5))
    print('end.')
    # for date in x:
        # print(date, x[date])

