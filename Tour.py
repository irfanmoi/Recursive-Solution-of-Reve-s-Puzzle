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
from ConsoleController import ConsoleController
from GUIController import GUIController
from TOAHModel import TOAHModel


import time
NUM_CHEESES = 3


def choice_of_i(n):

    '''(int) -> float

    Returns the most optimum choice of i, which is used in solving the
    four stools puzzle and is dependent on the given number of cheeses.

    Optimum choice always results in M(n) = {1 if n == 1, 2*M(n-i) + 2^i -1 for
    n > 1} moves required to solve Anne Hoy's cheese moving problem for n
    number of cheeses.

    >>> i = choice_of_i(0)
    >>> int(i)
    0
    >>> i = choice_of_i(1)
    >>> int(i)
    1
    >>> i = choice_of_i(2)
    >>> int(i)
    1
    >>> i = choice_of_i(3)
    >>> int(i)
    2
    >>> i = choice_of_i(4)
    >>> int(i)
    2
    >>> i = choice_of_i(100000)
    >>> int(i)
    446

    REQ: n >= 0
    '''
    # Uses quadratic formula to solve 0.5i^2 + 0.5i - n to solve for the most
    # optimum i!
    # Quadratic formula optimized to always return positive solution
    return -0.5 + ((0.25 - 2*-n)**0.5)


def helper_three_stools(moves, n, origin, spare, dest):

    '''(list, int, int, int, int) -> NoneType

    Given empty list, number of cheeses, and ints to indicate different
    representations of stools, modifies the list to store moves as tuples
    which are the solutions of three stool instance of the cheese-moving
    problem.

    >>> moves = []
    >>> helper_three_stools(moves, 0, 0, 1, 2)
    >>> moves == []
    True
    >>> helper_three_stools(moves, 1, 0, 1, 2)
    >>> moves == [(0, 2)]
    True
    >>> moves = []
    >>> helper_three_stools(moves, 2, 0, 1, 2)
    >>> moves
    [(0, 1), (0, 2), (1, 2)]
    >>> moves = []
    >>> helper_three_stools(moves, 16, 0, 1, 2)
    >>> from TOAHModel import MoveSequence
    >>> ms = MoveSequence(moves)
    >>> ms.length() == 2**16 - 1
    True
    >>> len(moves)
    65535
    >>> model = ms.generate_TOAHModel(3, 16)
    >>> model.top_cheese(2).size
    1
    >>> from TOAHModel import Cheese
    >>> model.cheese_location(Cheese(16))
    2
    >>> model.cheese_location(Cheese(15))
    2
    >>> model.cheese_location(Cheese(14))
    2
    >>> model.cheese_location(Cheese(13))
    2
    >>> model.cheese_location(Cheese(12))
    2
    >>> model.cheese_location(Cheese(11))
    2
    >>> model.cheese_location(Cheese(10))
    2
    >>> model.cheese_location(Cheese(9))
    2
    >>> model.cheese_location(Cheese(8))
    2
    >>> model.cheese_location(Cheese(7))
    2
    >>> model.cheese_location(Cheese(6))
    2
    >>> model.cheese_location(Cheese(5))
    2
    >>> model.cheese_location(Cheese(4))
    2
    >>> model.cheese_location(Cheese(3))
    2
    >>> model.cheese_location(Cheese(2))
    2
    >>> model.cheese_location(Cheese(1))
    2
    >>> model.number_of_cheeses() == 16
    True
    >>> model.number_of_stools() == 3
    True
    '''

    # added extra base case just in case
    if n == 0:
        pass
    # if there is only one cheese, move it to destination

    elif n == 1:
        # add it to list of moves
        moves.append((origin, dest))

    # if there are more than 1 cheeses, solve the problem recursively
    else:
        # recursively move the cheeses on to the spare stool
        helper_three_stools(moves, n-1, origin, dest, spare)
        # move the n'th cheese to destination!
        # add to the list of moves! as a tuple
        moves.append((origin, dest))
        # recursively move the cheeses to destination from spare
        helper_three_stools(moves, n-1, spare, origin, dest)


