#! python3
# mini_sudoku_creator.py

import random
import pprint
import logging
import time
logging.basicConfig(level=logging.WARNING)

GRID_SIDE_LENGTH = 5

def create_empty_grid():

    grid = []
    for _ in range(GRID_SIDE_LENGTH):
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
    return grid


def build_grid():
    """create the empty grid and insert the numbers that follow the rules"""
    start_time = time.time()
    complete_grid = add_numbers(create_empty_grid())
    seconds_taken = round(time.time() - start_time, 4)
    print("--- %s seconds ---" % seconds_taken)
    return seconds_taken
"""todo: write additional test and refactor here."""


def time_the_program(upper_grid_size_length):
    """time how long the program takes to find a correct grid for all of the
    grid sizes up to upper_grid_size_length"""
    assert upper_grid_size_length is not int
    time_taken = {}
    for i in range(upper_grid_size_length):
        global GRID_SIDE_LENGTH
        GRID_SIDE_LENGTH = i
        seconds_taken = build_grid()
        time_taken[f'Time taken for grid side length {i}'] = seconds_taken
    pprint.pprint(time_taken)


if __name__ == '__main__':
    time_the_program(10)
