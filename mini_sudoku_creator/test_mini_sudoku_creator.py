import mini_sudoku_creator as msc


def test_create_grid():
    assert len(msc.create_empty_grid()) == msc.GRID_SIDE_LENGTH


def test_get_possible_values():
    assert msc.get_possible_values() == [_ for _ in range(msc.GRID_SIDE_LENGTH)]


def test_assert_no_duplicates_present():
    assert msc.assert_no_duplicates_present(['1', '2', '3', '5', '6']) == True
    assert msc.assert_no_duplicates_present([]) is True
    assert msc.assert_no_duplicates_present([2, 3, 4, 0, 1, 1]) == False



def test_no_duplicates_in_grid_rows():
    test_grid_false = [[1, 2, 3, 4, 5], [1, 1, 3, 2, 4]]
    test_grid_true = [[1, 4, 5, 2, 3], [4, 3, 2, 0, 1], [4, 2, 3, 1, 9]]
    test_grid_empty = [[], [], []]
    assert msc.no_duplicates_in_grid_rows(test_grid_false) == False
    assert msc.no_duplicates_in_grid_rows(test_grid_true) == True
    assert msc.no_duplicates_in_grid_rows(test_grid_empty) == True


def test_convert_columns_to_rows():
    grid_columns = [[1, 2, 3, None], [1, 2, 3, 4], [1, 2, 3, 4]]
    grid_rows = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [None, 4, 4]]
    assert msc.convert_grid_columns_to_rows(grid_columns) == grid_rows
    

def test_no_duplicates_in_grid_columns():
    grid_no_col_duplicates = [
        [1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, None]
    ]
    grid_with_col_duplicates = [
        [1, 2, 3, 4], [1, 3, 4, 1], [7, 4, 1, 2], [4, None]
    ]
    assert msc.no_duplicates_in_grid_columns(grid_no_col_duplicates) is True
    assert msc.no_duplicates_in_grid_columns(grid_with_col_duplicates) is False


def test_none_not_present():
    grid_contains_none = [[1, 2, 3, 4], [3, 4, 1, 2], [4, None]]
    grid_without_none = [[1, 2, 3, 4], [3, 4, 2], [4, 1, 2, 4]]
    assert msc.none_not_present(grid_contains_none) == False
    assert msc.none_not_present(grid_without_none) == True


def test_build_random_row():
    assert len(msc.build_random_row()) == len(set(msc.build_random_row()))
    assert len(msc.build_random_row()) == len(msc.get_possible_values())


def test_build_grid():
    print('Working')
    test_grid = msc.build_grid()
    assert msc.no_duplicates_in_grid_rows(test_grid) is True
    assert msc.no_duplicates_in_grid_columns(test_grid) is True
    assert msc.none_not_present(test_grid) is True