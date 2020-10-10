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
    'EQUALSYM'
]

# Reserved Keywords
keywords = ['if', 'greater', 'less', 'than', 'equal', 'to', 'above', 'below',
            'crosses', 'and', 'or']
combinational_indicators = ['bbands', 'high', 'low']
# Makes a dict mapping keywords to token types and adds the tokens to the list
reserved = {k: k.upper() for k in keywords + combinational_indicators}
tokens += list(reserved.values())


# Defining regular expressions for tokens
def t_FLOAT(t):
    r'\d+\.\d+'
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


def t_STRING(t):
    r'[^\s\\]+'
    # Check for reserved words
    if t.value in ['open', 'close', 'volume', 'obv', 'atr', 'rsi', 'macd',
                   'ema', 'sma']:
        t.type = 'INDICATOR'
    elif t.value in ['days', 'months', "years", "day", "month", "year"]:
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
