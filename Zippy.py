from AST import *
from signalparse import build_ast
from datetime import datetime
import backtrader as bt


def zippy(signal: str, trade: str, amt: str, cover_signal: str, universe: str,
          t_profit: float, s_loss: float,
          cover_trade: str, cover_amt):
    global start_date
    global end_date
    global start_date_pre
    global end_date_pre
    global buy_bool
    global cover_buy_bool
    global amount
    amount = int(amt)
    global cover_amount
    cover_amount = int(cover_amt)
    global state
    global ast
    global cover_ast
    global main_signal
    main_signal = signal
    global other_signal
    other_signal = cover_signal
    global take_profit
    take_profit = float(t_profit)/100
    global stop_loss
    stop_loss = float(s_loss)/100

    if trade == 'sell':
        buy_bool = False
    else:
        buy_bool = True

    if cover_trade == 'sell':
        cover_buy_bool = False
    else:
        cover_buy_bool = True

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(.01)


    start_date_pre = "01/01/2020"
    start_date = datetime.strptime(start_date_pre, '%d/%m/%Y')
    end_date_pre = "10/01/2020"
    end_date = datetime.strptime(end_date_pre, '%d/%m/%Y')

    # FIXME: Validate input?? --> There is a max # of tickers you can input (11?)
    tickers_pre = universe.split(',')
    tickers = [x.strip() for x in tickers_pre]
    state = ASTState(start_date_pre, end_date_pre, tickers)
    ast = build_ast(main_signal, state, debug=False)
    cover_ast = build_ast(other_signal, state, debug=False)

    # TODO: Add check for syntax errors (Will be done soon - Ryan)
    if not ast.valid():
        print(ast.evaluate())
        exit(-42)

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

    saveplots(cerebro, file_path = 'chart.png')

    return cerebro.broker.getvalue(), cerebro.broker.getvalue()-1000000, 3.0, 2.0


class TreeSignalStrategy(bt.Strategy):

    def __init__(self):
        self._addobserver(True, bt.observers.BuySell)


    def notify_order(self, order):
        if not order.status == order.Completed:
            return  # discard any other notification

        if not self.position:  # we left the market
            return

        if buy_bool:
            stop_price = order.executed.price * (1.0 - stop_loss)
            self.sell(exectype=bt.Order.Stop, price=stop_price)
        else:
            stop_price = order.executed.price * (1.0 + stop_loss)
            self.buy(exectype=bt.Order.Stop, price=stop_price)

        if buy_bool:
            take_price = order.executed.price * (1.0 + take_profit)
            self.sell(exectype=bt.Order.Stop, price=take_price)
        else:
            take_price = order.executed.price * (1.0 - take_profit)
            self.buy(exectype=bt.Order.Stop, price=take_price)
        # TODO: Trailing?
        # self.sell(exectype=bt.Order.StopTrail, trailamount=stop_loss)


    def next(self):

        date_data = self.datetime.date(ago=0)
        state.current_day = date_data.strftime('%d/%m/%Y')

        if not self.position:
            if ast.evaluate():
                if buy_bool:
                    self.buy(size=int(amount))
                else:
                    self.sell(size=int(amount))

        if self.position:
            if cover_ast.evaluate():
                if cover_buy_bool:
                    self.buy(size=int(cover_amount))
                else:
                    self.sell(size=int(cover_amount))


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
    signal = "if rsi less than 56.1"
    # signal = "if rsi greater than 70 or 10 day macd crosses below 60"
    # signal = "if 5 day macd equal to 70"
    # signal = "if 5 day bollinger bands greater than 20"

    universe = "AAPL,TSLA,GOOG"

    zippy(signal, 'buy', '10', 'if rsi greater than 0', universe, .05, .02,
          'sell', '10')
