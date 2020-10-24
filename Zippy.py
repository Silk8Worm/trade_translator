from LexerParser.src.AST import *
from LexerParser.src.signalparse import build_ast
from datetime import datetime
import backtrader as bt
from PIL import Image
"""
IF A TRADE WOULD GIVE THE USER A NEGATIVE CASH BALANCE, THE TRADE DOES
NOT EXECUTE.
"""

def zippy(signal: str, trade: str, amt: str, cover_signal: str, universe: str,
          t_profit: str, s_loss: str, cover_trade: str, cover_amt: str,
          first_date: str, second_date: str):

    ticker_list = ['TSLA', 'MSFT', 'GOOG', 'AAPL']

    global start_date
    global end_date
    global start_date_pre
    global end_date_pre
    global buy_bool
    global cover_buy_bool
    global amount
    if amt == "":
        amount = 0
    else:
        amount = int(amt)
    global cover_amount
    if cover_amt == "":
        cover_amount = 0
    else:
        cover_amount = int(cover_amt)
    global starting_cash
    starting_cash = 500000.0
    global state
    global ast
    global cover_ast
    global main_signal
    main_signal = signal
    global other_signal
    other_signal = cover_signal
    global take_profit
    if t_profit == "":
        take_profit=1000
    else:
        take_profit = float(t_profit)/100
    global stop_loss
    if s_loss == "":
        stop_loss=1000
    else:
        stop_loss = float(s_loss)/100
    if trade == 'Sell':
        buy_bool = False
    else:
        buy_bool = True

    if cover_trade == 'Sell':
        cover_buy_bool = False
    else:
        cover_buy_bool = True

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(starting_cash)
    cerebro.broker.setcommission(0)


    start_date_pre = first_date
    start_date = datetime.strptime(start_date_pre, '%d/%m/%Y')
    end_date_pre = second_date
    end_date = datetime.strptime(end_date_pre, '%d/%m/%Y')

    if universe == '':
        return 'No Tickers Entered', "Universe", [], None
    tickers_pre = universe.split(',')
    tickers = [x.strip() for x in tickers_pre]
    invalid_tickers = []
    for ticker in tickers:
        if ticker not in ticker_list:
            invalid_tickers.append(ticker)
    if len(invalid_tickers) > 0:
        return 'Invalid Ticker List', "Universe", invalid_tickers, None

    state = ASTState(start_date_pre, end_date_pre, tickers)
    ast = build_ast(main_signal, state, debug=False)
    cover_ast = build_ast(other_signal, state, debug=False)

    # TODO: Add check for syntax errors (Will be done soon - Ryan)
    if not ast.valid():
        # print(ast.evaluate(), file=stderr)
        return 'Invalid Input', "Signal", ast.evaluate(), None
    if not cover_ast.valid():
        # print(cover_ast.evaluate(), file=stderr)
        return 'Invalid Input', "Cover", ast.evaluate(), None

    # Iterate over the tickers, and then the dates (that list will be provided by zipline?)
    for ticker in tickers:
        state.ticker = ticker
        # Updates the ticker being processed
        data = bt.feeds.YahooFinanceData(dataname=ticker,
                                         fromdate=start_date,
                                         todate=end_date,
                                         plot=False)

        cerebro.adddata(data)
        cerebro.addstrategy(TreeSignalStrategy)
    cerebro.run()


    saveplots(cerebro, file_path='Kivy/chart.png', start=start_date, end=end_date)
    img = Image.open("Kivy/chart.png")
    width, height = img.size
    area = (0,0,width,244)
    cropped_img = img.crop(area)
    cropped_img.save('chart.png')

    return cerebro.broker.getvalue(), cerebro.broker.getvalue()-starting_cash, 3.0, 2.0


class TreeSignalStrategy(bt.Strategy):

    def __init__(self):
        self._addobserver(True, bt.observers.BuySell)

    def next(self):
        date_data = self.datetime.date(ago=0)
        state.current_day = date_data.strftime('%d/%m/%Y')

        close = self.data.close[0]

        if amount > 0 and ast.evaluate():
            if buy_bool:
                self.buy_bracket(size=amount,
                                 exectype=bt.Order.Market,
                                 limitprice=close*(1+take_profit),
                                 stopprice=close*(1-stop_loss))
            else:
                self.sell_bracket(size=amount,
                                  exectype=bt.Order.Market,
                                  limitprice=close*(1-take_profit),
                                  stopprice=close*(1+stop_loss))

        if cover_amount > 0 and cover_ast.evaluate():
            if cover_buy_bool:
                self.buy_bracket(size=cover_amount,
                                 exectype=bt.Order.Market,
                                 limitprice=close*(1+take_profit),
                                 stopprice=close*(1-stop_loss))
            else:
                self.sell_bracket(size=cover_amount,
                                  exectype=bt.Order.Market,
                                  limitprice=close*(1-take_profit),
                                  stopprice=close*(1+stop_loss))


def saveplots(cerebro, numfigs=1, iplot=True, start=None, end=None,
              width=16, height=9, dpi=300, tight=True, use=None, file_path = '', **kwargs):

    from backtrader import plot
    if cerebro.p.oldsync:
        plotter = plot.Plot_OldSync(**kwargs)
    else:
        plotter = plot.Plot(**kwargs)

    figs = []
    for stratlist in cerebro.runstrats:
        for si, strat in enumerate(stratlist):
            rfig = plotter.plot(strat, figid=si * 100,
                                numfigs=numfigs, iplot=iplot,
                                start=start, end=end, use=use)
            figs.append(rfig)

    for fig in figs:
        for f in fig:
            f.savefig(file_path, bbox_inches='tight')
    return figs

if __name__ == '__main__':
    # signal = 'if 30 day macd crosses above 13 day macd'
    # signal = 'if 30 day macd crosses below 17'
    # signal = "if rsi less than 90.1"
    # signal = "if rsi greater than 70 or 10 day macd crosses below 60"
    # signal = "if 5 day macd equal to 70"
    # signal = "if 5 day bollinger bands greater than 20"

    # universe = "AAPL, TSLA, GOOG, TTM, XOM, F, T, MSFT, AMZN, COTY, GE, GM, NIO, ALL, NVDA, REAL, NFLX, BAC, BABA"
    universe = "AAPL,TSLA,GOOG"

    zippy('if rsi greater than 100', 'Buy', '1000', 'if rsi less than 0',
          universe, '100', '5',
          'Sell', '1000', '18/03/2020', '18/10/2020')
