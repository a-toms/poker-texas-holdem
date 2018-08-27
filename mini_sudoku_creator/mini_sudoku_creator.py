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


def assert_no_duplicates_present(sequence):
    return len(sequence) == len(set(sequence))


def add_numbers(grid):
    for row in grid:
        possible_values = get_possible_values()
        while len(row) != GRID_SIDE_LENGTH:
            choice = random.choice(possible_values)
            row.append(choice)
            if all_grid_tests_pass(grid) is True: # This is non-functional.
                possible_values.remove(choice)
            else:
                del row[:]
        print(grid)


def get_possible_values():
    values = [i for i in range(GRID_SIDE_LENGTH)]
    return values


def no_duplicates_in_rows(grid):
    for counter, row in enumerate(grid):
        if assert_no_duplicates_present(row) is False:
            return False
    return True


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
    logging.info(columns)
    return columns


def no_duplicates_in_columns(grid): # Working
    result = no_duplicates_in_rows(convert_columns_to_rows(grid))
    return result


def none_not_present(grid): # Working
    for counter, row in enumerate(grid):
        if None in row:
            return False
    else:
        return True


def all_grid_tests_pass(grid):
    #logging.info(f"None not present = {none_not_present(grid)}")
    #logging.info(f"No duplicates in grid rows = {no_duplicates_in_rows(grid)}")
    logging.info(f"No duplicates in columns = {no_duplicates_in_columns(grid)}")
    if none_not_present(grid) is False:
        return False
    if no_duplicates_in_rows(grid) is False:
        return False
    if no_duplicates_in_columns(grid) is False:
        return False
    else:
        return True


add_numbers(create_grid())