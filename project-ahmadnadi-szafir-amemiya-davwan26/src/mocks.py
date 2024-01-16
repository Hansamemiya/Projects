"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType


class ReversiStub(ReversiBase):
    """
    Stub implementation of ReversiBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.
    - The board is always initialized with four pieces in the four corners
      of the board. Player 1 has pieces in the northeast and southwest
      corners of the board, and Player 2 has pieces in the southeast and
      northwest corners of the board.
    - All moves are legal, even if there is already a piece in a given position.
    - The game ends after four moves. Whatever player has a piece in position
      (0,1) wins. If there is no piece in that position, the game ends in a tie.
    - It does not validate board positions. If a method
      is called with a position outside the board, the method will likely cause
      an exception.
    - It does not implement the ``load_game`` or ``simulate_moves`` method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The stub implementation "
                             "only supports two players")

        super().__init__(side, players, othello)

        self._grid = [[None]*side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return self._num_moves == 4

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [0, 1]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        raise NotImplementedError()

class ReversiMock(ReversiBase):
    """
    Implementation of ReversiMock.
    """

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The mock implementation "
                             "only supports two players")
        
        if side < 4:
            raise ValueError("This mock implementation" 
                             "only supports 4x4 or above boards")
        
        if side % 2 != players % 2:
            #Checks for parity, if not even raise exception
            raise ValueError("Parity does not match")
        
        super().__init__(side, players, othello)
        self._grid: BoardGridType = [[None] * side for _ in range(side)] 

        if othello:
            self._grid[side//2][side//2] = 2
            self._grid[side//2 - 1][side//2 - 1] = 2
            self._grid[side//2][side//2 - 1] = 1
            self._grid[side//2 - 1][side//2] = 1
        
        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)
    
    @property
    def turn(self) -> int:
        return self._turn
    
    @property
    def available_moves(self) -> ListMovesType:
        moves = set()  # Use a set to avoid duplicate moves
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), \
        (1, -1), (-1, -1)]
        for row in range(self._side):
            for col in range(self._side):
                if self._grid[row][col] is None:
                    for row_change, col_change in directions:
                        new_row, new_col = row + row_change, col + col_change
                        if 0 <= new_row < self._side and 0 <= new_col < \
                        self._side:  # Check if the position is inside the board
                            if self.legal_move((new_row, new_col)):
                                moves.add((new_row, new_col))
        return list(moves)  # Convert the set back to a list before returning

    
    @property
    def done(self) -> bool:
        if ((self._grid[0][0] is not None) or  # if a piece is on (0,0)
            (self._grid[self._side - 1][self._side - 1] is not None)): 
            # If a piece is on (side-1, side-1)
            return True
        
        return False  

        
    @property
    def outcome(self) -> List[int]:
        if not self.done:  # If the game is not done
            return []
        elif self._grid[0][0] is not None:  # if there is a piece at (0,0)
            return [self._grid[0][0]]
        elif self._grid[self._side - 1][self._side - 1] is not None: 
            # if there is a piece at (side-1, side-1)
            return [1, 2]

        return []

        
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        coord_x, coord_y = pos
        # position outside the board
        if coord_x >= self._side or coord_y >= self._side:
            raise ValueError("the specified position is outside the bounds of \
            the board.")
        # position already taken
        elif self._grid[coord_x][coord_y] != None:
            return self.grid[coord_x][coord_y]
        else:
            return None
        
    def legal_move(self, pos: Tuple[int, int]) -> bool:
    ### In the method for adding moves, or for checking if a move is legal,
     # Check if game is done. If True, keep the program from adding the move
        row, col = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), \
                      (1, -1), (-1, -1)]
        
        # If the position is outside the board, return False
        if row < 0 or row >= self._side or col < 0 or col >= self._side:
            return False
        
        elif self._grid[row][col] is None:
            for row_change, col_change in directions:
                new_row = row + row_change
                new_col = col + col_change
                if (new_row >= 0 and new_row < self._side and new_col >= 0 and 
                    new_col < self._side):
                    if self._grid[new_row][new_col] is not None:
                        return True
        if row == 0 and col == 0:
            return True
        if row == self._side-1 and col == self._side-1:
            return True
        
        return False
    
    def apply_move(self, pos: Tuple[int, int]) -> None:
        coord_x, coord_y = pos
        
        if coord_x >= self._side or coord_y >= self._side or coord_x < 0 or \
        coord_y < 0:    
            raise ValueError("The specified position is outside the bounds of\
             the board.")
            
        self._grid[coord_x][coord_y] = self._turn
        self._turn = self._turn % self._players + 1
        if self.available_moves == []:
            self._turn = self._turn % self._players + 1

            
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError # Does not need to implement anything
    
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        
        simulation = ReversiMock(self._side, self._players, self._othello)
        for move in moves:
            if not self.legal_move(move):
                raise ValueError("The move is not legal.")
            simulation.apply_move(move)

        return simulation
    

class ReversiBotMock(ReversiMock):
    def __init__(self, side: int, players: int, othello: bool):
        super().__init__(side, players, othello)
    
    @property
    def done(self) -> bool:
        """
        Returns if the every space in the board is occupied.
        """
        for row in self._grid:
            for piece in row:
                if piece is None:
                    return False
        
        return True
    

    @property
    def outcome(self) -> List[int]:
        """
        Returns the outcome of a reversi game in the bot mock. A player wins
        the game if their pieces outnumber the pieces of their opponent. A list
        with the winners' number (i.e. turn) is outputted.

        Returns: list of winners (returns both players if game is drawn)
        """
        if not self.done:
            return []
        
        p1_count = 0
        p2_count = 0
        for row in self._grid:
            for piece in row:
                if piece == 1:
                    p1_count += 1
                if piece == 2:
                    p2_count += 1
        
        if p1_count > p2_count:
            return [1]
        elif p1_count < p2_count:
            return [2]
        else:
            return [1,2]
    
    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the set of legal moves from a given position.
        """
        moves = []
        for row in range(self._side):
            for col in range(self._side):
                if self.legal_move((row, col)):
                    moves.append((row, col))
        return moves  
    

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Returns if it is legal for the current player to place a piece at a 
        given position, represented by a Tuple of integers. 

        Inputs:
            pos (Tuple[int, int]): position of piece being considered, as 
                (row, col)
        
        Output: True if move is legal, False if else
        """    
        row, col = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), \
                      (1, -1), (-1, -1)]
        # If the position is outside the board, return False
        if row < 0 or row >= self._side or col < 0 or col >= self._side:
            return False
        
        if self._grid[row][col] is None:
            if 0 <= self._num_moves < 4:
                # In the first 4 moves, it is legal to go in the center squares
                if (row == self._side // 2 or row == self._side // 2 - 1) and\
                    (col == self._side // 2 or col == self._side // 2 - 1):
                    return True
                
            # If position borders an existing piece, move is legal
            for row_change, col_change in directions:
                new_row = row + row_change
                new_col = col + col_change
                if (new_row >= 0 and new_row < self._side and new_col >= 0 and 
                    new_col < self._side):
                    if self._grid[new_row][new_col] is not None:
                        return True
        
        return False
    
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Places a piece on the board at pos and updates turn and number of moves
        accordingly. Also turns the value of any opponents' pieces neighboring
        pos to the value of the current player.

        Inputs:
            pos (Tuple[int, int]): the position of the move being inputted
        """
        coord_x, coord_y = pos
        x_dir = (-1, 0, 1)
        y_dir = (-1, 0, 1)

        if coord_x >= self._side or coord_y >= self._side or coord_x < 0 or \
        coord_y < 0:    
            raise ValueError("The specified position is outside the bounds of \
            the board.")
        
        # Place the player's piece at pos
        self._grid[coord_x][coord_y] = self._turn

        # Check for neighbors in each direction, and change them to players'
        for dx in x_dir:
            for dy in y_dir:
                if 0 <= coord_x + dx < self._side and \
                0 <= coord_y + dy < self._side and \
                self.piece_at((coord_x + dx, coord_y + dy)) is not None and\
                self.piece_at((coord_x + dx, coord_y + dy)) != self._turn:
                    self._grid[coord_x + dx][coord_y + dy] = self._turn

        # Change turn to next player with available moves
        old_turn = self._turn
        self._turn = self.turn % self._players + 1
        while self.available_moves == []:
            self._turn = self.turn % self._players + 1
            if self._turn == old_turn:
                break

        # Update the number of moves
        self._num_moves += 1


    def simulate_moves(self, moves: ListMovesType) -> "ReversiBotMock":
        """
        Creates a new ReversiBotMock object which simulates the effect of
        playing a list of moves.

        Input:
            moves (ListMovesType): list of moves to be inputted into the 
                simulation

        Output: ReversiBotMock object with the moves inputted
        """
        # Create new ReversiBotMock object
        simulation = ReversiBotMock(self._side, self._players, self._othello)

        # Copy self's information over to simulation
        simulation._grid = [row.copy() for row in self._grid]
        simulation._turn = self._turn
        simulation._num_moves = self._num_moves

        # Simulate each move
        for move in moves:
            if not self.legal_move(move):
                raise ValueError("The move is not legal.")
            simulation.apply_move(move)

        return simulation
