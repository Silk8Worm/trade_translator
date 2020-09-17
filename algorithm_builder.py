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

    and_bool: bool  # if this tree is type <and> or type <or>
    children: List

    def __init__(self, sentence: str):

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

        (fragments, and_bool) = parse_sentence(sentence) # If fragments is size 1, then its a leaf

        self.children = []

        if len(fragments) == 1:
            # <sentence> is a leaf
            self.children.append(fragments[0])

        else:
            # Well-Behaved Case
            self.and_bool = and_bool
            for (child in fragments):
                self.children.append(TradeTree(child))

    def parse_sentence(input: str):
        """
            - check for outside bracket
            - remove outside bracket
            - check for non-bracketed or statement
            - check for non-bracketed and statement
            - repeat (shave off ands/ors and store in object memory each time)
        """

    #  TODO Please add possible further non-theoretical stuff?

    def add_tree(self, to_add) -> None:

        """
        Equips the tree with one of: <and>, <or>.  Then adds the list of TradeTree to the sentence
        """
        self.children.append(to_add)

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
            for fragment in self.children:
                if fragment.get_status():
                    return True
            return False

        elif self.and_bool is True:
            # Tree is type <and>
            for fragment in self.children:
                if not fragment.get_status():
                    return False
            return True

        else:
            # Tree is a leaf
            if children[0] == "true":
                return True
            else:
                return False


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    tree = TradeTree("(true and false or true) and (false and true or true)")

"""Catch A and B or C"""
