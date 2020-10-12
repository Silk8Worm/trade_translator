"""

#TODO IMPORTANT: SET SANDBOX TO FALSE IF YOU WANT TO USE A REAL API TOKEN

Need to "pip install requests" in command prompt and install package

install by opening the Settings window, and doing the following:
Open Project: csc148 -> Project Intepreter.
Ensure that you have Python 3.8 selected in the “Project Intepreter” dropdown.
Press the green “+” icon, and type in requests
Select the package, and press “Install Package”.

"""

from typing import Dict, Optional
import requests
import json

SANDBOX = True


def cash_flow_statement(api_key: str, ticker: str, period: Optional[str] = 'quarter', num_periods: Optional[int] = 1) -> Dict:
    """
    Used for sending an HTTP request for the JSON response provided by IEX Cloud

    api_key: must be a valid api token for IEX cloud to take
    ticker: must be a valid ticker that exists within the iex cloud
    period: optional parameter specifying peiod of balance sheet. Must be either
        "annual" or "quarter"
        - default value is quarter
    num_periods: the number of periods that you want data for
        - Maximum 12 quarters or 4 years
        - default value is 1
    """

    if not SANDBOX:
        sand = 'cloud'
    else:
        sand = 'sandbox'

    url = f'https://{sand}.iexapis.com/stable/stock/{ticker}/cash-flow?'
    if period == "annual":
        url += 'period=annual&'
    if period == "annual":
        if num_periods < 5:
            url += f'last={num_periods}&'
    elif num_periods < 13:
        url += f'last={num_periods}&'
    else:
        print("Cannot request that many periods. Please read method description.")
    url += f'token={api_key}'

    # r represents the data that the website returns. I can edit it/scrape it however you'd like.
    # it is also in a JSON format which is held as a dictionary by python
    r = requests.get(url)
    return r.json()



def balance_sheet(api_key: str, ticker: str, period: Optional[str] = 'quarter', num_periods: Optional[int] = 1) -> Dict:
    """
    Used for sending an HTTP request for the JSON response provided by IEX Cloud

    api_key: must be a valid api token for IEX cloud to take
    ticker: must be a valid ticker that exists within the iex cloud
    period: optional parameter specifying peiod of balance sheet. Must be either
        "annual" or "quarter"
        - default value is quarter
    num_periods: the number of periods that you want data for
        - Maximum 12 quarters or 4 years
        - default value is 1
    """

    if not SANDBOX:
        sand = 'cloud'
    else:
        sand = 'sandbox'

    url = f'https://{sand}.iexapis.com/stable/stock/{ticker}/balance-sheet?'
    if period == "annual":
        url += 'period=annual&'
    if period == "annual":
        if num_periods < 5:
            url += f'last={num_periods}&'
    elif num_periods < 13:
        url += f'last={num_periods}&'
    else:
        print("Cannot request that many periods. Please read method description.")
    url += f'token={api_key}'

    # r represents the data that the website returns. I can edit it/scrape it however you'd like.
    # it is also in a JSON format which is held as a dictionary by python
    r = requests.get(url)
    print(url)
    return r.json()

def income_statement(api_key: str, ticker: str, period: Optional[str] = 'quarter', num_periods: Optional[int] = 1) -> Dict:
    """
    Used for sending an HTTP request for the JSON response provided by IEX Cloud

    api_key: must be a valid api token for IEX cloud to take
    ticker: must be a valid ticker that exists within the iex cloud
    period: optional parameter specifying peiod of balance sheet. Must be either
        "annual" or "quarter"
        - default value is quarter
    num_periods: the number of periods that you want data for
        - Maximum 12 quarters or 4 years
        - default value is 1
    """

    if not SANDBOX:
        sand = 'cloud'
    else:
        sand = 'sandbox'

    url = f'https://{sand}.iexapis.com/stable/stock/{ticker}/income?'
    if period == "annual":
        url += 'period=annual&'
    if period == "annual":
        if num_periods < 5:
            url += f'last={num_periods}&'
    elif num_periods < 13:
        url += f'last={num_periods}&'
    else:
        print("Cannot request that many periods. Please read method description.")
    url += f'token={api_key}'

    # r represents the data that the website returns. I can edit it/scrape it however you'd like.
    # it is also in a JSON format which is held as a dictionary by python
    r = requests.get(url)
    return r.json()

