
# Sudoku SAT solver

# Usage

1. Install a SAT solver, such as [Minisat](http://minisat.se/)
2. To get a solution run `python3 sudoku.py $sudoku board$`, where $sudoku board$ is a representation of the board with `'.'` for empty cells : e.g. `.......1.4.........2...........5.4.7..8...3....1.9....3..4..2...5.1........8.6...`. The solution will be printed out to the screen.
3. To count the number of solutions run `python3 sudoku.py -c $sudoku board$`. The number of solutions will be printed out to the screen.
