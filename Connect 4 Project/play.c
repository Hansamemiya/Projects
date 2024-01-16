#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "pos.h"
#include "logic.h"
#include "board.h"

int main(int argc, char *argv[]) {

    if (argc != 8) {
        printf("Error: Invalid number of arguments. Expected 8 \n");
        return 1;
    }
    unsigned int height = 0;
    unsigned int width = 0;
    unsigned int run_length = 0;
    enum type representation = MATRIX;

    bool flag = false; 
    for (int i = 0; i < argc; i++) {
        if (strlen(argv[i]) > 2 && argv[i][0] == '-') {
            printf("Invalid argument format for %s. Expected space \n", 
            argv[i]);
            return 1;
        }
        if (strcmp(argv[i], "-h") == 0) {
            if (i + 1 < argc) {
                height = atoi(argv[i + 1]);

            } else {
                printf("Missing value for -h\n");
                return 1;
            }
        } else if (strcmp(argv[i], "-w") == 0) {
            if (i + 1 < argc) {
                width = atoi(argv[i + 1]);
            } else {
                printf("Missing value for -w\n");
                return 1;
            }
        } else if (strcmp(argv[i], "-r") == 0) {
            if (i + 1 < argc) {
                run_length = atoi(argv[i + 1]);
            } else {
                printf("Missing value for -r\n");
                return 1;
            }
        } else if (strcmp(argv[i], "-m") == 0) {
            representation = MATRIX;
            flag = true;

        } else if (strcmp(argv[i], "-b") == 0) {
            representation = BITS;
            flag = true;
        }
    }
    if(!flag){
        fprintf(stderr, "Did not provide representation \n");
        return 1;
    
    }
    game *g = new_game(run_length, width, height, representation);
    g->run = run_length;
    g->b = board_new(width, height, MATRIX);
    g->black_queue = posqueue_new();
    g->white_queue = posqueue_new();
    g->player = BLACKS_TURN;
    g->last_rotation = NO_ROTATION;

    outcome o = IN_PROGRESS;
   
    while (o == IN_PROGRESS) {
        board_show(g->b);
        if(g->player == BLACKS_TURN){
            printf("BLACK:");
        }else{
            printf("WHITE:");
        }
        char input[3];
        if (scanf("%2s", input) != 1 || strlen(input) != 2) {
            printf("Invalid input. Please enter two characters.\n");
        } else {
            char x = input[0];
            char y = input[1];

            if (x == '!') {
                switch (y) {
                case '<':
                    rotate(g,false);
                    break;

                case '>':
                    rotate(g, true);
                    break;

                case 'B':
                    uplift(g, BLACK);
                    break;

                case 'W':
                    uplift(g, WHITE);
                    break;

                default:
                    printf("Invalid special move.\n");
                }
            } else {
                int row, col;

                if (x >= 'A' && x <= 'Z') {
                    row = x - 'A' + 10;
                } else {
                    row = x - '0';
                }

                if (y >= 'A' && y <= 'Z') {
                    col = y - 'A' + 10;
                } else {
                    col = y - '0';
                }

                if (row >= 0 && col >= 0 && row < g->b->height && 
                col < g->b->width) {
                    pos new_pos = make_pos((unsigned int)row, 
                    (unsigned int)col);
                    place_piece(g, new_pos);
                } else{
                    printf("Invalid position.\n");
                }
            }
        }
        o = game_outcome(g);
        printf("\n");
    }
    board_show(g->b);
    if(o == BLACK_WIN){
        printf("BLACK WINS!\n");
    }else if(o == WHITE_WIN){
        printf("WHITE WINS!\n");
    }else{
        printf("DRAW!\n");
    }
    game_free(g);

    return 0;
}
