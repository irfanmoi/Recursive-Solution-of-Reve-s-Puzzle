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
ConsoleController: User interface for manually solving Anne Hoy's problems
from the console.

move: Apply one move to the given model, and print any error message
to the console.
"""

from TOAHModel import TOAHModel, Cheese, IllegalMoveError
import tkinter as TI
import time

# HELPER FUNCTION


def input_checker(user_input):
    '''(object) -> int

    Returns an appropriate int value after recursively asking user for
    proper input. Given object can literally be anything, but console
    will stop asking user for input if user input is an int that is equal
    to or greater than 0.

    >>> n = input_checker(0)
    >>> n == 0
    True
    >>> n = input_checker(1)
    >>> n == 1
    True
    >>> n = input_checker(100)
    >>> n == 100
    True
    >>> n = input_checker(1000000000000000)
    >>> n
    1000000000000000
    >>> n == 1000000000000000
    True
    '''

    # If thereis an error in assessing the user input, simply ask user to
    # try again!
    try:
        # if user didn't input an integer, then it's simply wrong input
        isinstance(int(user_input), int)

    # if there is something wrong, then do this
    except Exception:
        # recursively asks the user to try again
        user_input = input('\nTry Again! ')
        return_input = input_checker(user_input)

    else:
        # Now we have to check if the input is the RIGHT integer!
        if int(user_input) >= 0:
            return_input = user_input

        # Since integer might be a negative (who knows)
        # then ask user to put a positive number
        else:
            print(
                'Only integer numbers greater than or equal' +
                ' to than 0 are accepted!')
            # recursively asks the user to try again
            user_input = input('\nTry Again! ')
            return_input = input_checker(user_input)

    # SINCE the system always takes the input as a string, we need to change
    # the str to integer!
    return int(return_input)


def move(model: TOAHModel, origin: int, dest: int):
    '''
    Module method to apply one move to the given model, and print any
    error message to the console.

    model - the TOAHModel that you want to modify
    origin - the stool number (indexing from 0!) of the cheese you want
             to move
    dest - the stool number that you want to move the top cheese
            on stool origin onto.

    >>> M = TOAHModel(4)
    >>> M.fill_first_stool(1)
    >>> move(M, 0, 1)
    >>> M.get_stools()
    [[], [Cheese(1)], [], []]
    >>> M = TOAHModel(4)
    >>> M.fill_first_stool(4)
    >>> move(M, 0, 1)
    >>> move(M, 0, 2)
    >>> move(M, 1, 2)
    >>> M.get_stools() == [[Cheese(4), Cheese(3)], [], [Cheese(2),\
    Cheese(1)], []]
    True
    >>> move(M, 2, 1)
    >>> M.get_stools()
    [[Cheese(4), Cheese(3)], [Cheese(1)], [Cheese(2)], []]
    >>> move(M, 0, 3)
    >>> M.get_stools() ==  [[Cheese(4)], [Cheese(1)], [Cheese(2)], \
    [Cheese(3)]]
    True
    >>> move(M, 0, 1)
    Traceback (most recent call last):
    ...
    TOAHModel.IllegalMoveError: Cannot move bigger Cheese onto smaller Cheese
    >>> M = TOAHModel(4)
    >>> move(M, 0, 1)
    Traceback (most recent call last):
    ...
    TOAHModel.IllegalMoveError: This stool is empty!

    REQ: model.top_cheese(dest).size > model.top_cheese(origin).size
    '''
    # Already implemented in TOAHModel. Better to simply use it.
    model.move(origin, dest)


class ConsoleController:

    def __init__(self: 'ConsoleController',
                 number_of_cheeses: int, number_of_stools: int):
        """
        Initialize a new 'ConsoleController'.

        number_of_cheeses - number of cheese to tower on the first stool,
                            not counting the bottom cheese acting as stool
        number_of_stools - number of stools, to be shown as large cheeses
        """
        # Initialize CC class with # of cheeses/stools

        self._number_of_cheeses = number_of_cheeses
        self._number_of_stools = number_of_stools

    def play_loop(self: 'ConsoleController'):
        '''
        Console-based game.
        TODO:

        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.

        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.

        -After each valid move, use the method TOAHModel.__str__ that we've
        provded to print a representation of the current state of the game.
        '''
        # Start off with terminate being false since user hasn't made a
        # decision yet
        terminate = False
        # ask for user input
        user_input = input("\nOrigin stool? ")
        # change terminate status to True if user wants to quit the game
        if user_input == 'quit':
            terminate = True

        else:
            # As long puts a proper stool number and it's not bigger
            # than the number of stools in the game
            origin = input_checker(user_input)
            # Now ask for destination
            user_input = input("\nDestination stool? ")
            # if user wants to quit now, then change status to True
            # and run no more code
            if user_input == 'quit':
                terminate = True

            else:
                # Same thing here, as long as stool number is
                # in the game
                dest = input_checker(user_input)
                # if not, then remind user to pick a proper number
                # if user's input is something goofy, then simply
                # run the loop again and tell user to run again
                # remind user of how the model looks
                print(new_model)
                # and moves
                print('\nmove count:', new_model.number_of_moves())

        if terminate is False:

            try:
                # if anything goes wrong, simply ask user to try again
                move(new_model, int(origin), int(dest))

            except Exception:
                print('\nTry Again!')

            print(new_model)

            print('\nmove count:', new_model.number_of_moves())
            # run the loop again if terminate is not True!
            self.play_loop()

        elif terminate is True:
            # stop the game when user wants to!
            print('\nGood Game!')

if __name__ == '__main__':
    # TODO:
    # You should initiate game play here. Your game should be playable by
    # running this file.

    # Prints instructions
    print('\nWelcome!\n')
    print('Type "quit" anytime to exit.')
    print(
        'The purpose of this game is to move all the cheeses' +
        'from origin stool to destination stool using minimal moves.')
    print('The only rule you need to follow is:')
    print('You cannot place a bigger cheese on top of a smaller cheese!')
    print('\nGood Luck!\n')
    print(
        '"Origin stool" is the stool where you' +
        'will be moving the cheese from.')
    print(
        '"Destination stool" is the stool' +
        'where the cheese will be moved to.\n')

    print('How many cheeses?')
    # Asks user for number of cheeses/stools he/she wants to implement
    # in the game
    number_of_cheeses = input()
    # If user types 'quit' then game prints "Good Game!" and nothing else
    # happens

    if number_of_cheeses == 'quit':
        print('Good Game!')

    else:
        # check if it's the right input!
        number_of_cheeses = input_checker(number_of_cheeses)
        print('How many stools?')
        number_of_stools = input()

        # if user wants to leave, let them!
        if number_of_stools == 'quit':
            print('Good Game!')

        else:

            number_of_stools = input_checker(number_of_stools)
            # Create a new CC object and initialize with user's inputs
            new_cc = ConsoleController(int(number_of_cheeses),
                                       int(number_of_stools))
            # Also create a new TOAHModel which will be modified
            new_model = TOAHModel(int(number_of_stools))
            # Fill the first stool so the game can be played
            new_model.fill_first_stool(int(number_of_cheeses))
            # Print a string representation so user can visually see which
            # he/she plays the game
            print(new_model)
            print(new_model.number_of_moves())
            # keep looping until user wants to exit by typing 'quit'
            new_cc.play_loop()
