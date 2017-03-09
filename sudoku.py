# sudoku.py
# Sudoku solver using constraint propagation and DFS
# Aviva Blonder

import numpy as np
import math
import queue
import copy

class Solver():
    

    def __init__(self, puzzlestring):
        """ Takes in a puzzle as a string of numbers and periods and saves it as a numpy array. """

        # initialize queue of indices in the puzzle whose value needs to be propagated to its neighbors
        self.propq = queue.Queue()
        
        # initialize the puzzle as an empty array
        self.puzzle = np.empty((9, 9), dtype = Square)

        # loop through each row in the array and fill it with a square representing the corresponding character in the puzzlestring
        for row in range(9):
            for col in range(9):
                # grab the corresponding value from the puzzlestring
                val = puzzlestring[row*9 + col]
                # if the value is a period, make a square with its value as a list of possible values instead
                if val == ".":
                    self.puzzle[row, col] = Square([1, 2, 3, 4, 5, 6, 7, 8, 9], row, col)
                # otherwise, just give it the integer value
                else:
                    self.puzzle[row, col] = Square(int(val), row, col)
                    # add it to the propagation queue so its value can be propagated to its neighbors
                    self.propq.put(self.puzzle[row,col])


    def solve(self, puzzle = None):
        """ Recursively solves the designated puzzle and returns the result as a string. """

        # if no puzzle was provided, just fill it in with the originally loaded one
        if puzzle is None:
            puzzle = self.puzzle
        # while there are indices in the propagation queue, propagate those
        while not self.propq.empty():
            # pop the square at the end of the queue
            sq = self.propq.get()
            # propagate that value to its row, if it runs into a conflict, return false to say that this path did not work
            if not self.propagate(sq, puzzle[:, sq.col]):
                return False
            # same for its column
            if not self.propagate(sq, puzzle[sq.row, :]):
                return False
            # find which column of boxes it's in
            col = math.floor(sq.col/3)
            # and which row
            row = math.floor(sq.row/3)
            # grab that box
            box = puzzle[row*3:row*3+3, col*3:col*3+3]
            # flatten it and propagate the value to it too
            if not self.propagate(sq, box.flatten()):
                return False

        # if no value has been returned yet, that means we have to find an unfilled square to asign a value to and recurse on that new puzzle
        for row in range(9):
            for col in range(9):
                # grab the square at that row and column
                sq = puzzle[row, col]
                # if the value of the square at that row and column is a list, recurse on it
                if isinstance(sq.val, list):
                    # loop through all of its possible values, if one of them is successful, return that
                    for val in sq.val:
                        # create a copy of the puzzle with that square's value equal to val
                        newpuz = copy.deepcopy(puzzle)
                        newpuz[row, col].val = val
                        # create a new propagation queue
                        self.propq = queue.Queue()
                        # and add that square to it
                        self.propq.put(newpuz[row, col])
                        # recurse on the new puzzle and store the result
                        result = self.solve(puzzle = newpuz)
                        # if it was successful, return the result
                        if result:
                            return result
                    # if none of the values were successful return false
                    return False

        # if no value has been returned yet, that means there were no unfilled squares, so the puzzle has been solved! Now we can return it as a string
        # string representation of the solved puzzle
        puzzlestr = ""
        # loop through each row and column in the puzzle
        for row in puzzle:
            for col in row:
                # add the string represetnation of that square
                puzzlestr += str(col)
        # return the string
        return puzzlestr        


    def propagate(self, propsq, neighbors):
        """ Propagates the designated value to all elements in the provided list of neighbors. """

        # loop through all the neighboring squares in the list provided and, if they don't have values of their own yet, propagate the constraint to them
        for sq in neighbors:
            # if the square's value is a list of possible values, and it contains the propagated value, remove that from it
            if isinstance(sq.val, list) and propsq.val in sq.val:
                sq.val.remove(propsq.val)
                # if the list now only contains one value, give it that value and propagate it
                if len(sq.val) == 1:
                    sq.val = sq.val[0]
                    self.propq.put(sq)
                # if the list is empty, return false
                elif len(sq.val) == 0:
                    return False
            # if the square's value is an integer that is equal to the propagated square's value, return false
            if sq.val == propsq.val and not sq is propsq:
                return False
        # if that all succeeds, return true
        return True



""" One square on the sudoku board as an object for my convenience. """
class Square():

    def __init__(self, val, row, col):
        """ Store the square's value and location """
        self.val = val
        self.row = row
        self.col = col

    def __str__(self):
        """ toString method that returns the square's value as a string """
        return str(self.val)


""" Main method from which the puzzles are loaded and turned into solver objects """
def main(fname):
    # open the designated file
    file = open(fname, "r")
    # create a file to write the solutions to
    solutions = open("solutions" + fname, "w")
    # solve each puzzle in the file
    for line in file:
        solver = Solver(line.strip('\n'))
        # solve the puzzle and write the results to the solution file
        solutions.write(solver.solve() + '\n')
