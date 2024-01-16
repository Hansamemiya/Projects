#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#include "logic.h"

game* new_game(unsigned int run, unsigned int width, unsigned int height, 
enum type type){
    if(run > width && run > height){
        fprintf(stderr, "ERROR: run is greater than width and height. Impossible Game\n");
        return NULL;
    }
    game* new = (game*)malloc(sizeof(game));
    new->run = run;
    new->b = board_new(width, height, type);
    new->black_queue = posqueue_new();
    new->white_queue = posqueue_new();
    new->player = BLACKS_TURN;
    new->last_rotation = NO_ROTATION;

    return new;
}

void game_free(game* g){
    board_free(g->b);
    posqueue_free(g->black_queue);
    posqueue_free(g->white_queue);
    free(g);
}

bool place_piece(game* g, pos p){
    if (board_get(g->b, p) != EMPTY){
        fprintf(stderr, "ERROR: position is not empty\n");
        return false;
    }else{
        if(g->player == WHITES_TURN){
            board_set(g->b, p, WHITE);
            pos_enqueue(g->white_queue, p);
            g->player = BLACKS_TURN;
        }else{
            board_set(g->b, p, BLACK);
            pos_enqueue(g->black_queue, p);
            g->player = WHITES_TURN;
        }
        g->last_rotation = NO_ROTATION;
        return true;
    }
}

#include <pthread.h>

typedef struct thread_data RotateThreadData; 
struct thread_data{
    game* g;
    board* n_board;
    bool clockwise;
    unsigned int row;
};

/*
    The function iterates over each cell in the specified row. For each cell, it
    calculates the new position of the cell after rotation. 
    The function then retrieves the value of the cell from the old board and 
    sets the cell at the new position on the new board to this value.

    Parameters:
    - arg: A void poninter to RotateThreadData struct 

    Returns:
    - NULL
 */
void* rotate_row(void* arg) {
    RotateThreadData* data = (RotateThreadData*)arg;
    unsigned int r = data->row;
    unsigned int width = data->g->b->width;
    unsigned int height = data->g->b->height;

    for (unsigned int c = 0; c < width; c++) {
        pos o_pos = make_pos(r, c);
        pos n_pos;
        if (data->clockwise) {
            n_pos = make_pos(c, height - 1 - r);
        } else{
            n_pos = make_pos(width - 1 - c, r);
        }
        cell value = board_get(data->g->b, o_pos);
        board_set(data->n_board, n_pos, value);
    }
    return NULL;
}

bool rotate(game* g, bool clockwise) {
    if ((clockwise && g->last_rotation == COUNTERCLOCKWISE) || 
        (!clockwise && g->last_rotation == CLOCKWISE)) {
        fprintf(stderr, "ERROR: cannot reverse rotation in the next move\n");
        return false;
    }
    board* n_board = board_new(g->b->height, g->b->width, MATRIX);
    if (g->b->type == MATRIX) {
        unsigned int g_height = g->b->height;
        pthread_t threads[g_height];
        RotateThreadData data[g_height];

        for (unsigned int i = 0; i < g_height; i++) {
            data[i] = (RotateThreadData){g, n_board, clockwise, i};
            pthread_create(&threads[i], NULL, rotate_row, &data[i]);
        }

        for (unsigned int i = 0; i < g->b->height; i++) {
            pthread_join(threads[i], NULL);
        }

    } else{
        unsigned int g_width = g->b->width;
        unsigned int g_height = g->b->height;
        for (unsigned int row = 0; row < g_height; row++) {
            for (unsigned int col = 0; col < g_width; col++) {
                pos old_pos = make_pos(row, col);
                pos n_pos;
                if (clockwise) {
                    n_pos = make_pos(col, g_height - 1 - row);
                } else {
                    n_pos = make_pos(g_width - 1 - col, row);
                }
                cell value = board_get(g->b, old_pos);
                board_set(g->b, n_pos, value);
            }
        }
    }
    board_free(g->b);
    g->b = n_board;

    posqueue* black_queue = g->black_queue;
    posqueue* white_queue = g->white_queue;
    posqueue* new_black_queue = posqueue_new();
    posqueue* new_white_queue = posqueue_new();

    while (black_queue->len > 0) {
        pos p = pos_dequeue(black_queue);
        pos np;
        if (clockwise) {
            np = make_pos(p.c, n_board->width - 1 - p.r);
        } else {
            np = make_pos(n_board->height - 1 - p.c, p.r);
        }
        pos_enqueue(new_black_queue, np);
    }

    while (white_queue->len > 0) {
        pos p = pos_dequeue(white_queue);
        pos np;
        if (clockwise) {
            np = make_pos(p.c, n_board->width - 1 - p.r);
        } else {
            np = make_pos(n_board->height - 1 - p.c, p.r);
        }
        pos_enqueue(new_white_queue, np);
    }

    posqueue_free(black_queue);
    posqueue_free(white_queue);

    g->black_queue = new_black_queue;
    g->white_queue = new_white_queue;

    if (clockwise) {
        g->last_rotation = CLOCKWISE;
    } else {
        g->last_rotation = COUNTERCLOCKWISE;
    }

    if (g->player == BLACKS_TURN) {
        g->player = WHITES_TURN;
    } else {
        g->player = BLACKS_TURN;
    }

    return true;
    }

