# sudoku.py
# Sudoku solver using constraint propagation and DFS
# Aviva Blonder

import numpy as np
import math
import queue

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
                    # and add it to the propagation queue so its value can be propagated to its neighbors
                    self.propq.put(self.puzzle[row,col])


    def solve(self):
        """ Solves the loaded puzzle and returns the result as a string. """

        # while there are indices in the propagation queue, propagate those
        while not self.propq.empty():
            # pop the square at the end of the queue
            sq = self.propq.get()
            # propagate that value to its row
            self.propagate(sq.val, self.puzzle[:, sq.col])
            # and its column
            self.propagate(sq.val, self.puzzle[sq.row, :])
            # find which column of boxes it's in
            col = math.floor(sq.col/3)
            # and which row
            row = math.floor(sq.row/3)
            # grab that box
            box = self.puzzle[row*3:row*3+3, col*3:col*3+3]
            # flatten it and propagate the value to it too
            self.propagate(sq.val, box.flatten())
            
        # TODO - implement search for when the puzzle isn't completely solved by constraint propagation

        # string representation of the solved puzzle
        puzzlestr = ""
        # loop through each row and column in the puzzle
        for row in self.puzzle:
            for col in row:
                # add the string represetnation of that square
                puzzlestr += str(col)
        # return the string
        return puzzlestr


    def propagate(self, value, neighbors):
        """ Propagates the designated value to all elements in the provided list of neighbors. """

        # loop through all the neighboring squares in the list provided and, if they don't have values of their own yet, propagate the constraint to them
        for sq in neighbors:
            # if the square's value is a list of possible values, and it contains value, remove value from it
            if isinstance(sq.val, list) and value in sq.val:
                sq.val.remove(value)
                # if the list now only contains one value, give it that value and propagate it
                if len(sq.val) == 1:
                    sq.val = sq.val[0]
                    self.propq.put(sq)
            # if the square's value is an integer that is equal to value, return false
            if sq.val == value:
                return False



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
    # solve each puzzle in the file
    for line in file:
        solver = Solver(line.strip('\n'))
        # solve the puzzle and print the results
        print(solver.solve())
        # lets just solve the first puzzle for now
        break

main("euler.txt")
    
