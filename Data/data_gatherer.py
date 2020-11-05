import datetime
import numpy as np
import pandas_datareader as pdr
from pandas import Series
import ta
from ta.volatility import BollingerBands
import requests
import json

# ta documentation
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#volatility-indicators

TECHNICAL_DATABASE = {}  # dictionaries allow you to assume a key already exists
#  TECHNICAL_DATABASE[ticker][indicator][date][value] <- whats being used
#  TODO: Make pull_data search Database first
#  Alpaca does not not behave well with stock splits!!


def pull_technical_data(ticker: str, indicator: str, startdate: str, enddate: str, indicator_range_specification: int):

    # Handle dates with datetime
    startdate = datetime.datetime.strptime(startdate, '%d/%m/%Y')
    enddate = datetime.datetime.strptime(enddate, '%d/%m/%Y')

    # <firstdate> obtains extra days of data; some indicators calculate from preexisting values
    # obtains exactly <period> many extra days
    firstdate = np.busday_offset(startdate.isoformat()[:10], -(indicator_range_specification+20), roll='forward')

    if indicator == 'macd':
        # Special case for MACD
        if indicator_range_specification < 26:
            firstdate = np.busday_offset(startdate.isoformat()[:10], -(26+20), roll='forward')
        elif indicator_range_specification == 26:
            print('26 is invalid input')
            return
    elif indicator in ['high', 'low'] and indicator_range_specification != 1:
        # Special case for high and low
        year = startdate.year
        firstdate = startdate.replace(year=year-1)
        firstdate = np.datetime64(firstdate.strftime('%Y-%m-%d'))


    firstdate = datetime.datetime.strptime(str(firstdate), '%Y-%m-%d')

    # Fetch with pandas data reader
    df = pdr.get_data_yahoo(ticker, firstdate, enddate)
    # print(type(df)) # pandas dataframe data type

    # Cull <df> to sufficient size
    extra = 0
    dates = df.axes[0]

    if indicator in ['high', 'low'] and indicator_range_specification != 1:
        found_first = False
        duration = 0
        for date in dates:
            pointer = str(date)[:10]
            pointer = datetime.datetime.strptime(pointer, '%Y-%m-%d')

            # if pointer != firstdate:
            # print(pointer.day > firstdate.day)
            if found_first is False and pointer.day >= startdate.day and pointer.month >= startdate.month and pointer.year >= startdate.year:
                firstdate = pointer
                found_first = True

            if found_first:
                duration += 1

    else:
        for date in dates:
            pointer = str(date)[:10]
            pointer = datetime.datetime.strptime(pointer, '%Y-%m-%d')

            if pointer.day < startdate.day and pointer.month <= startdate.month and pointer.year <= startdate.year:
                extra += 1
            else:
                break

        duration = len(dates) - extra
        extra -= indicator_range_specification
        df = df[extra:]

    output = get_technical(indicator, indicator_range_specification, duration, df, startdate)

    # Update Database
    if ticker not in TECHNICAL_DATABASE:
        TECHNICAL_DATABASE[ticker] = {}

    TECHNICAL_DATABASE[ticker][indicator + ", " + str(indicator_range_specification)] = output
    return output


