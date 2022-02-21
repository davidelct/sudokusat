import math
import itertools

class Board():
    """ 
    A NxN sudoku board that might have some pre-filled values
    """
    def __init__(self, string):
        """
        Create a Board object from a string of 81 chars in the .[1-9] range
        - A '.' char means that the position is empty
        - A digit in [1-9] means that the position is holds that value
        """
        size = math.sqrt(len(string))
        if not size.is_integer():
            raise RuntimeError(f'Expected a square board, but got a string of \
                len {len(string)}')
        
        self.data = [0 if x == '.' else int(x) for x in string]
        self.size_ = int(size)

    def size(self):
        """ 
        Return the size of the board, e.g. 9 if the board is a 9x9 board
        """
        return self.size_

    def value(self, x, y):
        """ 
        Return the value at row x and column y
        """
        return self.data[x*self.size_ + y]

    def all_coordinates(self):
        """
        Return all possible coordinates in the board
        """
        return ((x+1, y+1) for x, y in itertools.product(range(self.size_), repeat=2))

    def print(self):
        """
        Print the board in "matrix" form
        Works for 9x9 boards
        """
        assert self.size_ == 9
        for i in range(self.size_):
            base = i * self.size_
            row = self.data[base:base + 3] + ['|'] + self.data[base + 3:base + 6]\
                 + ['|'] + self.data[base + 6:base + 9]
            print(" ".join(map(str, row)))
            if (i + 1) % 3 == 0:
                print("")