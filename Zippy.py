from src import AST, signalparse, singallex
import ply.yacc as yacc
import logging

def zippy(signal,trade,cover_signal,universe,take_profit,stop_loss,cover_trade):
    print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

    # TODO Ryan, can you find a way to split the universe into a list of stocks
    start_date = "01/01/2020"
    end_date = "03/01/2020"
    universe = "AAPL,MSFT,GOOG"
    tickers = universe.split(',')
    print(tickers)

    signalparse.create_tree(start_date, end_date, ["AAPL", "TSLA", "GOOG"], "if 5 day bollinger bands greater than 20")

    try:
        print(signalparse.create_tree(start_date, end_date, ["AAPL", "TSLA", "GOOG"], 'if rsi greater than 70 or 10 day macd crosses below 60'))
    except Exception:
        print(Exception.__name__)


    return 5000, 10000, 1.4, 2.3, [1,2,3], [1,4,9]

zippy('if rsi greater than 70 or 10 day macd crosses below 60', 'buy 10', 'if rsi less than 56.1', ['AAPL', 'TSLA', 'GOOG'], .05, .02, 'sell 10')
