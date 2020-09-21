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
    'ALPHA',
    'INDICATOR',
    'LENGTH'
]

# Reserved Keywords
reserved = {
    'if': 'IF',
    'greater': 'GREATER',
    'less': 'LESS',
    'than': 'THAN',
    'equal': 'EQUAL',
    'to': 'TO',
    'above': 'ABOVE',
    'below': 'BELOW',
    'crosses': 'CROSSES'
}
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


def t_ALPHA(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    if t.value in ['rsi', 'macd']:
        t.type = 'INDICATOR'
    elif t.value in ['days', 'months', "years", "day", "month", "year"]:
        t.type = 'LENGTH'
    else:
        t.type = reserved.get(t.value, 'ALPHA')
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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
