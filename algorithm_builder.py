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

        """

        (fragments, and_bool) = self.parse_sentence(sentence) # If fragments is size 1, then its a leaf

        self.children = []

        if len(fragments) == 1:
            # <sentence> is a leaf
            self.children.append(fragments[0])

            #TODO FOR DEBUGGING ONLY, DELETE AFTER
            self.and_bool = 5
        else:
            # Well-Behaved Case
            self.and_bool = and_bool
            for child in fragments:
                self.children.append(TradeTree(child))

    def __str__(self):
        s = ""
        for child in self.children:
            s += f"({str(child)} + {self.and_bool})"
        return s


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
        print(input)

        if input.count('~') != 0:
            print("Don't use that character")
            return None

        count = 0
        # Checking to see if outside brackets are unnecessary
        if input[0] == '(' and input[-1] == ')':
            for i in range(len(input)):
                if input[i] == '(':
                    count += 1
                elif input[i] == ')':
                    count -= 1
                    if count == -1:
                        break
                    elif count == 0 and i != len(input) - 1:
                        break
                    elif count == 0:
                        print("removed outside brackets")
                        return self.parse_sentence(input[1:-1])


        count = 0
        # Making sure the bracket count is valid
        for i in input:
            if i == '(':
                count += 1
            elif i == ')':
                count -= 1
        if count != 0:
            print("brackets invalid")
            return None

        # Returning a leaf
        if input.count('(') == 0 and input.count(' or ') == 0 and input.count(' and ') == 0:
            return [input], False

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
                        input_copy = input_copy.replace(input_copy[start:i+1], '~' * (i-start+1))
                        start = i + 1
        # Finding instances of or
        start = 0
        if input_copy.find(' or ', start) != -1:
            while input_copy.find(' or ', start) != -1:
                fragments.append(input[start:input_copy.find(' or ')])
                start = input_copy.find(' or ') + 4
            fragments.append(input[start:])
            return fragments, False

        # Finding instances of and
        elif input_copy.find(' and ', start) != -1:
            while input_copy.find(' and ', start) != -1:
                fragments.append(input[start:input_copy.find(' and ')])
                start = input_copy.find(' and ') + 5
            fragments.append(input[start:])
            return fragments, True

        print("reached end, there is an error")
        return None

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
            if self.children[0] == "true":
                return True
            else:
                return False


if __name__ == '__main__':

    # import doctest
    # doctest.testmod()

    tree = TradeTree("(rsi above 50 or (this below 40 and macd below 10))")
    print(tree)
