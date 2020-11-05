"""
    File name: signalparse.py
    Author: Ryan Goldberg
    Date created: 20/09/2020
    Python Version: 3.8
"""

import ply.lex as lex

# Tokens
tokens = [
    'FLOAT',
    'INTEGER',
    'UNKNOWN',
    'INDICATOR',
    'LENGTH',
    'GREATERSYM',
    'LESSSYM',
    'EQUALSYM',
    'DEBTEBITDA',
    'SLASH',
]

# Reserved Keywords
keywords = ['if', 'greater', 'less', 'than', 'equal', 'to', 'above', 'below',
            'crosses', 'and', 'or', 'is']
combinational_indicators = ['cash', 'ratio', 'yield', 'growth', 'low',
                            'current', 'revenue', 'price', 'share', 'quick',
                            'high', 'per', 'dividend', 'assets', 'bbands',
                            'price', 'book', 'gross', 'close', 'eps', 'profit',
                            'debt', 'operating', 'roe', 'equity', 'sales',
                            'earnings', 'net', 'coverage', 'roa', 'margin',
                            'leverage', 'ebitda', 'book', 'yesterday', 'payout',
                            'open', 'value', 'short', 'interest']

# Makes a dict mapping keywords to token types and adds the tokens to the list
reserved = {k: k.upper() for k in keywords + combinational_indicators}
tokens += list(reserved.values())


# Defining regular expressions for tokens
def t_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_GREATERSYM(t):
    r'>'
    return t


def t_LESSSYM(t):
    r'<'
    return t


def t_EQUALSYM(t):
    r'='
    return t


def t_SLASH(t):
    r'/'
    return t


def t_DEBTEBITDA(t):
    r'debt/ebitda'
    return t


def t_STRING(t):
    r'[^\s\\]+'
    # Check for reserved words
    if t.value in ['volume', 'obv', 'atr', 'rsi', 'macd',
                   'ema', 'sma']:
        t.type = 'INDICATOR'
    elif t.value in ["day", "month", "year", 'week']:
        t.type = 'LENGTH'
    else:
        t.type = reserved.get(t.value, 'UNKNOWN')
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# EOF handling
def t_eof(t):
    return None


# Error handling rule
def t_error(t):
    t.lexer.skip(1)
    return t


# Build the lexer
lexer = lex.lex()
