"""
This is used for proof of concept of a boolean tree that can process a sentence
inputted by a user and then check the whole statement for if the trade should
execute.

Kevin Lai and Albert Cao
"""

from typing import List


class TradeTree:

    """
    This tree combines different market conditions into a boolean tree
    """

    # condition
    and_bool: bool
    words: List

    def __init__(self, condition):

        """
        Initializing tree with just a condition. Until others are added, only
        the base condition matters.
        """

        self.condition = condition
        self.and_bool = None
        self.words = []

    #TODO Please add delete condition and possible further non-theoretical stuff?

    def add_words(self, sub_trade_trees: List, and_bool: bool) -> None:

        """
        Knocks self's condition down and creates a list with it and all the new
        other trade trees. All condition checks should be at leaf level.
        """

        self.and_bool = and_bool

        for sub_trade_tree in sub_trade_trees:
            self.words.append(sub_trade_tree)

        self.and_bool = and_bool
        self.condition = None

    def get_status(self) -> bool:

        """
        Goes through the tree and returns the tree's total value

        >>> a = TradeTree('true')
        >>> a.add_words([TradeTree('true'), TradeTree('false')], False)
        >>> a.words[0].add_words([TradeTree('false'), TradeTree('true')], False)
        >>> a.get_status()
        True
        """

        if self.condition is not None:
            return self.check(self.condition)

        if self.and_bool:
            for word in self.words:
                if not word.get_status():
                    return False
            return True

        else:
            for word in self.words:
                if word.get_status():
                    return True
            return False

    def check(self, condition) -> bool:

        """
        Used to check a condition that can be specified however. This processes
        each individual condition. It could be a string, it's own class, etc.
        """

        if self.condition == "true":
            return True
        return False

def parse_sentence(input: str):
    """
    - split sentence
        - check for outside bracket
        - remove outside bracket
        - check for non-bracketed or statement
        - check for non-bracketed and statement
        - repeat (shave off ands/ors and store in object memory each time)
    - create tree
    """

if __name__ == '__main__':

    import doctest
    doctest.testmod()

    parse_sentence("(true and false or true) and (false and true or true)")

"""Catch A and B or C"""
