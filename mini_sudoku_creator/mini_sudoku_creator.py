#! python3
# mini_sudoku_creator.py

import random
import pprint
import copy
from contextlib import suppress
import logging

logging.basicConfig(level=logging.INFO)

# todo: refine script to remove None outputs
# todo: consider adding unit testing.


GRID_SIDE_LENGTH = 5

def create_grid():
    grid = []
    for i in range(GRID_SIDE_LENGTH):
        row = []
        grid.append(row)
    return grid

# def assert_number_not_repeated_in_column(n, row, grid):
#     test_row = copy.deepcopy(row)
#     test_row.append(n)
#     n_position = test_row.index(n)
#     logging.info(f'{n_position}')
#     with suppress(IndexError):
#         columns = []
#         for i in range(GRID_SIDE_LENGTH):
#             columns.append(grid[i][n_position])
#     print(columns)


def assert_duplicates_not_present(sequence):
    return bool(len(sequence) == len(set(sequence)))


def assert_none_not_in_sequence(sequence):
    return None not in sequence


# def check_number_fits(n, row, grid):
#     """Check chosen number fits with existing grid numbers."""
#     if assert_duplicates_not_present(row) is not True:
#         return False
#     # if assert_number_not_repeated_in_column(n, row, grid) is not True:
#     #     return False
#     if assert_none_not_in_sequence(row) is not True:
#         return False
#     else:
#         return True


def add_numbers(grid):
    for row in grid:
        possible_values = get_possible_values()
        while len(row) != GRID_SIDE_LENGTH:
            choice = random.choice(possible_values)
            row.append(choice)
            # if check passes
            possible_values.remove(choice)
            # else: def row[-1] continue
    logging.info(pprint.pprint(grid))


def get_possible_values():
    values = [i for i in range(GRID_SIDE_LENGTH)]
    return values


#add_numbers(create_grid())

test_grid = [
    [1, 0, 3, 1, 1],
    [1, 1, 1, 3, 2],
    [3, 2, 0, 2, 9],
    [2, 1, 4, 0, 3],
    [3, 0, 2, 4, 8]
]


def test_rows_for_duplication(grid): # Working
    for counter, row in enumerate(grid):
        print(f'row {counter} {assert_duplicates_not_present(row)}')


def convert_columns_to_rows(grid):
    columns = []
    try:
        for i in range(GRID_SIDE_LENGTH):
            column = []
            for j in range(GRID_SIDE_LENGTH):
                column.append(grid[j][i])
            columns.append(column)
    except IndexError:
        pass
    return columns


def test_columns_for_duplication(grid): #Working
    test_rows_for_duplication(convert_columns_to_rows(grid))

def test_for_none(grid): #Working
    for counter, row in enumerate(grid):
        print(f'row {counter} None present = {None not in row}')


def test_the_grid(grid):
    test_for_none(grid)





test_the_grid(test_grid)
