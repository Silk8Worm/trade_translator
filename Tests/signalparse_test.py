"""
    File name: signalparse_tests.py
    Author: Ryan Goldberg
    Date created: 23/10/2020
    Python Version: 3.8
"""
from sys import stderr
from LexerParser.src.signalparse import build_ast, ASTState

try:
    valid_inputs = open("/home/ryan/Projects/Python/trade_translator/Tests/valid_signals.txt", 'r')
except FileNotFoundError:
    print("File Not Found", file=stderr)
    exit(1)


def test_valid_inputs():
    for line in valid_inputs.readlines():
        i, o = line.strip().split(',')
        ast = build_ast(i, ASTState("", "", ""), debug=False)
        assert str(ast) == o


if __name__ == '__main__':
    import pytest

    pytest.main(['-s', 'signalparse_test.py'])
