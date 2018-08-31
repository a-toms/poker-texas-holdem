#! python3
# mini_sudoku_creator.py

import random
import pprint
import logging

logging.basicConfig(level=logging.WARNING)


GRID_SIDE_LENGTH = 7


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
        if row == []:
            pass
        elif assert_no_duplicates_present(row) is False:
            return False
    else:
        return True


def no_duplicates_in_grid_columns(grid):
    """check if there are duplicates in the grid's columns"""
    columns = convert_grid_columns_to_rows(grid)
    for col in columns:
        if assert_no_duplicates_present(col) == False:
            return False
    return True


def convert_grid_columns_to_rows(grid):
    """create list of column values"""
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


def none_not_present(grid):
    """check None in not in any grid row"""
    for row in grid:
        if None in row:
            return False
    else:
        return True


def does_the_grid_follow_the_rules(grid):
    """check that the grid contains unique numbers in every column and row,
    and contains no None value"""
    if none_not_present(grid) is False:
        return False
    if no_duplicates_in_grid_rows(grid) is False:
        return False
    if no_duplicates_in_grid_columns(grid) is False:
        return False
    else:
        return True


def build_random_row():
    """Produce a row with random values"""
    possible_values = get_possible_values()
    row = []
    for i in range(len(possible_values)):
        choice = random.choice(possible_values)
        row.append(choice)
        possible_values.remove(choice)
    return row


def add_numbers(grid):
    """add the correct numbers to the grid"""
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
    """create the empty grid and add correct numbers that follow the rules"""
    add_numbers(create_empty_grid())


build_grid()


# Todo: test the difference in speeds as I increase the grid side length. Use time.time

