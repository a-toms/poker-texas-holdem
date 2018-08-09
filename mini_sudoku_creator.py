#! python3
# mini_sudoku_creator.py

import random
import pprint

# Progressing
# todo: refine script to remove None outputs
# todo: consider adding unit testing.


GRID_SIDE_LENGTH = 100


def create_grid():
    grid_rows = []
    for i in range(GRID_SIDE_LENGTH):
        blank_row = ['' for j in range(GRID_SIDE_LENGTH)]
        grid_rows.append(blank_row)
    return grid_rows


def get_cell_value_that_fits(row_values, column_values):
    possible_cell_values = get_possible_cells()
    possible_cell_values -= set(row_values)
    possible_cell_values -= set(column_values)
    if possible_cell_values != set():
        value = choose_random_number(list(possible_cell_values))
        return value


def get_possible_cells():
    cells = {i for i in range(GRID_SIDE_LENGTH)}
    return cells


def choose_random_number(array):
    number = random.choice(array)
    return number


def get_column_values(grid, cell_position):
    column = []
    for i in range(GRID_SIDE_LENGTH):
        value = grid[i][cell_position]
        column.append(value)
    return column


def insert_numbers_into_grid(grid):
    for row in grid:
        for cell in row:
            cell_position = row.index(cell)
            row_values = row
            column_values = get_column_values(grid, cell_position)
            cell_value = get_cell_value_that_fits(row_values, column_values)
            assert cell_value != None # todo: find the None bug
            row[cell_position] = cell_value


def engine():
    grid = create_grid()
    insert_numbers_into_grid(grid)
    pprint.pprint(grid)


engine()
