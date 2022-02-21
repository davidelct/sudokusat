#!/usr/bin/env python3

import argparse
import itertools
import math
import sys

from utils import save_dimacs_cnf, solve
from board import Board


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("board", help="A string encoding the Sudoku board, with all rows concatenated,"
                                      " and 0s where no number has been placed yet.")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not print any output.')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Count the number of solutions.')
    return parser.parse_args(argv)


def print_solution(solution):
    """
    Print a solved Sudoku board in "matrix" form
    """
    print(f'Solution: {"".join(map(str, solution))}')
    print('Solution in board form:')
    Board(solution).print()


def compute_solution(sat_assignment, variables, size):
    solution = []

    for i in sat_assignment:

        if sat_assignment[i]:
            if i%9: solution.append((i%9))
            else: solution.append(9) 

    return solution


def generate_theory(board, verbose):
    """
    Generate the propositional theory that corresponds to the given board
    """
    size = board.size()
    clauses = []
    variables = [*range(1, size**3 + 1)]


    # Step 1 : Add the pre-filled values, if any
    clauses += [
        [str(size*i + board.data[i])] for i in range(size**2) if board.data[i]
    ]


    # Step 2 : Add clauses for cells
    cell_idx = [variables[i:i+size] for i in range(0, size**3, size)]

    cell_clauses = [
        [list(map(str, cell))] + [[f"-{i}", f"-{j}"] for i in cell for j in cell if j>i]
        for cell in cell_idx
    ]
    clauses += [item for clause in cell_clauses for item in clause]


    # Step 3 : Add clauses for rows
    row_idx = [[cell[i] for cell in cell_idx[j:j+size]] for j in range(0,size**2,size) for i in range(size)]

    row_clauses = [
        [list(map(str, row))] + [[f"-{i}", f"-{j}"] for i in row for j in row if j>i]
        for row in row_idx
    ]
    clauses += [item for clause in row_clauses for item in clause]


    # Step 4 : Add clauses for columns
    col_idx = [[cell[i] for cell in cell_idx[j::size]] for j in range(0,size) for i in range(size)]

    col_clauses = [
        [list(map(str, col))] + [[f"-{i}", f"-{j}"] for i in col for j in col if j>i]
        for col in col_idx
    ]
    clauses += [item for clause in col_clauses for item in clause]


    # Step 5: Add clauses for blocks
    block_size = int(math.sqrt(size))
    block_idx = [
        [row_idx[size*i+level][j:j+block_size] + 
        row_idx[size*(i+1)+level][j:j+block_size] + 
        row_idx[size*(i+2)+level][j:j+block_size] 
        for j in range(0, size, block_size) for level in range(size)
        ] 
        for i in range(0, size, block_size)
    ]
    block_idx = [item for clause in block_idx for item in clause]

    block_clauses = [
        [list(map(str, block))] + [[f"-{i}", f"-{j}"] for i in block for j in block if j>i]
        for block in block_idx
    ]
    clauses += [item for clause in block_clauses for item in clause]

    return clauses, variables, size

def count_number_solutions(board, verbose=False):
    count = 0

    clauses, vars, size = generate_theory(board, verbose=verbose)
    sigma = solve_sat_problem(clauses=clauses, filename="c-sudoku.cnf", size=size, variables=vars, verbose=verbose)

    while sigma:
        count += 1
        new_constraint = []
        #we want to take the true variables of the previous solution and negate their intersection 
        #(in other words take the union of negated variables)
        new_constraint += [str(-i) for i in range(len(sigma)) if sigma[i]]     
        ' '.join(new_constraint)
        clauses += [new_constraint]
        sigma = solve_sat_problem(clauses=clauses, filename="c-sudoku.cnf", size=size, variables=vars, verbose=verbose)

    print(f'Number of solutions: {count}')


def find_one_solution(board, verbose=False):
    clauses, variables, size = generate_theory(board, verbose)
    return solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)


def solve_sat_problem(clauses, filename, size, variables, verbose):
    
    save_dimacs_cnf(variables, clauses, filename, verbose)
    
    result, sat_assignment = solve(filename, verbose)
    
    if result != "SAT":
        if verbose:
            print("The given board is not solvable")
        return None
    
    solution = compute_solution(sat_assignment, variables, size)
    
    if verbose:
        print_solution(solution)
    
    return sat_assignment

def main(argv):
    args = parse_arguments(argv)
    board = Board(args.board)

    if args.count:
        count_number_solutions(board, verbose=False)
    else:
        find_one_solution(board, verbose=not args.quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
