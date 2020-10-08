from AST import *
from signalparse import build_ast
# import zipline.api as zl

def zippy(signal: str, trade: str, cover_signal: str, universe: str,
          take_profit: float, stop_loss: float,
          cover_trade: str):\

    start_date = "01/01/2020"
    end_date = "03/01/2020"

    # FIXME: Validate input??
    tickers_pre = universe.split(',')
    tickers = [x.strip() for x in tickers_pre]

    # Make the state
    state = ASTState(start_date, end_date, tickers)

    # Build the AST
    ast = build_ast(signal, state, debug=False)

    # TODO: Add check for syntax errors (Will be done soon - Ryan)
    if not ast.valid():
        print(ast.evaluate())
        exit(-42)


    # TODO: plug this into zipline
    # Iterate over the tickers, and then the dates (that list will be provided by zipline?)
    for ticker in tickers:
        # Updates the ticker being processed
        state.ticker = ticker
        for day in [start_date, "02/01/2020", end_date]:
            # Updates the date
            state.current_day = day

            # Prints the tree and evaluates it with the given state
            print(f'{ast} -> {ast.evaluate()}')

    return 5000, 10000, 1.4, 2.3, [1, 2, 3], [1, 4, 9]


if __name__ == '__main__':
    # signal = 'if 30 day macd crosses above 13 day macd'
    # signal = 'if 30 day macd crosses below 17'
    signal = "if rsi less than 56.1"
    # signal = "if rsi greater than 70 or 10 day macd crosses below 60"
    # signal = "if 5 day macd equal to 70"
    # signal = "if 5 day bollinger bands greater than 20"

    universe = "AAPL,TSLA,GOOG"

    zippy(signal, 'buy 10', 'if rsi less than 56.1', universe, .05, .02,
          'sell 10')
