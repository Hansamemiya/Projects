"""
Contains the board class that is used in the reversi implementation.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict
from piece import Piece

class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    _rows: int
    _cols: int
    _board: List[List[Optional[Piece]]]
    _location_of_pieces: Dict[int, List[Tuple[int, int]]]

    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._board = [[None] * cols for _ in range(rows)]
        self._location_of_pieces = {}

    @property
    def num_rows(self) -> int:
        """
        Returns the number of rows of the board
        """
        return self._rows

    @property
    def num_cols(self) -> int:
        """
        Returns the number of columns of the board
        """
        return self._cols

    @property
    def locations(self) -> Dict[int, List[Tuple[int, int]]]:
        """
        Returns all of the locations of the pieces
        """
        return self._location_of_pieces

    @property
    def board(self) -> List[List[Optional[Piece]]]:
        """
        Returns the board
        """
        return self._board


    def add_piece(self, player: int, location: Tuple[int, int]) -> bool:
        """
        Add a piece represented by a string to the board.

        Inputs:
            piece (int): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece

        Returns (bool): True if the piece was added successfully,
            False otherwise
        """
        player_locations = self._location_of_pieces.get(player, [])

        row, col = location
        new_piece = Piece(player)

        if self._board[row][col] is None:
            self._board[row][col] = new_piece
            player_locations.append(location)
            self._location_of_pieces[player] = player_locations
            return True
        return False

    @property
    def is_full(self) -> bool:
        """
        Checks if a board is full/has a piece on every spot.

        Returns (bool): True if the board is full/has every spot filled.
            False otherwise. 
        
        """
        for row in range(self._rows):
            for col in range(self._cols):
                if self._board[row][col] is None:
                    return False
        return True


    def num_player_pieces(self, player: int) -> int:
        """
        Returns the number of pieces on a board for a given player.

        Inputs:
            player (str): the identity of the player
        
        Returns: the number of pieces belonging to player on the board (int)
        """
        count = 0
        for row in self._board:
            for piece in row:
                if piece is not None and piece.get_player() == player:
                    count += 1

        return count


    def out_of_bounds(self, pos: Tuple[int, int]) -> bool:
        """
        Returns if a given position is in the bounds of the board

        Input:
            pos (Tuple[int, int]): the location being considered

        Returns: True is position is off the board, False otherwise.
        """
        row, col = pos
        if row < 0 or row >= self._rows:
            return True
        if col < 0 or col >= self._cols:
            return True   
        return False


    def __str__(self) -> str:
        """ Returns string representation of a board"""
        rows = []
        for row in self._board:
            rows.append(str(row))
        return '\n'.join(rows)


    def __repr__(self) -> str:
        """ Returns string representation of a board"""
        return self.__str__()


    def clear_board(self):
        """
        Clears the board of all pieces.

        Returns: None
        """
        self._board = [[None for _ in range(self._cols)] for _ in \
                      range(self._rows)]
        self._location_of_pieces = {}  # Also clear the location of pieces


    def get_piece(self, pos: Tuple[int, int]) -> Optional[Piece]:
        """
        Get method for a piece.
        Returns a piece or None if their is no piece at that position.
        """
        x, y = pos
        return self._board[x][y]


    def set_piece(self, pos: Tuple[int, int], player: int) -> None:
        """
        Sets a piece on the board at a position.
        Returns None
        """
        x, y = pos
        self._board[x][y] = Piece(player)
