"""
    File name: signalparse.py
    Author: Ryan Goldberg
    Date created: 20/09/2020
    Python Version: 3.8
"""

from typing import Union


# TODO Get data from file???
def get_data(indicator, time=None):
    return 50
    # Get from IEX (


# A abstract class for a node in the AST
class Expr:
    def evaluate(self):
        raise NotImplementedError


# A class which looksup an indicator value (with a possible time range)
class Lookup(Expr):
    def __init__(self, *args):
        self.args = args

    def evaluate(self):
        return get_data(self.args)

    def __str__(self):
        if len(self.args) > 1:
            return f'(Lookup "{self.args[1][0]} {self.args[1][1]}: {self.args[0]}")'
        else:
            return f'(Lookup "{self.args[0]}")'


# A class which represents a literal float/integer value
class Value(Expr):
    def __init__(self, value):
        self.value = value

    def evaluate(self, *args: list):
        return self.value

    def __str__(self):
        return f'{self.value}'


# Class which performs an operation on 2 child nodes
class BinOp(Expr):
    def __init__(self, fxn, left: Union[Expr, float],
                 right: Union[Expr, float]):
        Expr.__init__(self)
        self.left = left if isinstance(left, Expr) else Value(left)
        self.right = right if isinstance(right, Expr) else Value(right)
        self.fxn = fxn

    def evaluate(self) -> list:
        return self.fxn(self.left.evaluate(), self.right.evaluate())

    def __str__(self):
        return f'({self.left.__str__()} {self.fxn.__name__} ' \
               f'{self.right.__str__()})'
