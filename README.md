## A Simple Sudoku Solver

Implementation: It first attempts to solve the the sudoku with constraint propagation. However, when it reaches a point where it has to guess, it uses a depth first search to try out each possibility and eliminate the paths that don't work until it finds one that does.

See euler.txt and magictour.txt for sample sudoku puzzles in a format that can be processed by the solver.

Debugging: Initially, it didn't return any errors, just the wrong output. Eventually, I figured out that I was interrupting constraint propagation after propagating a square's value to only its first neighbor. I fixed the bug and was able to get it to solve sudokus successfuly.
