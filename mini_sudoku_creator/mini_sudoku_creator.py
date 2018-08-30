#! python3
# mini_sudoku_creator.py

import random
import pprint
import logging

logging.basicConfig(level=logging.WARNING)


GRID_SIDE_LENGTH = 8

def create_empty_grid():
    """Create outline grid of empty lists"""
    grid = []
    for i in range(GRID_SIDE_LENGTH):
        row = []
        grid.append(row)
    return grid


def get_possible_values():
    """get the possible values that may be inserted into the empty rows"""
    values = [i for i in range(GRID_SIDE_LENGTH)]
    return values


def assert_no_duplicates_present(sequence):
    """check no duplicates present"""
    return len(sequence) == len(set(sequence))


def no_duplicates_in_grid_rows(grid):
        for row in grid:
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
    for row in grid:
        if None in row:
            return False
    else:
        return True


def does_the_grid_follow_the_rules(grid):
    if none_not_present(grid) is False:
        return False
    if no_duplicates_in_grid_rows(grid) is False:
        return False
    if no_duplicates_in_grid_columns(grid) is False:
        return False
    else:
        return True


def build_random_row():
    possible_values = get_possible_values()
    row = []
    for i in range(len(possible_values)):
        choice = random.choice(possible_values)
        row.append(choice)
        possible_values.remove(choice)
    return row


def add_numbers(grid):
    for i in range(GRID_SIDE_LENGTH):
        while True:
            row = build_random_row()
            grid[i] = row
            logging.info(grid[i])
            if does_the_grid_follow_the_rules(grid) is True:
                print(f"Accepted row {i + 1} = {grid[i]}")
                break
            else:
                continue
    print('Complete Grid:')
    pprint.pprint(grid)


def build_grid():
    add_numbers(create_empty_grid())


build_grid()


# Todo: test the difference in speeds as I increase the grid side length. Use time.time

