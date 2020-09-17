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
    and_bool: bool  # if this tree is type <and> or type <or>

    words: List

    def __init__(self, condition):

        """
        Initializing tree with just a condition. Until others are added, only
        the base condition matters.

        >>> a = True
        >>> b = False
        >>> tree1 = TradeTree(a)
        >>> tree2 = TradeTree(b)

        >>> tree1.words
        [True]

        >>> tree2.words
        [False]
        """

        self.and_bool = None
        self.words = []
        self.words.append(condition)

    #  TODO Please add possible further non-theoretical stuff?
    def remove_words(self, index) -> None:

        """
        Given an index, removes the appropriate part of the statement

        If only one word remains, set <and_bool> as desired.

        Do nothing if there are no words to remove
        """
        if len(self.words) == 0:
            return None

        self.words.pop(index)

        if len(self.words) == 0 or len(self.words) == 1:
            self.and_bool = None

    def add_words(self, to_add: List, and_bool: bool) -> None:

        """
        Equips the tree with one of: <and>, <or>.  Then adds the list of TradeTree to the sentence
        """
        self.and_bool = and_bool

        for tree in to_add:
            self.words.append(tree)

    def get_status(self) -> bool:

        """
        Goes through the tree and returns the tree's total value

        >>> tree1 = TradeTree(False)
        >>> tree1.add_words([True], False)
        >>> tree2 = TradeTree(True)
        >>> tree3 = TradeTree(False)

        >>> tree = TradeTree(tree1)
        >>> tree.add_words([tree2, tree3], False)

        >>> tree.get_status()
        True
        """

        if self.and_bool is False:
            # Tree is type <or>
            for word in self.words:
                if isinstance(word, TradeTree):
                    if word.get_status():
                        return True
                else:  # word is a boolean
                    if word:
                        return True

            return False

        elif self.and_bool is True:
            # Tree is type <and>
            for word in self.words:
                if isinstance(word, TradeTree):
                    if not word.get_status():
                        return False
                else:
                    if not word:
                        return False
            return True

        else:  # Less than 2 conditions
            if len(self.words) == 0:
                # No Words
                return None

            return self.words[0]


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
