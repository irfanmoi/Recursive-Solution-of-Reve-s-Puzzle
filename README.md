# reve-puzzle-recursive-solution

Implementation of the recursive "optimal solution" for the [Reve's puzzle][revepuzzle] problem, in python.

- Background:

The Tower of Hanoi puzzle was invented by French mathematician Édouard Lucas in 1883. The game consists of three rods and any number of n disks of different diameters. These disks can slide onto any rod. Originally, all of the disks are placed on any rod and they form a stack in decreasing order. In other words, the largest disk is at the top, and vice versa. The purpose of this game is to move the entire tower of disks to any other rod. However, there are there are certain restrictions:

1) Only one disk can be moved from one rod to another
2) A large disk cannot be placed on a smaller one

It takes 2^n -1 moves to accomplish this. Nevertheless, in 1908, Henry Ernest Dudeney complicated the puzzle, by adding a fourth rod. This is known as "The Reve's Puzzle". 

The most efficient known recursive solution to Reve's puzzle is the "Frame-Stewart Algorithm". It can be found in the Tour.py file.

# instructions
