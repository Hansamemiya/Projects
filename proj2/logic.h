#ifndef LOGIC_H
#define LOGIC_H

#include <stdbool.h>
#include "board.h"


enum turn {
    BLACKS_TURN,
    WHITES_TURN
};

typedef enum turn turn;


enum outcome {
    IN_PROGRESS,
    BLACK_WIN,
    WHITE_WIN,
    DRAW
};

typedef enum outcome outcome;


enum rotation {
    NO_ROTATION,
    CLOCKWISE,
    COUNTERCLOCKWISE
};

typedef enum rotation rotation;


struct game {
    unsigned int run;
    board* b;
    posqueue *black_queue, *white_queue;
    turn player;
    rotation last_rotation;
};

typedef struct game game;

/*
Creates a new game. The 'run' parameter configures the length of a run 
needed to win. The function does not allow impossible games (i.e., games where 
run length is greater than the width or height). 

Parameters:
- run: The length of a run needed to win.
- width: The width of the game board.
- height: The height of the game board.
- type: The type of data representation to use for the game board.

Returns:
- A pointer to the newly created game.
*/
game* new_game(unsigned int run, unsigned int width,
               unsigned int height, enum type type);

/*
Frees the memory allocated for the game, including the game board and the 
position queues for both players.

Parameters:
- g: A pointer to the game that should be freed.
*/
void game_free(game* g);

/*
Places the current player's piece at the specified position if the spot is
unoccupied. Returns true for a successful placement; false for an illegal move.

This function also handles turn progression, updates the queue, and records no 
rotation for the turn. If an illegal move is detected, the player retains their 
turn for a retry.

Parameters:
- g: A pointer to the game where the piece should be placed.
- p: The position where the piece should be placed.

Returns:
- True if the piece was successfully placed; false if the move was illegal.
*/
bool place_piece(game* g, pos p);

/*
Rotates the game board 90 degrees in the specified direction. The direction of 
rotation is determined by the 'clockwise' parameter. If 'clockwise' is true, the 
board is rotated clockwise; if 'clockwise' is false, the board is rotated 
counterclockwise. 

Parameters:
- g: A pointer to the game whose board should be rotated.
- clockwise: A boolean indicating the direction of rotation. True for clockwise 
  rotation, false for counterclockwise rotation.

Returns:
- True if the rotation was successful; false if the rotation was not allowed 
  according to the game rules.
*/
bool rotate(game* g, bool clockwise);

/*
Uplift the oldest piece of the specified color, then advance the turn and record 
that the just-completed move was not a rotation.

Parameters:
- g: A pointer to the game where the piece should be uplifted.
- c: The color of the piece to be uplifted.

Returns:
- True if the uplift was successful; false if the specified color's queue is 
  empty.
*/
bool uplift(game* g, cell c);

/*
Determines the outcome of the game. This function checks the current state of
game.

Parameters:
- g: A pointer to the game whose outcome should be determined.

Returns:
- The outcome of the game.
*/
outcome game_outcome(game* g);

#endif /* LOGIC_H */
