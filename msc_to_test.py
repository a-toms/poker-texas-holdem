import mini_sudoku_creator

class TestGetColumnValues:

    grid_length = mini_sudoku_creator.GRID_SIDE_LENGTH
    grid = mini_sudoku_creator.create_grid()

    def test_create_grid(self):
        grid = mini_sudoku_creator.create_grid()
        assert type(grid) is list
        assert type(grid[0]) is list
        assert len(grid) == self.grid_length

    def test_get_possible_cells(self):
        cells = mini_sudoku_creator.get_possible_cells()
        assert None not in cells
        assert self.grid_length - 1 in cells

    def test_get_cell_value_that_fits(self):



