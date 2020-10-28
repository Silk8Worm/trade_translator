from LexerParser.src.AST import *
from LexerParser.src.signalparse import build_ast
from datetime import datetime
import backtrader as bt
from PIL import Image
from Data.rolling_sortinoV3 import rolling_Sortino
from Data.Rolling_Sharpe import rolling_sharpe
"""
IF A TRADE WOULD GIVE THE USER A NEGATIVE CASH BALANCE, THE TRADE DOES
NOT EXECUTE.
"""

def zippy(signal: str, trade: str, amt: str, cover_signal: str, universe: str,
          t_profit: str, s_loss: str, cover_trade: str, cover_amt: str,
          first_date: str, second_date: str):

    ticker_list = ['A', 'AAP', 'AAPL', 'ABB', 'ABBV', 'ABC', 'ABEV', 'ABMD', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEM', 'AEP', 'AES', 'AFL', 'AGR', 'AIG', 'AJG', 'AKAM', 'ALB', 'ALC', 'ALGN', 'ALL', 'ALLY', 'ALNY', 'ALXN', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMOV', 'AMOV', 'AMP', 'AMT', 'AMX', 'AMZN', 'ANET', 'ANSS', 'ANTM', 'AON', 'APD', 'APH', 'APTV', 'ARE', 'ARGX', 'ASML', 'ATHM', 'ATO', 'ATUS', 'ATVI', 'AU', 'AVB', 'AVGO', 'AVLR', 'AVTR', 'AVY', 'AWK', 'AXP', 'AZN', 'AZO', 'BA', 'BABA', 'BAC', 'BAH', 'BAM', 'BAX', 'BBDO', 'BBL', 'BBVA', 'BBY', 'BCE', 'BCS', 'BDX', 'BEN', 'BGNE', 'BHP', 'BIDU', 'BIIB', 'BILI', 'BIO', 'BIP', 'BK', 'BKI', 'BKNG', 'BKR', 'BLK', 'BLL', 'BMO', 'BMRN', 'BMY', 'BMY~', 'BNS', 'BNTX', 'BP', 'BPY', 'BR', 'BRO', 'BSBR', 'BSX', 'BTI', 'BUD', 'BURL', 'BX', 'BXP', 'BYND', 'C', 'CABO', 'CAG', 'CAH', 'CAJ', 'CAT', 'CB', 'CBRE', 'CCC', 'CCEP', 'CCI', 'CCK', 'CCL', 'CDAY', 'CDNS', 'CDW', 'CE', 'CEO', 'CERN', 'CFG', 'CGNX', 'CHA', 'CHD', 'CHGG', 'CHKP', 'CHL', 'CHRW', 'CHT', 'CHTR', 'CHU', 'CHWY', 'CI', 'CINF', 'CL', 'CLX', 'CM', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNHI', 'CNI', 'CNP', 'CNQ', 'COF', 'COO', 'COP', 'COST', 'COUP', 'CP', 'CPB', 'CPRT', 'CRH', 'CRL', 'CRM', 'CRWD', 'CS', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTLT', 'CTSH', 'CTVA', 'CTXS', 'CUK', 'CVNA', 'CVS', 'CVX', 'CZR', 'D', 'DAL', 'DB', 'DD', 'DDOG', 'DE', 'DELL', 'DEO', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCB', 'DISH', 'DLR', 'DLTR', 'DOCU', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DT', 'DTE', 'DUK', 'DVA', 'DXCM', 'E', 'EA', 'EBAY', 'EC', 'ECL', 'ED', 'EDU', 'EFX', 'EIX', 'EL', 'ELAN', 'ELS', 'EMN', 'EMR', 'ENB', 'ENIA', 'ENPH', 'ENTG', 'EOG', 'EPAM', 'EPD', 'EQIX', 'EQNR', 'EQR', 'ERIC', 'ERIE', 'ES', 'ESS', 'ET', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 'EXAS', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FB', 'FBHS', 'FCAU', 'FCX', 'FDS', 'FDX', 'FE', 'FICO', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FMS', 'FMX', 'FNV', 'FOX', 'FOXA', 'FRC', 'FTCH', 'FTNT', 'FTS', 'FTV', 'GD', 'GDDY', 'GDS', 'GE', 'GFI', 'GGG', 'GH', 'GIB', 'GILD', 'GIS', 'GLW', 'GM', 'GMAB', 'GNRC', 'GOLD', 'GOLD', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRFS', 'GRMN', 'GS', 'GSK', 'GSX', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD', 'HDB', 'HEI', 'HES', 'HIG', 'HLT', 'HMC', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSBC', 'HSY', 'HTHT', 'HUBS', 'HUM', 'HZNP', 'IAC', 'IBKR', 'IBM', 'IBN', 'ICE', 'ICLR', 'IDXX', 'IEP', 'IEX', 'IFF', 'ILMN', 'IMMU', 'INCY', 'INFO', 'INFO', 'INFY', 'ING', 'INTC', 'INTU', 'INVH', 'IP', 'IPGP', 'IQ', 'IQV', 'IR', 'ISRG', 'IT', 'ITW', 'IX', 'J', 'JBHT', 'JCI', 'JD', 'JHX', 'JKHY', 'JNJ', 'JPM', 'K', 'KB', 'KDP', 'KEP', 'KEY', 'KEYS', 'KGC', 'KHC', 'KKR', 'KL', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSU', 'LBRDA', 'LBRDK', 'LBTYA', 'LBTYB', 'LBTYK', 'LDOS', 'LEN', 'LFC', 'LH', 'LII', 'LIN', 'LKQ', 'LLY', 'LMT', 'LN', 'LNT', 'LOGI', 'LOW', 'LRCX', 'LSXMA', 'LSXMK', 'LULU', 'LUV', 'LVGO', 'LVS', 'LW', 'LYB', 'LYG', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MASI', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDB', 'MDLZ', 'MDT', 'MELI', 'MET', 'MFC', 'MFG', 'MGA', 'MGM', 'MKC', 'MKL', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH', 'MPC', 'MPLX', 'MPWR', 'MRK', 'MRNA', 'MRVL', 'MS', 'MSCI', 'MSFT', 'MSI', 'MT', 'MTB', 'MTCH', 'MTD', 'MTN', 'MU', 'MUFG', 'MXIM', 'MYOK', 'NDAQ', 'NDSN', 'NEE', 'NEM', 'NET', 'NFLX', 'NGG', 'NICE', 'NIO', 'NKE', 'NLOK', 'NLY', 'NMR', 'NOC', 'NOK', 'NOW', 'NSC', 'NTAP', 'NTCO', 'NTES', 'NTR', 'NTRS', 'NUE', 'NVCR', 'NVDA', 'NVO', 'NVR', 'NVS', 'NXPI', 'O', 'ODFL', 'OKE', 'OKTA', 'OMC', 'ON', 'ORAN', 'ORCL', 'ORLY', 'OTEX', 'OXY', 'PAGS', 'PANW', 'PAYC', 'PAYX', 'PBA', 'PBR', 'PCAR', 'PCG', 'PCTY', 'PDD', 'PEAK', 'PEG', 'PEGA', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHG', 'PHM', 'PINS', 'PKG', 'PKI', 'PKX', 'PLD', 'PM', 'PNC', 'PODD', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PTON', 'PTR', 'PUK', 'PXD', 'PYPL', 'QCOM', 'QDEL', 'QGEN', 'QGEN', 'QRVO', 'QSR', 'RACE', 'RCI', 'RCL', 'RDY', 'REGN', 'RELX', 'RF', 'RIO', 'RJF', 'RMD', 'RNG', 'ROK', 'ROKU', 'ROL', 'ROP', 'ROST', 'RPM', 'RSG', 'RUN', 'RY', 'RYAAY', 'SAM', 'SAN', 'SAP', 'SBAC', 'SBUX', 'SCCO', 'SCHW', 'SE', 'SEDG', 'SGEN', 'SHG', 'SHOP', 'SHW', 'SIRI', 'SIVB', 'SJM', 'SKM', 'SLB', 'SLF', 'SMFG', 'SNAP', 'SNE', 'SNN', 'SNP', 'SNPS', 'SNY', 'SO', 'SPG', 'SPGI', 'SPLK', 'SPOT', 'SQ', 'SRE', 'SRPT', 'SSNC', 'STE', 'STM', 'STNE', 'STT', 'STX', 'STZ', 'SU', 'SUI', 'SUZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAK', 'TAL', 'TCOM', 'TD', 'TDG', 'TDOC', 'TDY', 'TEAM', 'TECH', 'TEF', 'TEL', 'TER', 'TEVA', 'TFC', 'TFX', 'TGT', 'TIF', 'TJX', 'TLK', 'TM', 'TME', 'TMO', 'TMUS', 'TOT', 'TRI', 'TRMB', 'TROW', 'TRP', 'TRU', 'TRV', 'TSCO', 'TSLA', 'TSM', 'TSN', 'TTD', 'TTWO', 'TU', 'TW', 'TWLO', 'TWTR', 'TXG', 'TXN', 'TYL', 'UAL', 'UBER', 'UBS', 'UL', 'ULTA', 'UMC', 'UN', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VALE', 'VAR', 'VEEV', 'VFC', 'VIAC', 'VIACA', 'VICI', 'VIPS', 'VLO', 'VMC', 'VMW', 'VOD', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'W', 'WAB', 'WAT', 'WBA', 'WBK', 'WCN', 'WDAY', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WIT', 'WIX', 'WLTW', 'WM', 'WMB', 'WMT', 'WORK', 'WPC', 'WPM', 'WPP', 'WRB', 'WRK', 'WST', 'WTRG', 'WY', 'XEL', 'XLNX', 'XOM', 'XP', 'XRAY', 'XYL', 'YNDX', 'YUM', 'YUMC', 'Z', 'ZBH', 'ZBRA', 'ZEN', 'ZG', 'ZM', 'ZNGA', 'ZS', 'ZTO', 'ZTS']

    global start_date
    global end_date
    global start_date_pre
    global end_date_pre
    global buy_bool
    global cover_buy_bool
    global percentage_trade
    global amount
    if amt == "" or amt == "%":
        amount = 0
    else:
        if amt[-1] == '%':
            amt = amt.strip('%')
            percentage_trade = True
        else:
            percentage_trade = False
        amount = int(amt)
        if amount < 0:
            return 'Negative Values Not Accepted', "Trade", "", amt
    global cover_amount
    global percentage_cover_trade
    if cover_amt == "" or cover_amt == "%":
        cover_amount = 0
    else:
        if cover_amt[-1] == '%':
            cover_amt = cover_amt.strip('%')
            percentage_cover_trade = True
        else:
            percentage_cover_trade = False
        cover_amount = int(cover_amt)
        if cover_amount < 0:
            return 'Negative Values Not Accepted', "Cover Trade", "", cover_amt
    if cover_signal == "":
        cover_signal = "if rsi greater than 1000000"
    global starting_cash
    starting_cash = 1000000.0
    global port_vals
    port_vals = []
    global state
    global ast
    global cover_ast
    global main_signal
    main_signal = signal
    global other_signal
    other_signal = cover_signal
    global take_profit
    if t_profit == "":
        take_profit=10
    else:
        take_profit = float(t_profit)/100
        if take_profit < 0:
            return 'Negative Values Not Accepted', "Take Profit", "", t_profit
    global stop_loss
    if s_loss == "":
        stop_loss=10
    else:
        stop_loss = float(s_loss)/100
        if stop_loss < 0:
            return 'Negative Values Not Accepted', "Stop Loss", "", s_loss
    if trade == 'Sell #' or trade == 'Sell %':
        buy_bool = False
    else:
        buy_bool = True

    if cover_trade == 'Sell #' or cover_trade == 'Sell %':
        cover_buy_bool = False
    else:
        cover_buy_bool = True

    cerebro = bt.Cerebro(cheat_on_open=True)
    cerebro.broker.setcash(starting_cash)
    cerebro.broker.setcommission(0)


    start_date_pre = first_date
    start_date = datetime.strptime(start_date_pre, '%d/%m/%Y')
    end_date_pre = second_date
    end_date = datetime.strptime(end_date_pre, '%d/%m/%Y')

    if universe == '':
        return 'No Tickers Entered', "Universe", [], ""
    tickers_pre = universe.split(',')
    tickers = [x.strip() for x in tickers_pre]
    invalid_tickers = []
    for ticker in tickers:
        if ticker not in ticker_list:
            invalid_tickers.append(ticker)
    if len(invalid_tickers) > 0:
        return 'Invalid Ticker List', "Universe", invalid_tickers, universe

    state = ASTState(start_date_pre, end_date_pre, tickers)
    ast = build_ast(main_signal, state, debug=False)
    cover_ast = build_ast(other_signal, state, debug=False)

    # TODO: Add check for syntax errors (Will be done soon - Ryan)
    if not ast.valid():
        # print(ast.evaluate(), file=stderr)
        return 'Invalid Input', "Signal", ast.evaluate(), signal
    if not cover_ast.valid():
        # print(cover_ast.evaluate(), file=stderr)
        return 'Invalid Input', "Cover Signal", cover_ast.evaluate(), cover_signal

    cerebro.broker.set_checksubmit(checksubmit=False)
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
    cropped_img.save('Kivy/chart.png')

    port_vals_daily = []
    for i in range(len(tickers), len(port_vals), len(tickers)):
        port_vals_daily.append(port_vals[i])
    sharpe = rolling_sharpe(port_vals_daily, starting_cash)
    sortino = rolling_Sortino(port_vals_daily, starting_cash)
    if not sharpe:
        sharpe = 0
    if not sortino:
        sortino = 0

    return cerebro.broker.getvalue(), cerebro.broker.getvalue()-starting_cash, sharpe, sortino


class TreeSignalStrategy(bt.Strategy):

    def __init__(self):
        self._addobserver(True, bt.observers.BuySell)

    def next_open(self):
        port_vals.append(self.broker.getvalue())
        date_data = self.datetime.date(ago=0)
        state.current_day = date_data.strftime('%d/%m/%Y')

        open = self.data.open[0]
        if amount > 0 and ast.evaluate():
            if percentage_trade:
                size = round((self.broker.get_cash() / open * amount / 100), 0)
                if size == 0:
                    pass
                elif buy_bool:
                    if not self.position:
                        self.buy_bracket(size=size,
                                         exectype=bt.Order.Market,
                                         limitprice=open*(1+take_profit),
                                         stopprice=open*(1-stop_loss))
                else:
                    if not self.position:
                        self.sell_bracket(size=size,
                                          exectype=bt.Order.Market,
                                          limitprice=open*(1-take_profit),
                                          stopprice=open*(1+stop_loss))
            else:
                if buy_bool:
                    self.buy_bracket(size=amount,
                                     exectype=bt.Order.Market,
                                     limitprice=open*(1+take_profit),
                                     stopprice=open*(1-stop_loss))
                else:
                    if self.broker.get_cash() + amount * open < starting_cash*2:
                        self.sell_bracket(size=amount,
                                          exectype=bt.Order.Market,
                                          limitprice=open*(1-take_profit),
                                          stopprice=open*(1+stop_loss))

        if cover_amount > 0 and cover_ast.evaluate():
            if percentage_cover_trade:
                size = round((self.broker.get_cash() / open) * cover_amount/100, 0)
                if size == 0:
                    pass
                elif cover_buy_bool:
                    if not self.position:
                        self.buy_bracket(size=size,
                                         exectype=bt.Order.Market,
                                         limitprice=open*(1+take_profit),
                                         stopprice=open*(1-stop_loss))
                else:
                    if not self.position:
                        self.sell_bracket(size=size,
                                          exectype=bt.Order.Market,
                                          limitprice=open*(1-take_profit),
                                          stopprice=open*(1+stop_loss))
            else:
                if cover_buy_bool:
                    self.buy_bracket(size=cover_amount,
                                     exectype=bt.Order.Market,
                                     limitprice=open*(1+take_profit),
                                     stopprice=open*(1-stop_loss))
                else:
                    if self.broker.get_cash() + cover_amount * open < starting_cash*2:
                        self.sell_bracket(size=cover_amount,
                                          exectype=bt.Order.Market,
                                          limitprice=open*(1-take_profit),
                                          stopprice=open*(1+stop_loss))


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

    zippy('if rsi greater than 0', 'Buy', '1000', 'if rsi less than 40',
          universe, '50', '50',
          'Sell', '0', '18/03/2020', '25/03/2020')
