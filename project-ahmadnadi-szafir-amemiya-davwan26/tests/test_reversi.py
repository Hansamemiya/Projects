"""
Tests for the reversi implementation
"""
import pytest
from typing import List,Tuple,Optional,Set

BoardGridType = List[List[Optional[int]]]

from reversi import Reversi

def create_helper(size: int, num_players: int, othello_bool: bool, moves: \
                  Optional[List[Tuple[int, int]]]) -> Reversi: 
    """
    Creates a board and optionaly applies moves to it.

    Inputs:
    size [int]: the size of the board
    num_players [int]: the number of players in that game
    othello_bool [bool]: weather the game follows the othello cofigeration 
    (True) or not
    moves Optional[List[Tuple[int, int]]]: The possible list of moves you want
    to apply.

    Returns a reversi object that meets all of the inputed specifications. 
    
    """
    reversi = Reversi(side = size, players = num_players,\
                      othello = othello_bool)

    grid = reversi.grid

    assert len(grid) == size
    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1
    if moves:
        move_applier(reversi, moves)

    return reversi

def test_create_1():
    """
    Test whether we can correctly create a (non-Othello) 8x8 game
    """
    grid = create_helper(8, 2, False, None).grid

    for r, row in enumerate(grid):
        assert len(row) == 8
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"

def test_create_2():
    """
    Test whether we can correctly create a (non-Othello) 16x16 game
    """
    grid = create_helper(16, 2, False, None).grid

    for r, row in enumerate(grid):
        assert len(row) == 16
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"

