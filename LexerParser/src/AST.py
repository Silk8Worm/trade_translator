"""
    File name: AST.py
    Author: Ryan Goldberg
    Date created: 23/09/2020
    Python Version: 3.8
"""

from typing import Union, Any
from Data import data_gatherer


# The current state held by the abstract syntax tree
class ASTState:
    def __init__(self, start_date, end_date, universe):
        self.current_day = None
        self.ticker = None
        self.start = start_date
        self.end = end_date
        self.universe = universe


# A abstract class for a node in the AST
class Expr:
    def __init__(self, state: ASTState):
        self.state = state

    def evaluate(self) -> Any:
        raise NotImplementedError

    def valid(self) -> bool:
        return True


# A class which looks up an indicator value (with a possible time range)
class Lookup(Expr):
    def __init__(self, state: ASTState, *args: list):
        Expr.__init__(self, state)
        self.args = args
        self.data = None

    def evaluate(self) -> Any:
        # Check if the data has been pulled
        if not self.data:
            # Processes the number of days this indicator considers
            if len(self.args) == 1:
                num_days = 14
            else:
                len_conversion = {"day": 1, "week": 7, "month": 30, "year": 365}
                num_days = self.args[1][0] * len_conversion[self.args[1][1]]
            print(num_days)
            self.data = data_gatherer.get_data(self.state.universe,
                                               self.args[0].upper(), self.state.start, self.state.end, num_days)

        # Does the data lookup form the preinitialized list of values, self.data
        day = self.state.current_day
        ticker = self.state.ticker

        # If the lookup doesn't exist return 0
        return self.data.setdefault(day, {}).setdefault(ticker, 0)

    def __str__(self) -> str:
        if len(self.args) > 1:
            return f'(Lookup "{self.args[1][0]} {self.args[1][1]}: ' \
                   f'{self.args[0]} of {self.state.ticker} on ' \
                   f'{self.state.current_day}")'
        else:
            return f'(Lookup "{self.args[0]} of {self.state.ticker} on ' \
                   f'{self.state.current_day}")'


# A class which represents a literal float/integer value
class Value(Expr):
    def __init__(self, state: ASTState, value: float):
        Expr.__init__(self, state)
        self.value = value

    def evaluate(self, *args: list) -> float:
        return self.value

    def __str__(self) -> str:
        return f'{self.value}'


# Class which performs an operation on 2 child nodes
class BinOp(Expr):
    def __init__(self, state: ASTState, fxn, left: Union[Expr, float],
                 right: Union[Expr, float]):
        Expr.__init__(self, state)
        self.left = left if isinstance(left, Expr) else Value(state, left)
        self.right = right if isinstance(right, Expr) else Value(state, right)
        self.fxn = fxn

    def evaluate(self) -> bool:
        return self.fxn(self.left.evaluate(), self.right.evaluate())

    def __str__(self) -> str:
        return f'({self.left.__str__()} {self.fxn.__name__} ' \
               f'{self.right.__str__()})'


# A class which holds Nodes containing errors
class Error(Expr):
    def __init__(self, state: ASTState, value):
        Expr.__init__(self, state)
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return f'Errors {self.value}'

    def __repr__(self):
        return f'Errors {self.value}'

    def valid(self) -> bool:
        return False