def helper_four_stools(moves, n, origin, spare_1, spare_2, dest):

    '''(list, int, int, int, int, int) -> NoneType

    Given empty list, number of cheeses, and ints to indicate different
    representations of stools, modifies the list to store moves as tuples
    which are the solutions of four stool instance of the cheese-moving
    problem.

    >>> moves = []
    >>> helper_four_stools(moves, 0, 0, 1, 2, 3)
    >>> moves == []
    True
    >>> helper_four_stools(moves, 1, 0, 1, 2, 3)
    >>> moves == [(0, 3)]
    True
    >>> moves = []
    >>> helper_four_stools(moves, 2, 0, 1, 2, 3)
    >>> moves
    [(0, 1), (0, 3), (1, 3)]
    >>> moves = []
    >>> helper_four_stools(moves, 3, 0, 1, 2, 3)
    >>> moves
    [(0, 1), (0, 2), (0, 3), (2, 3), (1, 3)]

    >>> moves = []

    >>> helper_four_stools(moves, 30, 0, 1, 2, 3)
    >>> len(moves) == 1025
    True
    >>> from TOAHModel import MoveSequence
    >>> ms = MoveSequence(moves)
    >>> ms.length() == 1025
    True
    >>> len(moves)
    1025
    >>> model = ms.generate_TOAHModel(4, 30)
    >>> model.top_cheese(3).size
    1
    >>> model.number_of_cheeses() == 30
    True
    >>> model.top_cheese(3).size
    1
    >>> from TOAHModel import Cheese
    >>> model.cheese_location(Cheese(30))
    3
    >>> model.cheese_location(Cheese(29))
    3
    >>> model.cheese_location(Cheese(28))
    3
    >>> model.cheese_location(Cheese(27))
    3
    >>> model.cheese_location(Cheese(26))
    3
    >>> model.cheese_location(Cheese(25))
    3
    >>> model.cheese_location(Cheese(24))
    3
    >>> model.cheese_location(Cheese(23))
    3
    >>> model.cheese_location(Cheese(22))
    3
    >>> model.cheese_location(Cheese(21))
    3
    >>> model.cheese_location(Cheese(20))
    3
    >>> model.cheese_location(Cheese(19))
    3
    >>> model.cheese_location(Cheese(18))
    3
    >>> model.cheese_location(Cheese(17))
    3
    >>> model.cheese_location(Cheese(16))
    3
    >>> model.cheese_location(Cheese(15))
    3
    >>> model.cheese_location(Cheese(13))
    3
    >>> model.cheese_location(Cheese(12))
    3
    >>> model.cheese_location(Cheese(11))
    3
    >>> model.cheese_location(Cheese(10))
    3
    >>> model.cheese_location(Cheese(9))
    3
    >>> model.cheese_location(Cheese(8))
    3
    >>> model.cheese_location(Cheese(7))
    3
    >>> model.cheese_location(Cheese(6))
    3
    >>> model.cheese_location(Cheese(5))
    3
    >>> model.cheese_location(Cheese(4))
    3
    >>> model.cheese_location(Cheese(3))
    3
    >>> model.cheese_location(Cheese(2))
    3
    >>> model.cheese_location(Cheese(1))
    3

    '''
    # i is 0 for now
    i = 0

    # extra base case, just in case
    # if there are no cheeses, then do nothing
    if n == 0:
        pass

    # if there is only 1 cheese, move it to the destination!
    elif n == 1:
        # add it to the list of moves as a tuple
        moves.append((origin, dest))

    else:
        # calculate the i which gives the least # of moves
        i = int(choice_of_i(n))
        # recursively move n - i cheeses to spare stool 1
        helper_four_stools(moves, n - i, origin, dest, spare_2, spare_1)
        # recursively move the remaining i cheeses to the destination,
        # using every stool except stool 1
        # since we have only 3 stools in this case, we can use the same
        # algorithm which gets done in 2^i - 1 moves!
        helper_three_stools(moves, i, origin, spare_2, dest)
        # recursively move the n-i from spare stool 1 to the destination
        # (these were moved to spare stool 1 earlier)
        helper_four_stools(moves, n - i, spare_1, origin, spare_2, dest)


def tour_of_four_stools(model: TOAHModel, delay_btw_moves: float=0.5,
                        console_animate: bool=False,):
    """Move a tower of cheeses from the first stool in model to the fourth.

       model - a TOAHModel with a tower of cheese on the first stool
                and three other empty stools
       console_animate - whether to use ConsoleController to animate the tour
       delay_btw_moves - time delay between moves in seconds IF
                         console_animate == True
                         no effect if console_animate == False
    """
    # store the number of cheeses in n, because it's shorter and easier
    n = model.number_of_cheeses()
    # create an empty list to store the moves (in tuple form)
    moves = []
    # call the helper function so the solution can be stored in moves
    helper_four_stools(moves, n, 0, 1, 2, 3)

    # if user wants to animate
    if console_animate is True:
        # grab a movie one by one and apply it to the given model
        # until the moves list is empty
        while len(moves) != 0:
            # temp is basically the first move in the list
            # it's a tuple
            temp = moves[0]
            # delete that move from the original moves list because we
            # already saved it and we won't need it again
            moves = moves[1:]
            # since temp is a tuple, temp[0] is the original stool and
            # temp[1] is the destination stool: temp = (temp[0], temp[1])
            model.move(temp[0], temp[1])
            # if user wants a delay between moves, use sleep to pause
            time.sleep(delay_btw_moves)
            # print a visual representation of the model being changed
            print(model)

    # if user does not any animation, only the model is changed
    else:
        # exact same thing but this time there is no delay between moves
        while len(moves) != 0:
            # get origin stool
            temp = moves[0]
            # get destination stool
            moves = moves[1:]
            # change the model
            model.move(temp[0], temp[1])

if __name__ == '__main__':
    # DO NOT MODIFY THE CODE BELOW.

    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=8)

    tour_of_four_stools(four_stools,
                        console_animate=False,
                        delay_btw_moves=0.5)

    print(four_stools.number_of_moves())