def get_technical(indicator: str, period: int, duration: int, df: str, startdate: datetime):

    # Get Technical Indicator
    if indicator == 'open':
        output = df['Open'][period:]

    elif indicator == 'close':
        output = df['Close'][period:]

    elif indicator == 'high':
        if period == 1:
            # Return the daily high
            output = df['High'][period:]
        else:
            # Return the highest price among the last period of days
            high = df['High']

            output = np.zeros(duration)

            for i in range(len(output)):
                output[i] = high[i:len(high)-duration+i].max()

            output = output.tolist()

    elif indicator == 'low':
        if period == 1:
            # Return the daily low
            output = df['Low'][period:]
        else:
            # Return the lowest price among the last period of days
            low = df['Low']

            output = np.zeros(duration)

            for i in range(len(output)):
                output[i] = low[i:len(low)-duration+i].min()

            output = output.tolist()

    elif indicator == 'volume':
        output = df['Volume'][period:]

    elif indicator in ['low bb', 'bb low', 'bbands low']:  # Lower Bollinger Band
        bb_low = ta.volatility.bollinger_lband(df["Close"][1:], n=period, ndev=2, fillna=True)
        output = bb_low[period-1:]

    elif indicator in ['high bb', 'bb high', 'bbands high']:  # Higher Bollinger Band
        bb_high = ta.volatility.bollinger_hband(df["Close"][1:], n=period, ndev=2, fillna=True)
        output = bb_high[period-1:]

    elif indicator == 'bbands':  # Bollinger Band Range
        high = get_technical('high bb', period, duration, df, startdate)
        low = get_technical('low bb', period, duration, df, startdate)

        difference = {}

        for key in high:
            difference[key] = high[key] - low[key]

        return difference

    elif indicator == 'atr':  # Average True Range
        high = df['High'][1:]
        low = df['Low'][1:]
        close = df['Close'][1:]
        tr = np.zeros(len(close))
        atr = np.zeros(len(close))

        # Prime the first true range values
        tr[0] = high[0] - low[0]
        # Obtain values for the rest of the true range
        for i in range(1, len(tr)):
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))

        # Obtain values for average true range
        for i in range(period - 1, len(atr)):
            atr[i] = tr[i - period + 1:i + 1].mean()

        output = atr.tolist()[period-1:]

    elif indicator == 'rsi':  # Relative Strength Index
        close = df['Close']

        today_gain = np.zeros(len(close))
        today_loss = np.zeros(len(close))
        avg_gain = np.zeros(len(close))
        avg_loss = np.zeros(len(close))
        rs = np.zeros(len(close))
        rsi = np.zeros(len(close))

        # Compute Gain and Loss of Each Day
        for i in range(1, len(close)):
            diff = close[i] - close[i - 1]
            if diff > 0:
                today_gain[i] = diff
            else:
                today_loss[i] = abs(diff)

        # Compute Average Gain/Loss
        for i in range(period, len(close)):
            x = today_gain[i - (period - 1):i + 1]
            y = today_loss[i - (period - 1):i + 1]

            count = 0
            for value in x:
                if value != 0:
                    avg_gain[i] += value
                    count += 1
            avg_gain[i] /= count

            count = 0
            for value in y:
                if value != 0:
                    avg_loss[i] += value
                    count += 1

            if avg_loss[i] == 0:
                # Edge Case, avoid division by zero
                rsi[i] = 100
            else:
                # Standard Case
                avg_loss[i] /= count

                rs[i] = avg_gain[i] / avg_loss[i]
                rsi[i] = 100 - 100 / (1 + rs[i])

        output = rsi.tolist()[period:]

    elif indicator == 'obv':  # On-Balance Volume
        close = df['Close'][period:]
        volume = df['Volume'][period:]

        obv = np.zeros(len(close))

        # Prime the first OBV value
        obv[0] = 0
        for i in range(1, len(obv)):
            if close[i] > close[i - 1]:
                obv[i] = obv[i - 1] + volume[i]
            elif close[i] < close[i - 1]:
                obv[i] = obv[i - 1] - volume[i]
            else:
                obv[i] = obv[i - 1]

        output = obv.tolist()

    elif indicator == 'ema':  # Exponential Moving Average
        close = df['Close']

        ema = np.zeros(len(close))
        multiplier = 2 / (period + 1)
        multiplier = multiplier / (1 + period)

        # Prime the first EMA values as the previous SMA
        ema[period] = close[:period].mean()

        # Compute the rest of the EMA values
        for i in range(period + 1, len(ema)):
            ema[i] = close[i] * multiplier + ema[i - 1] * (1 - multiplier)

        output = ema.tolist()[period:]

    elif indicator == 'macd':  # Moving Average Convergence Divergence
        other_startdate = np.busday_offset(startdate.isoformat()[:10], -(abs(26-period)), roll='forward', holidays=HOLIDAYS_LIST)
        other_startdate = datetime.datetime.strptime(str(other_startdate), '%Y-%m-%d')

        macd = {}

        if period < 26:
            ema26 = get_technical('ema', 26, duration, df, startdate)
            other_ema = get_technical('ema', period, duration, df, other_startdate)

            for key in ema26:
                macd[key] = other_ema[key] - ema26[key]
        else:
            ema26 = get_technical('ema', 26, duration, df, other_startdate)
            other_ema = get_technical('ema', period, duration, df, startdate)

            for key in other_ema:
                macd[key] = ema26[key] - other_ema[key]

        return macd

    elif indicator == 'sma':  # Simply Moving Average
        close = df['Close'][1:]

        sma = np.zeros(len(close))

        # Compute the SMA
        for i in range(period-1, len(sma)):
            sma[i] = close[i - period + 1:i+1].mean()

        output = sma.tolist()[period-1:]

    # Return in dictionary with mapping [date:value]
    data = {}

    if isinstance(output, Series):
        output = Series.tolist(output)
    # <output> is a list

    dates = df.axes[0][period:]

    if indicator in ['high', 'low'] and period != 1:
        # Special case for period high/low
        dates = df.axes[0][len(df)-len(output):]

    for i in range(len(dates)):
        date = dates[i].isoformat()[:10]
        date = datetime.datetime.strptime(str(date), '%Y-%m-%d')
        date = date.strftime('%d/%m/%Y')
        data[date] = output[i]

    return data