def test_create_othello_1():
    """
    Test whether we can correctly create an 10x10 Othello game
    """
    grid = create_helper(10, 2, True, None).grid

    othello_pos = [(4, 4, 2), (4, 5, 1), (5, 4, 1), (5, 5, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 10
        for c, value in enumerate(row):
            if r in (4, 5) and c in (4, 5):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"

    for r, c, player in othello_pos:
        assert (
            grid[r][c] == player
        ), f"Expected grid[{r}][{c}] to be {player} but got {grid[r][c]}"

def test_create_othello_2():
    """
    Test whether we can correctly create a 20x20 Othello game
    """
    grid = create_helper(20, 2, True, None).grid

    othello_pos = [(9, 9, 2), (9, 10, 1), (10, 9, 1), (10, 10, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 20
        for c, value in enumerate(row):
            if r in (9, 10) and c in (9, 10):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"

    for r, c, player in othello_pos:
        assert (
            grid[r][c] == player
        ), f"Expected grid[{r}][{c}] to be {player} but got {grid[r][c]}"

def test_parity():
    """
    Test that parity checking works
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)

def test_size_othello_8x8():
    """
    Test the size of a 8x8 othello game
    """
    reversi = Reversi(side=8, players=2, othello=True)

    grid = reversi.grid

    assert len(grid) == 8

    for _ , row in enumerate(grid):
        assert len(row) == 8

def test_size_othello_6x6():
    """
    Test the size of a 6x6 othello game
    """
    reversi = Reversi(side=6, players=2, othello=True)

    grid = reversi.grid

    assert len(grid) == 6

    for _ , row in enumerate(grid):
        assert len(row) == 6

def test_size_othello_20x20():
    """
    Test the size of a 20x20 othello game
    """
    reversi = Reversi(side=20, players=2, othello=True)

    grid = reversi.grid

    assert len(grid) == 20

    for _ , row in enumerate(grid):
        assert len(row) == 20

def test_num_players_othello_8x8_1():
    """
    Test that in a 8x8 othello game the number of players are 2
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert reversi.num_players == 2

def test_num_players_othello_8x8_2():
    """
    Test that in a 8x8 othello game the number of players are not 3 when they 
    are 2
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert not reversi.num_players == 3

def test_num_players_othello_6x6():
    """
    Test that in a 2 player 6x6 othello game the number of players are 2
    """
    reversi = Reversi(side=6, players=2, othello=True)
    assert reversi.num_players == 2

def test_num_players_othello_20x20():
    """
    Test that in a 20x20 othello game the number of players are 2
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assert reversi.num_players == 2

def test_turn_othello_8x8_1():
    """
    Test that in a 8x8 othello game the number of players the defult turn is 
    for player 1.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert reversi.turn == 1

def test_turn_othello_8x8_2():
    """
    Test that in a 8x8 othello game the number of players the defult turn is 
    not 2.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert not reversi.turn == 2

def test_turn_othello_6x6():
    """
    Test that in a 6x6 othello game the number of players the defult turn is 
    for player 1.
    """
    reversi = Reversi(side=6, players=2, othello=True)
    assert reversi.turn == 1

def test_turn_othello_20x20():
    """
    Test that in a 20x20 othello game the number of players the defult turn is 
    for player 1.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assert reversi.turn == 1

def check_piece_board(reversi: Reversi, piece_pos: List[Tuple[int,int,int]]):
    """
    Checks the grid to make sure that the places that are supposed to have a
    pice have one and the ones without a piece have None as a value.

    Inputs:
    reversi Reversi: the reversi game object
    piece_pos List[Tuple[int,int]]: the positions that are expected to have a 
    piece

    Return nothing
    """
    grid = reversi.grid
    locs = []
    for r,c,p in piece_pos:
        assert grid[r][c] == p
        locs.append((r,c))

    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            piece = reversi.piece_at((r, c))
            if (r, c) not in locs:
                assert piece is None, f"Expected grid[{r}][{c}] to be None but \
                    got {grid[r][c]}"
                
def check_legal_moves(reversi: Reversi, legal_moves: List[Tuple[int,int]]):
    """
    Checks the grid to make sure that all the legal moves are viewed as legal.

    Inputs:
    reversi Reversi: the reversi game object
    legal_moves List[Tuple[int,int]]: the legal moves

    Return nothing
    """
    grid = reversi.grid
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if (r, c) in legal_moves:
                assert reversi.legal_move((r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"

def test_piece_at_8x8_1():
    """
    Test that piece at returns the correct piece or non if there is no piece for
    the original 8x8 othello config.
    """
    reversi = Reversi(side=8, players=2, othello=True)

    othello_pos = [(3, 3, 2), (3, 4, 1), (4, 3, 1), (4, 4, 2)]

    check_piece_board(reversi, othello_pos)

def test_piece_at_8x8_2():
    """
    Test that piece at returns a exception if a piece off the board is given
    """
    reversi = Reversi(side=8, players=2, othello=True)

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.piece_at((-1, -1))

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.piece_at((9, 9))

def test_piece_at_6x6():
    """
    Test that piece at returns the correct piece or none if there is no piece 
    for the original 6x6 othello config.
    """
    reversi = Reversi(side=6, players=2, othello=True)

    othello_pos = [(2, 2, 2), (2, 3, 1), (3, 2, 1), (3, 3, 2)]

    check_piece_board(reversi, othello_pos)

def test_piece_at_20x20():
    """
    Test that piece at returns the correct piece or none if there is no piece 
    for the original 20x20 othello config.
    """
    reversi = Reversi(side=20, players=2, othello=True)

    othello_pos = [(9, 9, 2), (9, 10, 1), (10, 9, 1), (10, 10, 2)]

    check_piece_board(reversi, othello_pos)
                
def test_legal_moves_1():
    """
    Test that 2,3 is a legal move in an 8x8 Othello game with no moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert reversi.legal_move((2,3)) , f"{(2,3)} is a legal move, but \
        legal_move returned False"

def test_legal_moves_2():
    """
    Test that location (1,2) is not legal move in an 8x8 Othello game with no
    moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert not reversi.legal_move((1,2)), f"{(1,2)} is not a legal move, but \
        legal_move returned True"

def test_legal_moves_3():
    """
    Test all the legal moves in a 8x8 othello board
    """
    reversi = Reversi(side=8, players=2, othello=True)

    legal = {
        (2, 3),
        (4, 5),
        (3, 2),
        (5, 4),
    }

    check_legal_moves(reversi, legal)

def test_legal_moves_6x6():
    """
    Test all the legal initial moves in a 6x6 othello board
    """
    reversi = Reversi(side=6, players=2, othello=True)

    legal = {
        (1, 2),
        (3, 4),
        (4, 3),
        (2, 1),
    }

    check_legal_moves(reversi, legal)

def test_legal_moves_20x20():
    """
    Test all the legal initial moves in a 20x20 othello board
    """
    reversi = Reversi(side=20, players=2, othello=True)

    legal = {
        (8, 9),
        (9, 8),
        (10, 11),
        (11, 10),
    }

    check_legal_moves(reversi, legal)

def test_legal_moves_8x8_non_othello():
    """
    Test all the legal initial moves in a 8x8 non othello board
    """
    reversi = Reversi(side=8, players=2, othello=False)

    legal = {
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4),
    }

    check_legal_moves(reversi, legal)

def test_legal_moves_8x8_non_othello_center_filled():
    """
    Test all the legal moves in a 8x8 non othello board that has the 
    center filled
    """
    
    reversi = create_helper(8, 2, False, None)
    
    legal = {
        (2, 3),
        (4, 5),
        (3, 2),
        (5, 4),
    }

    grid = [[None] * reversi.size for _ in range(reversi.size)]
    grid[3][4] = 1
    grid[3][3] = 2
    grid[4][3] = 1
    grid[4][4] = 2

    reversi.load_game(1, grid)

    check_legal_moves(reversi, legal) 

def test_legal_moves_9x9_non_othello_3_player():
    """
    Test all the legal initial moves in a 9x9 non othello board with 3 players
    """
    reversi = Reversi(side=9, players=3, othello=False)

    legal = {
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4),
        (5, 5)
    }

    check_legal_moves(reversi, legal)

def test_legal_moves_9x9_non_othello_center_filled():
    """
    Test all the legal moves in a 9x9 non othello board that has the 
    center filled with 3 players
    """
    reversi = create_helper(9, 3, False, None)
    grid = [[None] * reversi.size for _ in range(reversi.size)]
    grid[3][3] = 1
    grid[3][4] = 2
    grid[3][5] = 3
    grid[4][3] = 1
    grid[4][4] = 2
    grid[4][5] = 3
    grid[5][3] = 1
    grid[5][4] = 2
    grid[5][5] = 3

    reversi.load_game(1, grid)
    
    legal = {
        (2, 5),
        (2, 6),
        (3, 6),
        (4, 6),
        (5, 6),
        (6, 6),
        (6, 5)
    }

    check_legal_moves(reversi, legal)

def test_legal_move_4():
    """
    Test that calling legal_move with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.legal_move((-1, -1))

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.legal_move((8, 9))

def test_legal_move_5():
    """
    Test that calling legal_move with an invalid position
    raises a ValueError exception 20x20 grid.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=20, players=2, othello=True)
        reversi.legal_move((-20, -20))

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.legal_move((20, 20))

def has_duplicates(moves: List[Tuple[int,int]]) -> bool:
    """
    Makes sure that the list of the moves does not have duplicates

    Inputs:
        moves [List[Tuple[int,int]]]: the list of moves that you want to apply

    Returns[bool]:  True it has duplicates False otherwise 
    """
    return len(set(moves)) != len(moves)

def test_available_moves_8x8():
    """
    Test that available_moves returns correct values
    in an 8x8 Othello game with no moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=True)
    expected = {
        (2, 3),
        (4, 5),
        (3, 2),
        (5, 4),
    }

    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"

def test_available_moves_6x6():
    """
    Test that available_moves returns correct values
    in an 6x6 Othello game with no moves made yet
    """
    reversi = Reversi(side=6, players=2, othello=True)
    expected = {
        (1, 2),
        (3, 4),
        (4, 3),
        (2, 1),
    }

    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"

def test_available_moves_20x20():
    """
    Test that available_moves returns correct values
    in an 20x20 Othello game with no moves made yet
    """
    reversi = Reversi(side=20, players=2, othello=True)
    expected = {
        (8, 9),
        (9, 8),
        (10, 11),
        (11, 10),
    }

    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"

def test_available_moves_8x8_non_othello():
    """
    Test that available_moves returns correct values
    in an 8x8 non Othello game with no moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=False)
    expected = {
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4),
    }
    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"

def test_availible_moves_8x8_non_othello_center_filled():
    """
    Test all the avalible moves in a 8x8 non othello board that has the 
    center filled
    """
    reversi = create_helper(8, 2, False, None)

    grid = [[None] * reversi.size for _ in range(reversi.size)]
    grid[3][4] = 1
    grid[3][3] = 2
    grid[4][3] = 1
    grid[4][4] = 2

    reversi.load_game(1, grid)
    
    expected = {
        (2, 3),
        (4, 5),
        (3, 2),
        (5, 4),
    }
    
    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"   
    
def test_available_moves_9x9_non_othello():
    """
    Test that available_moves returns correct values
    in an 9x9 non Othello game with no moves made yet with 3 players
    """
    reversi = Reversi(side=9, players=3, othello=False)
    expected = {
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4),
        (5, 5)
    }
    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"

def test_availible_moves_9x9_non_othello_center_filled():
    """
    Test all the avalible moves in a 9x9 non othello board that has the 
    center filled 3 player
    """
    reversi = create_helper(9, 3, False, None)

    grid = [[None] * reversi.size for _ in range(reversi.size)]
    grid[3][4] = 1
    grid[3][3] = 2
    grid[4][3] = 1
    grid[4][4] = 2

    reversi.load_game(1, grid)
    
    expected = {
        (3, 5),
        (4, 5),
        (5, 5),
        (5, 4),
        (5, 3)
    }
    
    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"
    
def test_available_moves_3_player():
    """
    Additional 3 player test for avalible moves in the reversi setting.
    Makes sure that you cannot take pices while still filling the center.
    The loaded grid is the equivilant of applying these moves
    (3, 4), (3,3), (3, 5), (4, 4), (4, 5), (4, 3), (5, 4), (5, 3), (5, 5), 
    Then (4, 2)
    """
    reversi = create_helper(9, 3, False, None)

    grid = [[None] * reversi.size for _ in range(reversi.size)]
    
    grid[3][3] = 2
    grid[3][4] = 1
    grid[3][5] = 3
    grid[4][3] = 3
    grid[4][4] = 1
    grid[4][5] = 2
    grid[5][3] = 2
    grid[5][4] = 1
    grid[5][5] = 3

    reversi.load_game(1, grid)

    reversi.apply_move((4, 2))

    expected = {
        (2, 3), 
        (2, 5), 
        (2, 6), 
        (3, 1), 
        (3, 6), 
        (4, 1), 
        (5, 1), 
        (5, 6), 
        (6, 3), 
        (6, 5), 
        (6, 6)
    }
    
    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"

def test_available_moves_7_player():
    """
    Additional 7 player test for avalible moves in the reversi setting.
    """
    reversi = create_helper(9, 7, False, None)

    grid=[[None, None, None, None, None, None, None, None, None],
        [None, 1, 2, 3, 4, 5, 6, 7, None],
        [None, 1, 2, 3, 4, 5, 6, 7, None],
        [None, 1, 2, 3, 4, 5, 6, 7, None],
        [None, 1, 2, 3, 4, 5, 6, 7, None],
        [None, 1, 2, 3, 4, 5, 6, 7, None],
        [None, 1, 2, 3, 4, 5, 6, 7, None],
        [None, 1, 2, 3, 4, 5, 6, None, None],
        [None, None, None, None, None, None, None, None, None]]

    reversi.load_game(7, grid)

    reversi.apply_move((7, 7))

    expected = {
        (0, 3),
        (0, 4), 
        (0, 5), 
        (0, 6), 
        (0, 7), 
        (0, 8), 
        (1, 8), 
        (2, 8), 
        (3, 8), 
        (4, 8), 
        (5, 8),
        (6, 8),
        (7, 8),
        (8, 8),
        (8, 3),
        (8, 4), 
        (8, 5), 
        (8, 6), 
        (8, 7),
    }
    
    assert set(reversi.available_moves) == expected
    assert not has_duplicates(reversi.available_moves), "Make sure you don't \
        include duplicate moves!"
 
def move_applier(reversi: Reversi, moves: List[Tuple[int,int]]):
    """
        Applies a list of moves.

        Inputs:
            reversi: the reversi game object
            moves: List[Tuple[int,int]]: the list of moves that you want to 
            apply
        Returns nothing
    
    """
    for move in moves:
        reversi.apply_move(move)

def test_apply_move_1():
    """
    Test making one move. This test is directly testing the apply move method.
    
    """

    reversi = Reversi(side=8, players=2, othello=True)
    reversi.apply_move((2, 3))

    assert reversi.legal_move((4, 2))
    assert reversi.legal_move((2, 2))
    assert reversi.legal_move((2, 4))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((2, 3)) == 1
    assert reversi.piece_at((3, 3)) == 1
    assert reversi.piece_at((4, 3)) == 1
    assert reversi.piece_at((4, 4)) == 2
    assert reversi.piece_at((3, 4)) == 1
    assert reversi.turn == 2
    assert not reversi.done
    assert reversi.outcome == []

def test_apply_move_2():
    """
    Test making multiple moves but not till the end of the game.
    This test is directly testing the apply move method.
    """

    reversi = Reversi(side=8, players=2, othello=True)
    move_applier(reversi, [(2, 3),(4, 2),(5, 3),(2, 4)])
    assert not reversi.legal_move((2, 2))
    assert reversi.legal_move((2, 5))
    assert not reversi.legal_move((4, 2))
    assert not reversi.legal_move((0, 0))
    assert reversi.legal_move((2, 5))
    assert reversi.legal_move((4, 5))
    assert reversi.legal_move((3, 5))
    assert reversi.legal_move((4, 1))

    assert reversi.piece_at((3, 3)) == 2
    assert reversi.piece_at((4, 3)) == 1
    assert reversi.piece_at((2, 5)) == None
    assert reversi.piece_at((3, 5)) == None
    assert reversi.piece_at((4, 5)) == None
    assert reversi.piece_at((3, 4)) == 2
    assert reversi.piece_at((4, 3)) == 1

    assert reversi.turn == 1
    assert not reversi.done
    assert reversi.outcome == []

def test_apply_move_3():
    """
    Test applying a move to an invalid position raises a ValueError exception.
    This test is directly testing the apply move method. 
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.apply_move((-1, -1))

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.apply_move((9, 8))

def test_apply_move_till_end_tie():
    """
    Test making moves till the end of the game.
    This test is directly testing the apply move method.
    """
    reversi = Reversi(side=4, players=2, othello=True)
    move_applier(reversi, [(0, 1),(2, 0),(3, 1),(0, 2),(0, 3),(1, 3),(2, 3),\
                           (3, 3),(1, 0),(0, 0),(3, 2),(3,0)])

    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((3, 0)) == 2
    assert reversi.piece_at((0, 0)) == 2
    assert reversi.piece_at((1, 0)) == 2
    assert reversi.piece_at((1, 2)) == 1
    assert reversi.piece_at((0, 2)) == 1

    assert reversi.done
    assert reversi.outcome == [1,2]

def test_apply_move_till_end_win_4x4():
    """
    Test making moves till the end of the game othello version.
    This test is directly testing the apply move method.
    """
    reversi = Reversi(side=4, players=2, othello=True)
    move_applier(reversi, [(3, 2),(3, 3),(2, 3),(3, 1),(3, 0),(0, 2),(0, 3),\
                           (1, 3),(0, 1),(1, 0),(2, 0),(0,0)])

    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((3, 0)) == 1
    assert reversi.piece_at((0, 0)) == 2
    assert reversi.piece_at((1, 0)) == 2
    assert reversi.piece_at((1, 2)) == 2
    assert reversi.piece_at((0, 2)) == 1

    assert reversi.done
    assert reversi.outcome == [2]

def test_apply_move_till_end_win_5x5():
    """
    Test making moves till the end of the game in a 5x5 non othello 3 player
    game. Also makes sure you cannot take center pieces until you fill the 
    center.
    This test is directly testing the apply move method.
    """
    reversi = Reversi(side=5, players=3, othello=False)
    move_applier(reversi, [(1, 1),(1, 2),(1, 3),(2, 3),(2, 2),(2, 1),(3, 1),\
                           (3, 2),(3, 3),(4, 4),(1, 4),(4, 1),(0, 2),\
                            (1, 0),(3, 4),(0, 0),(0, 1),(0, 3),(0, 4),(2, 4),\
                            (2, 0),(4, 0),(3, 0),(4, 2),(4,3)])

    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((3, 0)) == 3
    assert reversi.piece_at((0, 0)) == 1
    assert reversi.piece_at((1, 0)) == 1
    assert reversi.piece_at((1, 2)) == 1
    assert reversi.piece_at((0, 2)) == 1
    assert reversi.piece_at((2, 1)) == 2

    assert reversi.done
    assert reversi.outcome == [1]

def test_load_game_8x8_othello():
    """
    Test whether we loaded a othello 8x8 game correctly.
    """
    reversi = create_helper(8, 2, True, [(2,3)])
    grid = [[None] * reversi.size for _ in range(reversi.size)]
    grid[3][2] = 1
    grid[3][3] = 1
    grid[3][4] = 1
    grid[4][3] = 1
    grid[4][4] = 2

    reversi.load_game(2, grid)

    assert not reversi.legal_move((3, 4))
    assert reversi.legal_move((2, 4))

    assert reversi.piece_at((2, 3)) == None
    assert reversi.piece_at((3, 2)) == 1
    assert reversi.piece_at((0, 0)) == None
    assert reversi.piece_at((4, 4)) == 2
    assert reversi.piece_at((3, 3)) == 1

    assert not reversi.done
    assert reversi.turn == 2
    assert reversi.outcome == []

def test_load_game_turn_consistency():
    """ 
    Raise a value error if the value of turn is inconsistent
        with the _players attribute.
    """
    with pytest.raises(ValueError):
        reversi = create_helper(8, 2, True, [(2,3)])
        grid = [[None] * reversi.size for _ in range(reversi.size)]
        grid[3][2] = 1
        grid[3][3] = 1
        grid[3][4] = 1
        grid[4][3] = 1
        grid[4][4] = 2

        reversi.load_game(3, grid)

def test_load_game_size_error():
    """
    Raise a value error if the size of the grid is inconsistent
        with the _side attribute.
    """
    with pytest.raises(ValueError):
        reversi = create_helper(8, 2, True, [(2,3)])
        grid = [[None] * reversi.size for _ in range(reversi.size+1)]
        grid[3][2] = 1
        grid[3][3] = 1
        grid[3][4] = 1
        grid[4][3] = 1
        grid[4][4] = 2

        reversi.load_game(2, grid)

def test_load_game_grid_error():
    """
    Raise a value error if any value in the grid is inconsistent
        with the _players attribute.
    """
    with pytest.raises(ValueError):
        reversi = create_helper(8, 2, True, [(2,3)])
        grid = [[None] * reversi.size for _ in range(reversi.size)]
        grid[3][2] = 1
        grid[3][3] = 3
        grid[3][4] = 3
        grid[4][3] = 1
        grid[4][4] = 2

        reversi.load_game(2, grid)

def test_apply_move_skip():
    """
    Makes sure that a players turn is skipped if they have no moves availible.
    """
    reversi = Reversi(side=5, players=3, othello=False)
    
    grid = [[None] * reversi.size for _ in range(reversi.size)]
    grid[1][1] = 1
    grid[1][2] = 2
    grid[1][3] = 3
    grid[2][1] = 1
    grid[2][2] = 1
    grid[2][3] = 3
    grid[3][1] = 1
    grid[3][2] = 2
    grid[3][3] = 1
    grid[4][4] = 1

    reversi.load_game(2, grid)

    reversi.apply_move((1,4))
    
    assert reversi.turn != 3
    assert reversi.turn == 1

def check_original_game_state(reversi: Reversi, grid_orig: BoardGridType, \
                              legal: Set[Tuple[int,int]], turn: int):
    """
    Check that the original game state has been preserved
    """
    assert reversi.grid == grid_orig
    assert reversi.turn == turn
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

def test_simulate_move_1():
    """
    Test simulating a move that doesn't end the game
    """

    reversi = Reversi(side=8, players=2, othello=True)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(4, 5)])

    orig_legal = {
        (2, 3),
        (4, 5),
        (3, 2),
        (5, 4)
    }

    legal = {
        (5, 3),
        (5, 5),
        (3, 5)
    }

    check_original_game_state(reversi, grid_orig, orig_legal, 1)

    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 2
    assert set(future_reversi.available_moves) == legal
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_simulate_move_2():
    """
    Test simulating a move that results in Player 2 winning
    """

    reversi = Reversi(side=4, players=2, othello=True)
    
    grid=[[2, 2, 2, 2,],
        [2, 2, 2, 2,],
        [2, 2, 2, 2,],
        [None, 1, 2, 2,]]
    
    reversi.load_game(2, grid)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(3, 0)])

    orig_legal ={
        (3,0)
    }

    check_original_game_state(reversi, grid_orig, orig_legal, 2)

    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert future_reversi.outcome == [2]

