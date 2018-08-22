#! python3
# mini_sudoku_creator.py

import random
import pprint
import logging
logging.basicConfig(level=logging.INFO)

# todo: refine script to remove None outputs
# todo: consider adding unit testing.


GRID_SIDE_LENGTH = 5


def get_possible_values():
    cells = [i for i in range(GRID_SIDE_LENGTH)]
    return cells




def create_grid():
    grid = {}
    for i in range(GRID_SIDE_LENGTH):
        possible_values = get_possible_values()
        row = []
        for j in range(GRID_SIDE_LENGTH):
            cell = random.choice(possible_values)
            possible_values.remove(cell)
            row.append(cell)
            logging.info(cell)

        get_column_values(grid)

        if check_for_none(row) == True:
            cell = random.choice(possible_values)
            possible_values.remove(cell)
            row.append(cell)
            logging.info(cell)
            grid[i - 1] = row
        else:
            grid[i] = row


    pprint.pprint(grid)





def check_for_none(array):
    if None in array:
        return True
    else:
        return False


def get_column_values(dict):
    columns = []
    for i in range(GRID_SIDE_LENGTH):
        inner_col = []
        for j in range(GRID_SIDE_LENGTH):
            inner_col.append(dict[i][j])
        columns.append(inner_col)
    logging.info(columns)



def get_cell_value_that_fits():
    possible_cell_values = get_possible_values()
    possible_cell_values -= set(column_values)
    return choose_random_number(list(possible_cell_values))





''' todo: backtracking'''

def engine():
    grid = create_grid()



engine()