def pull_fundamental_data(ticker: str, indicator: str, start_date_pre: str, end_date_pre: str):
    start_date = datetime.datetime.strptime(start_date_pre, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end_date_pre, '%d/%m/%Y')

    # TODO: Delete this, just temporary
    balance_sheet = json.loads(requests.get('https://tranquil-beyond-74281.herokuapp.com/info/tt/statements/'+ticker+'/balance/').text)
    income_statement = json.loads(requests.get('https://tranquil-beyond-74281.herokuapp.com/info/tt/statements/'+ticker+'/income/').text)
    cash_flow_statement = json.loads(requests.get('https://tranquil-beyond-74281.herokuapp.com/info/tt/statements/'+ticker+'/cash/').text)

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

    r = requests.post('https://tranquil-beyond-74281.herokuapp.com/info/tt/price/', data={"tickers":ticker, "start":start_date_pre, "end":end_date_pre})
    prices_j = r.json()
    prices = {}
    for key, value in prices_j.items():
        prices[datetime.datetime.strptime(key, '%d/%m/%Y')] = value

    temp_date = start_date

    output = {}

    # Passing the appropriate dictionary of values
    while temp_date <= end_date:
        output[temp_date.strftime("%d/%m/%Y")] = get_fundamental(temp_date, indicator, bs_dict, in_dict, cf_dict, prices)
        temp_date += datetime.timedelta(days=1)

    return output


