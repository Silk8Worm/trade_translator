"""
    File name: signalparse.py
    Author: Ryan Goldberg
    Date created: 20/09/2020
    Python Version: 3.8
"""

import logging

import ply.yacc as yacc
from singallex import tokens
from ply.lex import LexToken

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
    '''signal : IF subsignal
              | subsignal'''
    # Return the subsignal itself, regardless of the word if
    p[0] = list(p)[-1]


# A grammar rule defining a subsignal in terms of other
# subsignals combined with and/or
def p_subsignal_andor(p):
    '''subsignal : subsignal AND subsignal
                 | subsignal OR subsignal'''
    if p[2] == 'and':
        p[0] = BinOp(state, and_, p[1], p[3])
    else:
        p[0] = BinOp(state, or_, p[1], p[3])


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
        p[0] = BinOp(state, gt, p[1], p[3])
    elif p[2] == 'lt':
        p[0] = BinOp(state, lt, p[1], p[3])
    elif p[2] == 'eq':
        p[0] = BinOp(state, eq, p[1], p[3])
    elif p[2] == 'above':
        p[0] = BinOp(state, gt, p[1], p[3])
    elif p[2] == 'below':
        p[0] = BinOp(state, lt, p[1], p[3])


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
        p[0] = BinOp(state, gt, p[1], p[3])
    elif p[2] == 'below':
        p[0] = BinOp(state, lt, p[1], p[3])
    elif p[2] == 'gt':
        p[0] = BinOp(state, gt, p[1], p[3])
    elif p[2] == 'lt':
        p[0] = BinOp(state, lt, p[1], p[3])
    elif p[2] == 'eq':
        p[0] = BinOp(state, eq, p[1], p[3])


# A grammar rule defining lookup based on an Indicator and a length of time
def p_lookup_time(p):
    '''lookup : time indicator'''
    p[0] = Lookup(state, p[2], p[1])


def p_lookup_fundamental(p):
    '''lookup : fundamental'''
    p[0] = Lookup(state, p[1], (1, 'day'))

def p_lookup_openclose(p):
    '''lookup : indicatory'''
    p[0] = Lookup(state, p[1], (1, 'day'))


# A grammar rule defining lookup based on just an Indicator
def p_lookup(p):
    '''lookup : indicator'''
    p[0] = Lookup(state, p[1])

# A grammar rule defining a length of time (Ex. 5 days)
def p_time(p):
    '''time : INTEGER LENGTH'''
    p[0] = (p[1], p[2])


# Merges multi word tokens
def p_gt(p):
    '''gt : GREATER THAN
          | GREATERSYM '''
    p[0] = "gt"


def p_lt(p):
    '''lt : LESS THAN
          | LESSSYM '''
    p[0] = "lt"


def p_eq(p):
    '''eq : EQUAL TO
          | EQUALSYM '''
    p[0] = "eq"


def p_above(p):
    '''above : CROSSES ABOVE'''
    p[0] = "above"


def p_below(p):
    '''below : CROSSES BELOW'''
    p[0] = "below"


# Combines all indicators, single and multi-word
def p_indicator_combined_bb(p):
    '''indicator : BBANDS
                 | BBANDS HIGH
                 | BBANDS LOW'''
    p[0] = " ".join(p[1:])


def p_indicator_single(p):
    '''indicator : INDICATOR
                 | LOW
                 | HIGH
                 | OPEN
                 | CLOSE'''
    p[0] = p[1]

def p_indicator_yesterady(p):
    '''indicatory : OPEN YESTERDAY
                  | CLOSE YESTERDAY'''
    p[0] = p[1]


# Defines the fundamentals
#FIXME:  'net debt/EBITDA'
def p_fundamental(p):
    '''fundamental : EBITDA
                   | EBITDA GROWTH
                   | LEVERAGE RATIO
                   | OPERATING MARGIN
                   | REVENUE GROWTH'''
    p[0] = " ".join([str(x) for x in p[1:]])

# Error rule for syntax errors
def p_error(p):
    errors = []
    tok = p
    # Handles the empty input
    if tok is None:
        errors.append(("", -1, "Input Too Short. Missing tokens"))
    # This means that the first error was a syntax error
    elif tok.type != 'UNKNOWN':
        errors.append((tok.value, tok.lexpos, "Unexpected Token"))
    while tok is not None:
        if tok.type == 'UNKNOWN':
            errors.append((tok.value, tok.lexpos, "Invalid Token"))
        tok = parser.token()

    # Clears the current parse stack and sets the error state to ok
    parser.symstack = parser.symstack[:1]
    generated_tree.value = errors


###############################################################################
# The function to build an abstract syntax tree
def build_ast(str_input: str, _state: ASTState, debug=False):
    # Global variables used in the parser algorithm
    global parser, state, generated_tree

    # Build the parser
    parser = yacc.yacc()
    state = _state

    # The output tree is originally an error Node, and it will be updated
    # if the value of generated_tree is None i.e no errors
    generated_tree = Error(state, None)

    # Parses in debug/ non-debug mode
    if debug:
        # Set up a logging object
        logging.basicConfig(
            level=logging.DEBUG,
            filename="parselog.txt",
            filemode="w",
            format="%(filename)10s:%(lineno)4d:%(message)s"
        )
        log = logging.getLogger()

        yacc.yacc(debug=True, debuglog=log)
        temp_tree = parser.parse(str_input.lower(), debug=log)
    else:
        yacc.yacc()
        temp_tree = parser.parse(str_input.lower())

    # If the value is None then this tree has no errors
    if generated_tree.value is None:
        # The parsed, error free signal's AST
        generated_tree = temp_tree
    return generated_tree


if __name__ == '__main__':
    # s = ""
    # s = "if rsa greater than 4"
    # s = "if ras gpraper than 4"
    # s = "fi rsi greater than 4.9"
    # s = "rsi if less than 3"
    # s = "i ras greaf tha 3"
    # s = "If RSI MACD crosses above"
    # s = "if exponential moving average crosses below"
    s = "if open yesterday greater than 50.5"
    # s = "if rsi greater than 30 or 5 day macd crosses below 50 and moving average equal to 43"
    ast = build_ast(s, ASTState("", "", ""), debug=True)
    print(ast)

# TODO
'''
Add Open yesterday
Add close yesterday
'''
