#! python3
# mini_sudoku_creator.py

import random
import pprint
import copy
from contextlib import suppress
import logging

logging.basicConfig(level=logging.INFO)


GRID_SIDE_LENGTH = 5

def create_grid():
    grid = []
    for i in range(GRID_SIDE_LENGTH):
        row = []
        grid.append(row)
    return grid


def get_possible_values():
    values = [i for i in range(GRID_SIDE_LENGTH)]
    return values


def assert_no_duplicates_present(sequence):
    return len(sequence) == len(set(sequence))


def no_duplicates_in_grid_rows(grid):
    for counter, row in enumerate(grid):
        if assert_no_duplicates_present(row) is False:
            return False
    else:
        return True


def convert_grid_columns_to_rows(grid):
    columns = []
    for i in range(GRID_SIDE_LENGTH):
        try:
            column = []
            for j in range(GRID_SIDE_LENGTH):
                column.append(grid[j][i])
        except IndexError:
            pass
        if column != []:
            columns.append(column)
    return columns


def no_duplicates_in_grid_columns(grid):
    columns = convert_grid_columns_to_rows(grid)
    for col in columns:
        if assert_no_duplicates_present(col) == False:
            return False
    return True


def none_not_present(grid): # Working
    for counter, row in enumerate(grid):
        if None in row:
            return False
    else:
        return True


# todo: working here
def add_numbers(grid):
    print(grid)
    for i in range(len(grid)):
        row = build_random_row()
        grid[i].extend(row)
        if no_duplicates_in_grid_columns(grid) is True:
            print(no_duplicates_in_grid_columns(grid))
            break
        else:
            print(no_duplicates_in_grid_columns(grid))
            continue

    print(grid)
    print('complete')





def all_grid_tests_pass(grid):
    #logging.info(f"None not present = {none_not_present(grid)}")
    #logging.info(f"No duplicates in grid rows = {no_duplicates_in_rows(grid)}")
    #logging.info(f"No duplicates in columns = {no_duplicates_in_columns(grid)}")
    if none_not_present(grid) is False:
        return False
    if no_duplicates_in_rows(grid) is False:
        return False
    if no_duplicates_in_grid_columns(grid) is False:
        return False
    else:
        return True
