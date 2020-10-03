from src import AST, signalparse, singallex
import ply.yacc as yacc
import logging

def zippy(signal,trade,cover_signal,universe,take_profit,stop_loss,cover_trade):
    print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

    try:
        print(signalparse.create_parser(signal))
    except Exception:
        print(Exception)


    return 5000, 10000, 1.4, 2.3, [1,2,3], [1,4,9]