def test_simulate_move_3():
    """
    Test simulating a move that results in a tie
    """

    reversi = Reversi(side=4, players=2, othello=True)

    grid=[[2, 1, 1, 1,],
        [2, 2, 1, 1,],
        [2, 1, 1, 1,],
        [None, 1, 1, 2,]]
    
    reversi.load_game(2, grid)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(3,0)])

    legal = {
        (3, 0)
    }

    check_original_game_state(reversi, grid_orig, legal, 2)

    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert sorted(future_reversi.outcome) == [1, 2]

def test_simulate_moves_4():
    """
    Test that calling simulate_moves with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(-1, -1)])

    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(8, 8)])

def test_simulate_move_5():
    """
    Test simulating multiple move that doesn't end the game
    """

    reversi = Reversi(side=8, players=2, othello=True)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(4, 5),(3,5)])

    orig_legal = {
        (2, 3),
        (4, 5),
        (3, 2),
        (5, 4)
    }

    legal = {
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6)
    }

    check_original_game_state(reversi, grid_orig, orig_legal, 1)

    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 1
    assert set(future_reversi.available_moves) == legal
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_end_game_8x8_2_players_one_winner():
    """
    Uses load game to test an 8x8 two-player game that ends with a full board,
    and just one player as the winner.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    grid=[[2, 2, 2, 2, 2, 2, 1,None],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [1, 2, 1, 2, 2, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [1, 1, 1, 2, 1, 2, 1, 1,]]

    reversi.load_game(2, grid)
    reversi.apply_move((0,7))
    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.done
    assert reversi.outcome == [2]

def test_end_game_8x8_2_players_tie():
    """
    Uses load game to test an 8x8 two-player game that ends with a full board,
    and with the two players tying.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    grid=[[2, 2, 2, 2, 2, 2, 1,None],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 1, 1,]]

    reversi.load_game(2, grid)
    reversi.apply_move((0,7))
    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((3, 0)) == 2
    assert reversi.piece_at((0, 0)) == 2
    assert reversi.piece_at((6, 6)) == 1

    assert reversi.done
    assert reversi.outcome == [1,2]

def test_end_game_7x7_3_players_one_winner():
    """
    Uses load game to test a 7x7 three-player game that ends with a full board,
    and just one player as the winner.
    """
    reversi = Reversi(side=7, players=3, othello=False)
    grid=[[2, 2, 2, 2, 2, 1,None],
        [2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2,],
        [1, 1, 1, 1, 1, 1, 1,],
        [2, 1, 2, 2, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 3,]]

    reversi.load_game(2, grid)
    reversi.apply_move((0,6))
    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((3, 0)) == 2
    assert reversi.piece_at((0, 0)) == 2
    assert reversi.piece_at((4, 0)) == 1
    assert reversi.piece_at((6, 6)) == 3

    assert reversi.done
    assert reversi.outcome == [2]
    
def test_end_game_7x7_3_players_2_players_tie():
    """
    Uses load game to test a 7x7 three-player game that ends with a full board,
    and two of the players tying (i.e., not a three-way tie)
    """
    reversi = Reversi(side=7, players=3, othello=False)
    grid=[[2, 2, 2, 2, 2, 1,None],
        [2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2,],
        [1, 1, 1, 3, 2, 2, 3,],
        [1, 1, 1, 1, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 1,],
        [1, 1, 1, 1, 1, 1, 3,]]

    reversi.load_game(2, grid)
    reversi.apply_move((0,6))
    assert not reversi.legal_move((2, 2))
    assert not reversi.legal_move((3, 2))
    assert not reversi.legal_move((0, 0))

    assert reversi.piece_at((3, 0)) == 1
    assert reversi.piece_at((0, 0)) == 2
    assert reversi.piece_at((4, 0)) == 1
    assert reversi.piece_at((6, 6)) == 3

    assert reversi.done
    assert reversi.outcome == [1,2]

def test_end_game_8x8_2_players_one_winner_other_no_moves():
    """
    Uses load game to test an 8x8 two-player game where, before the board is
    full, both players end up having no available moves (with one of them
    winning at that point in the game)
    """
    reversi = Reversi(side=8, players=2, othello=False)
    grid=[[2, 2, 2, 2, 2, 2, 2,None],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [2, 2, 2, 2, 2, 2, 2, 2,],
        [1, 1, 1, 2, 1, 1, 2, 2,],
        [1, 1, 2, 1, 1, 1, 2, 2,],
        [1, 2, 1, 1, 1, 1, 2, 2,],
        [2, 1, 1, 1, 1, 1, 2, 2,]]

    reversi.load_game(2, grid)
    assert reversi.done
    assert reversi.outcome == [2]