def get_fundamental(date: datetime, indicator: str, bal, inc, cash, prices):

    correct_bs, previous_bs, correct_is, previous_is, correct_cf, previous_cf = \
        {}, {}, {}, {}, {}, {}

    # Finding the correct financial statements for date
    for i in range(len(bal)-1):
        date_check = list(bal.keys())[i]
        if datetime.datetime.strptime(date_check, '%Y-%m-%d') < date:
            correct_bs = bal[date_check]
            previous_bs = bal[list(bal.keys())[i+1]]
            break
    for i in range(len(inc)-1):
        date_check = list(inc.keys())[i]
        if datetime.datetime.strptime(date_check, '%Y-%m-%d') < date:
            correct_is = inc[date_check]
            previous_is = inc[list(inc.keys())[i+1]]
            break
    for i in range(len(cash)-1):
        date_check = list(cash.keys())[i]
        if datetime.datetime.strptime(date_check, '%Y-%m-%d') < date:
            correct_cf = cash[date_check]
            previous_cf = cash[list(cash.keys())[i+1]]
            break
    if correct_bs == {} or correct_is == {} or correct_cf == {}:
        return 0

    for key, value in correct_bs.items():
        if value is None:
            correct_bs[key] = 0
    for key, value in correct_is.items():
        if value is None:
            correct_is[key] = 0
    for key, value in correct_cf.items():
        if value is None:
            correct_cf[key] = 0

    try:
        if indicator == "":
            return 'temporary'
        elif indicator == 'ebitda':
            return correct_is['operatingIncome'] + correct_cf['depreciation']
        elif indicator == 'ebitda growth':
            this_year = correct_is['operatingIncome'] + correct_cf['depreciation']
            last_year = previous_is['operatingIncome'] + previous_cf['depreciation']
            return (this_year-last_year)/last_year
        elif indicator == 'leverage ratio':
            return ((previous_bs['totalAssets']+correct_bs['totalAssets'])/2)/((previous_bs['shareholderEquity']+correct_bs['shareholderEquity'])/2)
        elif indicator == 'net debt to ebitda':
            return (correct_bs['totalLiabilities'] - correct_bs['currentCash']) / (correct_is['operatingIncome'] + correct_cf['depreciation'])
        elif indicator == 'operating margin':
            return correct_is['operatingIncome'] / correct_is['totalRevenue']
        elif indicator == 'revenue growth':
            return (correct_is['totalRevenue'] - previous_is['totalRevenue']) / previous_is['totalRevenue']

        #TODO: Ryan plz add
        elif indicator == 'debt to equity':
            return (correct_bs['currentLongTermDebt'] + correct_bs['longTermDebt']) / correct_bs['shareholderEquity']
        elif indicator == 'debt to assets':
            return (correct_bs['currentLongTermDebt'] + correct_bs['longTermDebt']) / correct_bs['totalAssets']
        elif indicator == 'cash debt coverage ratio':
            return correct_cf['cashFlow'] / ((correct_bs['totalLiabilities'] + previous_bs['totalLiabilities'])/2)
        elif indicator == 'eps':
            return correct_is['netIncomeBasic'] / correct_bs['commonStock']
        elif indicator == 'eps growth':
            return ((correct_is['netIncomeBasic'] / correct_bs['commonStock']) - (previous_is['netIncomeBasic'] / previous_bs['commonStock']))/(previous_is['netIncomeBasic'] / previous_bs['commonStock'])
        elif indicator == 'gross margin':
            return correct_is['grossProfit'] / correct_is['totalRevenue']
        elif indicator == 'profit margin':
            return correct_is['netIncome'] / correct_is['totalRevenue']
        elif indicator == 'roe':
            return correct_is['netIncome'] / ((correct_bs['shareholderEquity'] + previous_bs['shareholderEquity'])/2)
        elif indicator == 'roa':
            return correct_is['netIncome'] / ((correct_bs['totalAssets'] + previous_bs['totalAssets'])/2)
        elif indicator == 'current ratio':
            return correct_bs['currentAssets'] / correct_bs['totalCurrentLiabilities']
        elif indicator == 'quick ratio':
            return (correct_bs['currentCash'] + correct_bs['shortTermInvestments'] + correct_bs['receivables']) / correct_bs['totalCurrentLiabilities']
        elif indicator == 'payout ratio':
            return correct_cf['dividendsPaid'] / correct_is['netIncome']
        elif indicator == 'revenue per share':
            return correct_is['totalRevenue'] / correct_bs['commonStock']
        elif indicator == 'net income growth':
            return (correct_is['netIncome'] - previous_is['netIncome'])/previous_is['netIncome']
        elif indicator == 'revenue':
            return correct_is['totalRevenue']
        elif indicator == 'book value to share':
            return correct_bs['shareholderEquity'] / correct_bs['commonStock']
        elif indicator == 'price to book value':
            try:
                return prices[date] / (correct_bs['shareholderEquity'] / correct_bs['commonStock'])
            except KeyError:
                return 0
        elif indicator == 'price to revenue':
            try:
                return prices[date] * correct_bs['commonStock'] / correct_is['totalRevenue']
            except KeyError:
                return 0
        elif indicator == 'dividend yield':
            try:
                return (correct_cf['dividendsPaid'] / correct_bs['commonStock']) / prices[date]
            except KeyError:
                return 0
        elif indicator == 'price to sales':
            try:
                return prices[date] / (correct_is['totalRevenue'] / correct_bs['commonStock'])
            except KeyError:
                return 0
        elif indicator == 'price to earnings':
            try:
                return prices[date] / (correct_is['netIncomeBasic'] / correct_bs['commonStock'])
            except KeyError:
                return 0
        elif indicator == 'short interest':
            return 0
        else:
            return 0
    except ZeroDivisionError:
        return 0


def get_data(tickers: list, indicator: str, start_date: str, end_date: str, period: int):

    indicator = indicator.lower()

    data_dict = {}
    technical_indicators = ['open', 'close', 'high', 'low', 'volume', 'low bb',
                            'bb low', 'high bb', 'bb high', 'bbands', 'atr', 'rsi', 'obv',
                            'ema', 'macd', 'proper macd', 'macd proper',
                            'signal macd', 'macd signal', 'divergent macd',
                            'macd divergent', 'sma', 'bbands']
    fundamental_indicators = ['eps', 'book value to share',
                              'dividend yield', 'ebitda growth', 'eps growth',
                              'leverage ratio', 'ebitda',
                              'net debt to ebitda', 'operating margin',
                              'price to book value', 'price to revenue',
                              'revenue growth', 'short interest', # Short interest only returns 0, revenue growth not added to lexer parser
                              #TODO: To be added
                              'debt to equity', 'debt to assets', 'cash debt coverage ratio',
                              'eps', 'gross margin', 'profit margin', 'roe', 'roa',
                              'current ratio', 'quick ratio', 'payout ratio',
                              'revenue per share', 'price to sales', 'price to earnings',
                              # The two below have not been added as valid indicators on the lexer parser side
                              'net income growth', 'revenue']

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
    x = get_data(['NFLX'], 'macd', '01/11/2019', '03/11/2019', 365)

    print('Data from <x>')
    for date in x:
        print(date)
        for stock in x[date]:
            print(stock, x[date][stock])
        print('-----')

