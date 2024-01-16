# TEXT USER INTERFACE

import sys
from typing import List, Tuple
from reversi import Reversi, ReversiBase
import click
from colored import fg, attr # type: ignore

WALL_CHARS = {
    "H_WALL": "─", "V_WALL": "│", "HV_WALL": "┼",
    "NW_CORNER": "┌", "NE_CORNER": "┐", "SW_CORNER": "└", "SE_CORNER": "┘",
    "VE_WALL": "├", "VW_WALL": "┤", "HS_WALL": "┬", "HN_WALL": "┴",
    "N_WALL": "╵", "E_WALL": "╶", "S_WALL": "╷", "W_WALL": "╴"
}

PLAYER_COLORS = {
    1: fg('red'),
    2: fg('blue'),        
    3: fg('green'),       
    4: fg('cyan'),        
    5: fg('white'),      
    6: fg('tan'),      
    7: fg('yellow'),  
    8: fg('orange_3'),  
    9: fg('magenta'),
}

PLAYER_SYMBOLS = {
    1: "●",                
    2: "■",                
    3: "▲",                
    4: "○",                
    5: "□",                
    6: "◆",                
    7: "★",                
    8: "▼",                
    9: "◊",                
}

EMPTY_CELL_SYMBOL = " "

PIECES = {"EMPTY": " "}

def make_grid(board_size):
    """
    Creates a grid for the board

    Args:
        board_size (int): The size of the board

    Returns:
        List[List[str]]: The grid for the board
    """
    grid = []
    for row in range(2 * board_size + 1):
        grid_row = []
        for col in range(2 * board_size + 1):
            if row == 0 and col == 0:
                grid_row.append(WALL_CHARS["NW_CORNER"])
            elif row == 0 and col == 2 * board_size:
                grid_row.append(WALL_CHARS["NE_CORNER"])
            elif row == 2 * board_size and col == 0:
                grid_row.append(WALL_CHARS["SW_CORNER"])
            elif row == 2 * board_size and col == 2 * board_size:
                grid_row.append(WALL_CHARS["SE_CORNER"])
            elif row == 0 or row == 2 * board_size:
                (grid_row.append(WALL_CHARS["H_WALL"] if col % 2 != 0 
                                 else (WALL_CHARS["HS_WALL"] if row == 0 
                                       else WALL_CHARS["HN_WALL"])))
            elif col == 0 or col == 2 * board_size:
                (grid_row.append(WALL_CHARS["V_WALL"] if row % 2 != 0 
                                 else (WALL_CHARS["VE_WALL"] if col == 0 
                                       else WALL_CHARS["VW_WALL"])))
            elif row % 2 == 0 and col % 2 == 0:
                grid_row.append(WALL_CHARS["HV_WALL"])
            elif row % 2 == 0:
                grid_row.append(WALL_CHARS["H_WALL"])
            elif col % 2 == 0:
                grid_row.append(WALL_CHARS["V_WALL"])
            else:
                grid_row.append(PIECES["EMPTY"])
        grid.append(grid_row)
    return grid

def print_grid(grid):
    """
    Prints the grid

    Args:
        grid (List[List[str]]): The grid to print

    Returns:
        None
    """
    for row in grid:
        print(''.join(row))

@click.command()
@click.option('-n', '--num-players', default=2, help='Number of players')
@click.option('-s', '--board-size', default=8, help='Board size')
@click.option('--othello/--non-othello', 'game_mode', default=True, 
              help='Othello mode')

def main(num_players, board_size, game_mode):
    """
    Main function for the text user interface

    Args:
        num_players (int): The number of players
        board_size (int): The size of the board
        game_mode (bool): Whether to play in Othello mode or not
        
    Returns:
        None
    """
    if num_players % 2 != board_size % 2:
        print("Error: Num of players and board should be both even or odd")
        sys.exit(1)

    stub = Reversi(board_size, num_players, game_mode)

    # use helper function to make the grid
    grid = make_grid(board_size)

    # Add the pieces from the stub object to the grid
    update_grid_with_pieces(grid, stub)

    while not stub.done:
        # Print the final grid
        print_grid(grid)

        # Get and display possible moves for the current player
        possible_moves = get_possible_moves(stub)
        display_pos_moves(possible_moves, stub)

        # Get player move
        move = get_player_move(possible_moves)

        # Apply move
        stub.apply_move(move)

        # Update grid with the new pieces
        update_grid_with_pieces(grid, stub)

    update_grid_with_pieces(grid, stub)
    print_grid(grid)
    
    print("Game over!")
    print_winner(stub)

def update_grid_with_pieces(grid: List[List[str]], stub: ReversiBase):
    """
    Updates the grid with the pieces from the stub object

    Args:
        grid (List[List[str]]): The grid to update
        stub (ReversiBase): The stub object

    Returns:
        None
    """
    for row in range(stub.size):
        for col in range(stub.size):
            piece = stub.piece_at((row, col))
            if piece is not None:
                player_color = PLAYER_COLORS.get(piece, "")
                player_symbol = PLAYER_SYMBOLS.get(piece, "")
                grid[2 * row + 1][2 * col + 1] = (player_color + player_symbol
                                                  + attr('reset'))

def get_possible_moves(stub: ReversiBase) -> List[Tuple[int, int]]:
    """
    Returns a list of possible moves for the current player

    Args:
        stub (ReversiBase): The stub object

    Returns:
        List[Tuple[int, int]]: A list of possible moves for the current player
    """
    return stub.available_moves

def display_pos_moves(possible_moves: List[Tuple[int, int]], stub: ReversiBase):
    """
    Displays the possible moves for the current player

    Args:
        possible_moves (List[Tuple[int, int]]): A list of possible moves for
                                                the current player
        stub (ReversiBase): The stub object

    Returns:
        None
    """
    print("It is Player {}'s turn. Please choose a move:".format(stub.turn))
    for index, move in enumerate(possible_moves, start=1):
        print("{}) {}, {}".format(index, move[0], move[1]))

def get_player_move(possible_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Gets the player's move
    
    Args:
        possible_moves (List[Tuple[int, int]]): A list of possible moves for
                                                the current player

    Returns:
        Tuple[int, int]: The player's move
    """
    move_index = None
    while (move_index is None or move_index < 1 or 
           move_index > len(possible_moves)):
        try:
            move_index = int(input("> "))
            if move_index < 1 or move_index > len(possible_moves):
                raise ValueError("Invalid move index")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return possible_moves[move_index - 1]

def print_winner(stub: ReversiBase):
    """
    Prints the winner of the game

    Args:
        stub (ReversiBase): The stub object

    Returns:
        None
    """
    outcome = stub.outcome
    if len(outcome) == 1:
        print(f"Player {outcome[0]} wins!")
    elif len(outcome) >= 2:
        print("It's a tie!")
    else:
        print("Error determining the winner.")

if __name__ == "__main__":
    main()
