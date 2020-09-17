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

    def parse_sentence(self, input: str):
        """
        Returns None if invalid bracket setup

            - check for outside bracket
            - remove outside bracket
            - check for non-bracketed or statement
            - check for non-bracketed and statement
            - repeat (shave off ands/ors and store in object memory each time)
        """
        input_copy = input
        fragments = []

        if str.count('~') != 0:
            print("Don't use that character")
            return None

        count = 0
        # Checking to see if outside brackets are unnecessary
        for i in range(len(input)):
            if input[i] == '(':
                count += 1
            elif input[i] == ')':
                count -= 1
                if count == 0 and i != len(input) - 1:
                    break
                elif count == 0:
                    return self.parse_sentence(input[1:-2])

        count = 0
        # Making sure the bracket count is valid
        for i in input:
            if i == '(':
                count += 1
            elif i == ')':
                count -= 1
        if count != 0:
            return None

        # Returning a leaf
        if input.count('(') == 0 and input.count(' or ') == 0 and input.count(' and ') == 0:
            return [input]

        # Exclude inner bracket strings
        if input.count('(') >= 1:
            count = 0
            start = 0
            for i in range(len(input_copy)):
                if input_copy[i] == '(':
                    start = i
                    count += 1
                elif input_copy[i] == ')':
                    count -= 1
                    if count == 0:
                        # Completed section, breaking it off from parsing
                        input_copy.replace(input_copy[start:i+1], '~' * (i-start+1))
                        start = i + 1

        # Finding instances of or
        start = 0
        if input_copy.find(' or ', start) != -1:
            while input_copy.find(' or ', start) != -1:
                fragments.append(input[start:input_copy.find(' or ')])
                start = input_copy.find(' or ') + 4

        # Finding instances of and
        elif input_copy.find(' and ', start) != -1:
            while input_copy.find(' and ', start) != -1:
                fragments.append(input[start:input_copy.find(' or ')])
                start = input_copy.find(' and ') + 5






        return fragments[], and_bool

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


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    tree = TradeTree("(true and false or true) and (false and true or true)")

"""Catch A and B or C"""
