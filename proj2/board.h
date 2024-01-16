#ifndef BOARD_H
#define BOARD_H

#include "pos.h"


enum cell {
    EMPTY,
    BLACK,
    WHITE
};

typedef enum cell cell;


union board_rep {
    enum cell** matrix;
    unsigned int* bits;
};

typedef union board_rep board_rep;

enum type {
    MATRIX, BITS
};


struct board {
    unsigned int width, height;
    enum type type;
    board_rep u;
};

typedef struct board board;

/*
Creates a new board with the specified width and height. The type of the board 
(matrix or bits) is determined by the 'type' parameter. The board is initially 
empty.

Parameters:
- width: The width of the board.
- height: The height of the board.
- type: The type of the board. This should be either MATRIX or BITS.

Returns:
- A pointer to the newly created board.
*/
board* board_new(unsigned int width, unsigned int height, enum type type);

/*
Frees the memory associated with the board.
*/
void board_free(board* b);

/*
Prints the current state of the board to stdout. Each cell is represented by its 
current state (either BLACK, WHITE, or EMPTY).

Parameters:
- b: A pointer to the board

Returns:
- None. This function does not return a value.
*/
void board_show(board* b);

/*
Retrieves the cell at the specified position on the board.

Parameters:
- b: A pointer to the board from which the cell should be retrieved.
- p: The position of the cell to be retrieved.

Returns:
- The cell at the specified position.
*/
cell board_get(board* b, pos p);

/*
Sets the cell at the specified position on the board to the specified state.

Parameters:
- b: A pointer to the board on which the cell should be set.
- p: The position of the cell to be set.
- c: The new state for the cell. This should be either BLACK, WHITE, or EMPTY.

*/
void board_set(board* b, pos p, cell c);

#endif /* BOARD_H */