bool uplift(game* g, cell c){
    //Check if the cell exist
    if((c == BLACK && g->black_queue->len == 0)|| 
    (c == WHITE && g->white_queue->len == 0)){
        fprintf(stderr, "Cannot uplift as no pieces were placed yet \n");
        return false;
    } 

    pos up;
    if(c == BLACK){
        up = pos_dequeue(g->black_queue);
    } else {
        up = pos_dequeue(g->white_queue);
    }

    if(up.r == 0){
        printf("NO change");
        if(c == BLACK){
            pos_enqueue(g->black_queue, up);
        }else{
            pos_enqueue(g->white_queue, up);
        }

    }else{
        pos original = up;
        while (up.r > 0 && board_get(g->b, make_pos(up.r - 1, up.c)) == EMPTY) {
            up.r--;
        }
        board_set(g->b, original, EMPTY);

        board_set(g->b, up, c);

        if(c == BLACK){
            pos_enqueue(g->black_queue, up);
        } else {
            pos_enqueue(g->white_queue, up);
        }
    }

    if(g->player == WHITES_TURN){
        g->player = BLACKS_TURN;
    }else{
        g->player = WHITES_TURN;
    }

    g->last_rotation = NO_ROTATION;

    return true;
}

/*
 * The function check_run checks if there is a winning condition in the game.
 * It takes a board pointer, a position, a cell color, the direction of the row 
 * (dr), the direction of the column (dc), and the length of the run as 
 * parameters.
 * 
 * It iterates over the board in the specified direction (dr, dc) for the length 
 * of the run.
 * If it finds a cell that does not match the specified color, it returns 
 * IN_PROGRESS,indicating the game is still ongoing.
 * 
 * If all cells in the run match the specified color, it checks the color.
 * If the color is BLACK, it returns BLACK_WIN, indicating that the black player 
 * has won.
 * Otherwise, it returns WHITE_WIN, indicating that the white player has won.
 */
outcome check_run(board* b, pos p, cell color, int dr, int dc, int run){
    for(int i = 0; i < run; i++){
        if(board_get(b, make_pos(p.r + i * dr, p.c + i * dc)) != color){
            return IN_PROGRESS;
        }
    }
    if(color == BLACK){
        return BLACK_WIN;
    }else{
        return WHITE_WIN;
    }
}

outcome game_outcome(game* g){
    int run = g->run;
    for(int r = 0; r < g->b->height; r++){
        for(int c = 0; c < g->b->width; c++){
            pos p = {r, c};
            cell color = board_get(g->b, p);
            if(color == EMPTY){
                continue;
            }
            if(color != EMPTY){
                //horizontal Directions
                if(c + run <= g->b->width){
                    outcome check = check_run(g->b, p, color, 0, 1, run);
                    if(check != IN_PROGRESS){
                        return check;
                    }
                }
                
                //vertical Directions
                if(r + run <= g->b->height){
                    outcome check = check_run(g->b, p, color, 1, 0, run);
                    if(check != IN_PROGRESS){
                        return check;
                    }
                }

                //diagonal Direction
                if(c + run <= g->b->width && r + run <= g->b->height){
                    outcome check = check_run(g->b, p, color, 1, 1, run);
                    if(check != IN_PROGRESS){
                        return check;
                    }
                }

                if(c + run <= g->b->width && r - run + 1 >= 0){
                    outcome check = check_run(g->b, p, color, -1, 1, run);
                    if(check!= IN_PROGRESS){
                        return check;
                    }
                }
            }
        }
    }
    //if there are no empty spaces and no winner, then it is a draw
    for(int r = 0; r < g->b->height; r++){
        for(int c = 0; c < g->b->width; c++){
            pos p = {r, c};
            if(board_get(g->b, p) == EMPTY){
                return IN_PROGRESS;
            }
        }
    }
    return DRAW;
}
