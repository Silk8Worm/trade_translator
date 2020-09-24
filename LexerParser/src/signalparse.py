"""
    File name: signalparse.py
    Author: Ryan Goldberg
    Date created: 20/09/2020
    Python Version: 3.8
"""

import logging

import ply.yacc as yacc
from singallex import tokens

# Used for building the AST
from AST import *
from operator import gt, lt, eq, and_, or_

# Sets the precedence for the LALR parser for and and or
precedence = (
    ('left', 'AND'),
    ('left', 'OR')
)


# current top layer grammar rule
def p_signal(p):
    '''signal : IF subsignal'''
    p[0] = p[2]


# A grammar rule defining a subsignal in terms of other
# subsignals combined with and/or
def p_subsignal_andor(p):
    '''subsignal : subsignal AND subsignal
                 | subsignal OR subsignal'''
    if p[2] == 'and':
        p[0] = BinOp(and_, p[1], p[3])
        # p[0] = p[1] and p[3]
    else:
        p[0] = BinOp(or_, p[1], p[3])
        # p[0] = p[1] or p[3]


# A grammar rule defining a subsignal in terms of a single comparison value
def p_subsignal_comp(p):
    '''subsignal : comparison'''
    p[0] = p[1]


# A grammar rule defining a comparison between to lookups
def p_comparison_lookup(p):
    ''' comparison : lookup gt lookup
                   | lookup lt lookup
                   | lookup eq lookup
                   | lookup above lookup
                   | lookup below lookup'''
    if p[2] == 'gt':
        p[0] = BinOp(gt, p[1], p[3])
        # p[0] = p[1] > p[3]
    elif p[2] == 'lt':
        p[0] = BinOp(lt, p[1], p[3])
        # p[0] = p[1] < p[3]
    elif p[2] == 'eq':
        p[0] = BinOp(eq, p[1], p[3])
        # p[0] = p[1] == p[3]
    elif p[2] == 'above':
        p[0] = BinOp(gt, p[1], p[3])
        # p[0] = p[1] > p[3]
    elif p[2] == 'below':
        p[0] = BinOp(lt, p[1], p[3])
        p[0] = p[1] < p[3]


# A grammar rule defining a comparison between a lookup and a value
def p_comparison_literal(p):
    ''' comparison : lookup above FLOAT
                   | lookup below FLOAT
                   | lookup above INTEGER
                   | lookup below INTEGER
                   | lookup gt FLOAT
                   | lookup lt FLOAT
                   | lookup eq FLOAT
                   | lookup gt INTEGER
                   | lookup lt INTEGER
                   | lookup eq INTEGER'''
    if p[2] == 'above':
        p[0] = BinOp(gt, p[1], p[3])
        # p[0] = p[1] > p[3]
    elif p[2] == 'below':
        p[0] = BinOp(lt, p[1], p[3])
        # p[0] = p[1] < p[3]
    elif p[2] == 'gt':
        p[0] = BinOp(gt, p[1], p[3])
        # p[0] = p[1] > p[3]
    elif p[2] == 'lt':
        p[0] = BinOp(lt, p[1], p[3])
        # p[0] = p[1] < p[3]
    elif p[2] == 'eq':
        p[0] = BinOp(eq, p[1], p[3])
        # p[0] = p[1] == p[3]


# A grammar rule defining lookup based on an Indicator and a length of time
def p_lookup_time(p):
    'lookup : time indicator'
    # p[0] = get_data(p[2], p[1])
    p[0] = Lookup(p[2], p[1])


# A grammar rule defining lookup based on just an Indicator
def p_lookup(p):
    'lookup : indicator'
    # p[0] = get_data(p[1])
    p[0] = Lookup(p[1])


# A grammar rule defining a length of time (Ex. 5 days)
def p_time(p):
    'time : INTEGER LENGTH'
    p[0] = (p[1], p[2])


# Merges multi word tokens
def p_gt(p):
    'gt : GREATER THAN'
    p[0] = "gt"


def p_lt(p):
    'lt : LESS THAN'
    p[0] = "lt"


def p_eq(p):
    'eq : EQUAL TO'
    p[0] = "eq"


def p_above(p):
    'above : CROSSES ABOVE'
    p[0] = "above"


def p_below(p):
    'below : CROSSES BELOW'
    p[0] = "below"


# Combines all indicators, single and multi-word
def p_indicator_combined_ma(p):
    'indicator : MOVING AVERAGE'
    p[0] = "moving average"


def p_indicator_combined_ema(p):
    'indicator : EXPONENTIAL MOVING AVERAGE'
    p[0] = "exponential moving average"


def p_indicator_combined_bb(p):
    'indicator : BOLLINGER BANDS'
    p[0] = "bollinger bands"


def p_indicator_single(p):
    'indicator : INDICATOR'
    p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    print(p)
    exit(1)


# Build the parser
parser = yacc.yacc()

# Different test data, (relies on the current value of get_data), uncomment to
# try different ones
# s = 'if 30 day macd crosses above 13 day macd'
# s = 'if 30 day macd crosses below 17'
# s = "if rsi less than 56.1"
s = "if rsi greater than 70 or 10 day macd crosses below 60"
# s = "if 5 day bollinger bands greater than 20"

# Set up a logging object
logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Create a compiler, run in debug mode (creates a debug log file) and then
yacc.yacc(debug=True, debuglog=log)
result = parser.parse(s.lower(), debug=log)

# print the boolean result
print(result)
print(result.evaluate())
