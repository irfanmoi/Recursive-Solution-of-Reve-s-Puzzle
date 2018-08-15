# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap,
# Dustin Wehr, Brian Harrington, Moin Irfan
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Summer 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
TOAHModel:  Model a game of Towers of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Towers of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """Model a game of Towers Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.  Note that
    large, aged, cheeses at the bottom of each pile serve as stools, and
    these may not be moved!

    fill_first_stool - put an existing model in the standard starting config
    move - move cheese from one stool to another
    add - add a cheese to a stool
    cheese_location - index of the stool that the given cheese is on
    number_of_cheeses - number of cheeses in this game
    number_of_moves - number of moves so far
    number_of_stools - number of stools in this game
    get_move_seq - MoveSequence object that records the moves used so far
    """
    def __init__(self, number_of_stools):

        # RI

        # _number_of_stools is the number of stools in the game
        # _number_of_cheeses is the number of cheeses in the game
        # _number_of_moves is the number of moves applied in the game
        # _number_of_moves > 0 iff (number_of_cheeses > 0) and
        # (_number_of_stools > 0)

        # _moves is a list containing tuples of moves applied in the game
        # len(_moves) == _number_of_moves
        # if len(_moves) != 0, then _moves[0] is a tuple, (A, B) where
        # A is a stool number between 0-(_number_of_stools - 1) and
        # B is a also a stool number between 0 - (_number_of_stools - 1)
        # (Uses 0-indexing for stool number)

        # _stools is the string representation of all the stools in the game
        # len(_stools) == 0 iff (number_of_stools == 0)
        # and (number_of_cheeses == 0)
        # len(_stools) == _number_of_stools

        '''(TOAHModel, int) -> NoneType
        Given number of stools in int, initializes a TOAHModel object.
        '''
        self._number_of_stools = number_of_stools
        self._number_of_cheeses = 0
        self._number_of_moves = 0
        self._stools = []
        self._moves = []
        # complete the list representation of all the stools
        # each list appended to self._stools is another stool
        for i in range(self._number_of_stools):
            self._stools.append([])

    def top_cheese(self, stool):
        '''(TOAHModel, int) -> Cheese
        Returns the Cheese object located at the top of the given stool.

        REQ: stool <= self.number_of_stools

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.top_cheese(0).size
        1
        >>> M.move(0, 1)
        >>> c = Cheese(2)
        >>> M.top_cheese(0) == c
        True
        >>>
        >>> M.top_cheese(0).size == 2
        True
        >>> M.top_cheese(3)
        Traceback (most recent call last):
        ...
        IllegalMoveError: This stool is empty!

        REQ: len(stool) > 0
        '''
        # get the list representation of all the stools
        stools = self.get_stools()
        # if the stool is not empty, return the top Cheese object!
        if len(stools[stool]) != 0:
            return stools[stool][-1]
        else:
            # if stool is empty, raise an IllegalMoveError
            raise IllegalMoveError("This stool is empty!")

    def get_stools(self):
        '''
        (TOAHModel) -> list
        Returns a list representation of all the stools and the Cheese objects.
        >>> M = TOAHModel(4)
        >>> M.get_stools()
        [[], [], [], []]
        >>> M.fill_first_stool(5)
        >>> M.get_stools()
        [[Cheese(5), Cheese(4), Cheese(3), Cheese(2), Cheese(1)], [], [], []]
        >>> M.move(0, 1)
        >>> M.move(0, 2)
        >>> M.move(0, 3)
        >>> M.get_stools()
        [[Cheese(5), Cheese(4)], [Cheese(1)], [Cheese(2)], [Cheese(3)]]
        '''
        # simply return the private variable which holds the list
        # representation of all the stools
        return self._stools

    def fill_first_stool(self: 'TOAHModel', number_of_cheeses: int):
        """
        Put number_of_cheeses cheeses on the first (i.e. 0-th) stool, in order
        of size, with a cheese of size == number_of_cheeses on bottom and
        a cheese of size == 1 on top.
        >>> M = TOAHModel(1)
        >>> M.fill_first_stool(0)
        >>> M.get_stools () == [[]]
        True
        >>> M = TOAHModel(1)
        >>> M.fill_first_stool(2)
        >>> M.get_stools() == [[Cheese(2), Cheese(1)]]
        True
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.get_stools()
        [[Cheese(5), Cheese(4), Cheese(3), Cheese(2), Cheese(1)], [], [], []]

        """
        # Fill the first stool with the biggest cheese at the bottom and
        # smallest cheese at the top
        for i in range(number_of_cheeses, 0, -1):
            # add it to first stool
            self.add(0, Cheese(i))

    def move(self, s1, s2):
        '''
        (TOAHModel, int, int) -> NoneType
        Given stool numbers: s1 and s2, moves the top Cheese object from
        s1'th stool to s2'th stool.
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(1)
        >>> M.move(0, 1)
        >>> M.get_stools()
        [[], [Cheese(1)], [], []]
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(4)
        >>> M.move(0, 1)
        >>> M.move(0, 2)
        >>> M.move(1, 2)
        >>> M.get_stools() == [[Cheese(4), Cheese(3)], [], [Cheese(2),\
        Cheese(1)], []]
        True
        >>> M.move(2, 1)
        >>> M.get_stools()
        [[Cheese(4), Cheese(3)], [Cheese(1)], [Cheese(2)], []]
        >>> M.move(0, 3)
        >>> M.get_stools() ==  [[Cheese(4)], [Cheese(1)], [Cheese(2)], \
        [Cheese(3)]]
        True
        >>> M.move(0, 1)
        Traceback (most recent call last):
        ...
        IllegalMoveError: Cannot move bigger Cheese onto smaller Cheese
        >>> M = TOAHModel(4)
        >>> M.move(0, 1)
        Traceback (most recent call last):
        ...
        IllegalMoveError: This stool is empty!


        REQ: s2.top_cheese().size > s1.top_cheese().size
        '''

        # For this move to work, the destination stool has to be either empty
        # OR
        # if the destination is not empty, the user must not be allowed to
        # place a smaller cheese on a bigger cheese

        if len(self.get_stools()[s2]) > 0 and (
            self.get_stools()[s2][-1].size < self.get_stools()[s1][-1].size
                ):
            # raise IllegalMoveError if requirements are violated
            raise IllegalMoveError(
                "Cannot move bigger Cheese onto smaller Cheese")

        elif len(self.get_stools()[s1]) == 0:
            raise IllegalMoveError(
                "This stool is empty!")
        else:
            # the number of moves is now + 1
            self._number_of_moves += 1
            # record this move in self._moves list
            self._moves.append((s1, s2))
            # get the origin stool
            s1 = self._stools[s1]
            # ger the destination stool
            s2 = self._stools[s2]
            # pop from origin stool and append to destination!
            s2.append(s1.pop())

    def add(self, stool, cheese):
        '''
        (TOAHModel, int, Cheese) -> NoneType
        Given stool location and Cheese object, places the Cheese at the top
        of the stool.

        >>> M = TOAHModel(4)
        >>> M.add(0, Cheese(2))
        >>> M.top_cheese(0) == Cheese(2)
        True
        >>> M.add(0, Cheese(1))
        >>> M.get_stools()
        [[Cheese(2), Cheese(1)], [], [], []]
        >>> M.add(1, Cheese(3))
        >>> M.top_cheese(1).size
        3
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(4)
        >>> M.add(1, Cheese(5))
        >>> M.top_cheese(0) == Cheese(4)
        False
        >>> print(M.get_stools())
        [[Cheese(4), Cheese(3), Cheese(2), Cheese(1)], [Cheese(5)], [], []]
        '''
        # get the stool and add the cheese on top
        self._stools[stool].append(cheese)
        # now there are + 1 more cheeses in the game!
        self._number_of_cheeses += 1

    def cheese_location(self, cheese):
        '''(TOAHModel, Cheese) -> int
        Given Cheese object, returns the location of the Cheese, in terms of
        stool number.
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.cheese_location(Cheese(5))
        0
        >>> M.cheese_location(Cheese(4))
        0
        >>> M.cheese_location(Cheese(3))
        0
        >>> M.cheese_location(Cheese(2))
        0
        >>> M.cheese_location(Cheese(1))
        0
        >>> M = TOAHModel(4)
        >>> M.add(2, Cheese(4))
        >>> M.cheese_location(Cheese(4)) == 0
        False
        >>> M.cheese_location(Cheese(4)) == 2
        True

        REQ: cheese.size <= self.number_of_cheeses()
        '''
        # since we haven't started searching yet, found is false
        found = False
        # location is also unknown
        location = None
        try:
            i = 0
            x = len(self._stools) - 1
            # loop until the given Cheese object is found
            # looping through the i't stool
            while (found is False) and (i <= x):
                ii = 0
                y = len(self._stools[i]) - 1
                while (found is False) and (ii <= y):
                    # checking if ii'th item in i'th stool matches the given
                    # Cheese object
                    if self._stools[i][ii] == cheese:
                        # if it matches, then found is True
                        # and location is to be stored
                        found = True
                        location = i
                    ii += 1
                i += 1
            # return the location!
        except Exception:
            location = None

        return location

    def number_of_cheeses(self):
        '''(TOAHModel) -> int
        Returns the number of cheeses inside the TOAHModel object,
        (total number of cheeses involved in the game).
        >>> M = TOAHModel(4)
        >>> M.number_of_cheeses()
        0
        >>> M.fill_first_stool(10)
        >>> M.number_of_cheeses()
        10
        >>> M.move(0, 1)
        >>> M.number_of_cheeses() == 11
        False
        >>> M.number_of_cheeses() == 10
        True
        >>> M.add(3, Cheese(11))
        >>> M.number_of_cheeses()
        11
        >>> M.add(2, Cheese(12))
        >>> M.number_of_cheeses() == 12
        True
        '''
        # getter for private var which holds the number of cheeses in the game
        # just return the variable
        return self._number_of_cheeses

    def number_of_moves(self):
        '''(TOAHModel) -> int
        Returns the total number of times the Cheese object(s) were moved from
        their original location.
        >>> M = TOAHModel(4)
        >>> M.number_of_moves()
        0
        >>> M.fill_first_stool(3)
        >>> M.number_of_moves()
        0
        >>> M.add(1, Cheese(4))
        >>> M.number_of_moves() > 0
        False
        >>> M.number_of_moves() == 0
        True
        >>> M.move(0,1)
        >>> M.number_of_moves() == 1
        True
        >>> M.move(0, 2)
        >>> M.move(0, 3)
        >>> M.number_of_moves()
        3
        '''
        # getter for private var which holds the number of moves in the game
        # just return the variable
        return self._number_of_moves

    def number_of_stools(self):
        '''(TOAHModel) -> int
        Return the total number of stools associated with the TOAHModel
        (number of stools in the game).
        >>> M = TOAHModel(4)
        >>> M.number_of_stools()
        4
        >>> M = TOAHModel(0)
        >>> M.number_of_stools() == 1
        False
        >>> M.number_of_stools() == 0
        True
        >>> M = TOAHModel(100000)
        >>> M.number_of_stools()
        100000
        '''
        # getter for private var which holds the number of stools in the game
        # just return the variable
        return self._number_of_stools

    def _cheese_at(self: 'TOAHModel', stool_index,
                   stool_height: int) -> 'Cheese':
        """
        If there are at least stool_height+1 cheeses
        on stool stool_index then return the (stool_height)-th one.
        Otherwise return None.

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """

        try:
            stool = self._stools[stool_index]
            return_cheese = stool[stool_height]
        except Exception:
            return_cheese = None

        return return_cheese

    def get_move_seq(self: 'TOAHModel') -> 'MoveSequence':
        '''
        Returns a MoveSequence object which has recorded all the moves
        applied in this game.
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.move(0, 1)
        >>> M.get_move_seq().length()
        1
        >>> M.move(0, 2)
        >>> M.move(0, 3)
        >>> ms = M.get_move_seq()
        >>> isinstance(ms, MoveSequence)
        True
        >>> ms.length() == 3
        True
        >>> ms.get_move(0) == (0, 1)
        True
        >>> ms.get_move(1)
        (0, 2)
        '''
        # return a new MoveSequence object initialized with the moves applied
        # to TOAHModel (self)
        return MoveSequence(self._moves)

    def __eq__(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        We're saying two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1 == m2
        True
        """
        # if the list of stools representations are the same, then the two
        # models are equivalent!
        return self.get_stools() == other.get_stools()

    def __str__(self: 'TOAHModel') -> str:
        """
        Depicts only the current state of the stools and cheese.
        """
        stool_str = "=" * (2 * (self.number_of_cheeses()) + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.number_of_stools()

        def cheese_str(size: int):
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = cheese_str(int(c.size))
                else:
                    s = cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines


class Cheese:
    def __init__(self: 'Cheese', size: int):
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __repr__(self: 'Cheese') -> str:
        """
        Representation of this Cheese
        """
        return "Cheese(" + str(self.size) + ")"

    def __eq__(self: 'Cheese', other: 'Cheese') -> bool:
        """Is self equivalent to other? We say they are if they're the same
        size."""
        return isinstance(other, Cheese) and self.size == other.size


class IllegalMoveError(Exception):
    pass


class MoveSequence(object):

    def __init__(self: 'MoveSequence', moves: list):
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self: 'MoveSequence', i: int):
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self: 'MoveSequence', src_stool: int, dest_stool: int):
        self._moves.append((src_stool, dest_stool))

    def length(self: 'MoveSequence') -> int:
        return len(self._moves)

    def generate_TOAHModel(self: 'MoveSequence', number_of_stools: int,
                           number_of_cheeses: int) -> 'TOAHModel':
        """
        An alternate constructor for a TOAHModel. Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in move_seq.
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model

    def __repr__(self: 'MoveSequence') -> str:
        return "MoveSequence(" + repr(self._moves) + ")"


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
