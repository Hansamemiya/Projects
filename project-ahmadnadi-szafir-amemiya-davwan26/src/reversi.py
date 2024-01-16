"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from board import Board

BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""

class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """
    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError
    
class Reversi(ReversiBase):
    """
    Class for the game of Reversi
    """
    def __init__(self, side, players, othello):
        if players % 2 != side % 2:
            raise ValueError("Parity of players and side must match")
        
        if othello and players != 2:
            raise Exception("Othello is only for 2 players")
        
        super().__init__(side, players, othello)

        self._board = Board(side, side)
        if othello:
            self._board.add_piece(2, (side // 2, side // 2))
            self._board.add_piece(2, (side // 2 - 1, side // 2 - 1))
            self._board.add_piece(1, (side // 2, side // 2 - 1))
            self._board.add_piece(1, (side // 2 - 1, side // 2))

        self._turn = 1
        self._num_moves = 0
        self._side = side

    @property
    def size(self) -> int:
        return self._side

    @property
    def num_players(self) -> int:
        return self._players
    
    @property
    def grid(self) -> BoardGridType:
        grid: BoardGridType = [[None] * self._side for _ in range(self._side)]
        for row in range(self._board.num_rows):
            for col in range(self._board.num_cols):
                if self.piece_at((row, col)) is not None:
                    grid[row][col] = \
                        self.piece_at((row, col))
        return grid

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:      
        moves = set()
        for row in range(self._board.num_rows):
            for col in range(self._board.num_cols):
                if self.piece_at((row, col)) is None and \
                    self.legal_move((row, col)):
                    moves.add((row, col))
        return list(moves)
    
    @property
    def done(self) -> bool:
        """
        Returns: True if the game is over, False otherwise.

        Saves the current player. Then checks all the available moves for each 
        player and if a single player has a move then the game is not done. 
        resets the turn to the current player. If no player has a move then the 
        game is done
        """
        current_player = self._turn 
        for player in range(1, self._players + 1): 
            self._turn = player
            if len(self.available_moves) > 0:
                self._turn = current_player
                return False 
        self._turn = current_player 
        return True 
        
    @property
    def outcome(self) -> List[int]:
        """
        Returns: A list of player numbers, in order of
        their position in the game's outcome. If the game
        is not over, returns an empty list.

        If the game is done, using a dictionary, find the number of pieces each 
        player has on the board. Then find the max number of pieces and return 
        as a list. 
        
        If the game is not over, the outcome is an empty
        list.
        """
        if self.done:
            player_scores = {} 
            for player in range(1, self._players + 1):
                player_scores[player] = self._board.num_player_pieces(player)
            max_score = max(player_scores.values()) 
            winners = [player for player in player_scores \
                       if player_scores[player] == max_score]
            return winners 
        else:
            return [] 

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        row, col = pos
        if row >= self._board.num_rows or col >= self._board.num_cols or \
            row < 0 or col < 0:
            raise ValueError("The specified position is outside the bounds of \
                             the board.")
        piece = self._board.board[row][col]
        return None if piece is None else int(piece.get_player())

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        row, col = pos
        piece = self._turn
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), \
                              (-1, -1), (1, -1),(-1, 1)]
        if row >= self._board.num_rows or col >= self._board.num_cols or \
            row < 0 or col < 0:
            raise ValueError("The specified position is outside the bounds of \
                             the board.")
        if not self._othello and self._num_moves < (self.num_players **2):
            #Players can only put within the middle number of \
            #(players by player square)
            # they can put anywhere
            edge_len = (self._board.num_rows - self.num_players) // 2
            if edge_len <= row < (self._board.num_rows-edge_len):
                if edge_len <= col < (self._board.num_cols-edge_len):
                    if self.piece_at((row,col)) is None:
                        return True
            return False

        else:
            if self.piece_at((row, col)) is None:          
                for row_direc, col_direc in directions:
                    new_row, new_col = row + row_direc, col + col_direc
                    if new_row < self._board.num_rows and new_col < \
                        self._board.num_cols and new_row >= 0 and new_col >= 0:
                        if self.piece_at((new_row, new_col)) is not None and \
                            self.piece_at((new_row, new_col)) != piece:
                            done = False
                            while not done:
                                if new_row >= self._board.num_rows or \
                                    new_col >= self._board.num_cols or \
                                        new_row < 0 or new_col < 0:
                                    done = True
                                elif self.piece_at((new_row, new_col)) is None:
                                    done = True
                                elif self.piece_at((new_row, new_col)) == piece:
                                    return True
                                new_row, new_col = new_row + row_direc, new_col\
                                 + col_direc

            return False

    def flip(self, pos: Tuple[int, int], dir: Tuple[int, int]):
        """
        Beginning at a piece at position pos, proceeds in direction dir and 
        changes any enemy pieces to player's value
        """
        if not self._othello and self._num_moves < (self.num_players **2):
            # dont flip if not othello and at the start
            return
        else:
            x, y = pos
            dx, dy = dir

            cursor = (x + dx, y + dy)
            pieces_to_flip = [] # Pieces in this direction

            ### Check pieces in direction dir until encounter
                # Board edge
                # Own piece
                # Empty square
            while not self._board.out_of_bounds(cursor) and \
            self.piece_at(cursor) is not None and \
            self.piece_at(cursor) != self.piece_at(pos):
                pieces_to_flip.append(self._board.get_piece(cursor))
                cursor = (cursor[0] + dx, cursor[1] + dy)

            # If cursor ends on own piece, flip all encountered pieces
            if not self._board.out_of_bounds(cursor) and\
            self.piece_at(cursor) == self.piece_at(pos):
                for piece in pieces_to_flip:
                    piece.set_player(self.turn)        

    def apply_move(self, pos: Tuple[int, int]) -> None:
        if pos not in self.available_moves:
            raise ValueError("Illegal Move")

        # Insert piece of player
        player = self._turn
        self._board.add_piece(player, pos)

        # Adjust the values of all neighboring enemy pieces
        dirs = [(1,0), (1,1), (0, 1), (-1, 1),\
                (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for dir in dirs:
            self.flip(pos, dir)
        
        # Adjust values of turn and num_moves
        self._num_moves += 1

        old_turn = self._turn
        self._turn = self.turn % self._players + 1
        while not self.available_moves:
            self._turn = self.turn % self._players + 1
            if self._turn == old_turn:
                break

        # If applying the move ends the game, update game.done and 
        # outcome accordingly

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        count = 0
        if turn < 1 or turn > self._players:
            raise ValueError("The value of turn is inconsistent with the \
                             _players attribute.")
        
        size = len(grid)
        if size != self._side:
            raise ValueError("The size of the grid is inconsistent with the \
                             _side attribute.")
        
        for row in grid:
            if len(row) != size:
                raise ValueError("The size of the grid is inconsistent with the\
                                  _side attribute.")
            for cell in row:
                if cell is not None and (cell < 1 or cell > self._players):
                    raise ValueError("A value in the grid is inconsistent with\
                                     the _players attribute.")
        
        self._turn = turn

        self._board.clear_board() 
        # Clear the board before loading the new game state

        for row_idx in range(size):
            for col_idx in range(size):
                if grid[row_idx][col_idx] is not None:
                    count += 1
                    self._board.add_piece(grid[row_idx][col_idx], \
                                          (row_idx, col_idx))
        
        self._num_moves = count
        old_turn = self._turn

        while not self.available_moves:
            self._turn = self.turn % self._players + 1
            if self._turn == old_turn:
                break

    def simulate_moves(self, moves: ListMovesType) -> "Reversi":
        simulation = Reversi(self._side, self._players, self._othello)
        simulation.load_game(self.turn, self.grid) 
        # Load the current state into the simulation

        for move in moves:
            if not simulation.legal_move(move): 
                # Check if the move is legal in the simulation
                raise ValueError("The move is not legal.")
            simulation.apply_move(move)

        return simulation

    def num_pieces(self, player: int):
        """
        Return the number of pieces of a given player on the board
        """
        return self._board.num_player_pieces(player)
