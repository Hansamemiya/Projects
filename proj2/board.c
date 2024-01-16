#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdbool.h>
#include "pos.h"
#include "board.h"


board* board_new(unsigned int width, unsigned int height, enum type type){
    if(type == BITS){
        board* solution = (board*)malloc(sizeof(board));
        solution->width = width;
        solution->height = height;
        solution->type = type;

        unsigned int num_cells = width * height;
        unsigned int num_unsignedints = (num_cells + 16 - 1) / 16;
        solution->u.bits = (unsigned int*)malloc(sizeof(unsigned int) * 
        num_unsignedints);
        for(unsigned int i = 0; i < num_unsignedints; i++){
            solution->u.bits[i] = 0;
        }
        return solution;
    }else{
        board* solution = (board*)malloc(sizeof(board));
        solution->width = width;
        solution->height = height;
        solution->type = type;
        solution->u.matrix = (cell**)malloc(sizeof(cell*)*height);
        for(int i = 0; i < height; i++){
            solution->u.matrix[i] = (cell*)malloc(sizeof(cell)*width);
            for(int j = 0; j < width; j++){
                solution->u.matrix[i][j] = EMPTY;
            }
        }
        return solution;
    }
}

void board_free(board* b){
    if(b->type == BITS){
        free(b->u.bits);
    }else{
        for(int i = 0; i < b->height; i++){
            free(b->u.matrix[i]);
        }
        free(b->u.matrix);
        free(b);
    }
}

void board_show(board* b){
    if(b->type == BITS){
        printf(" ");
        for(int n = 0; n < b->width; n++){
            if(n < 10){
                printf("%d", n);
            }else if (n < 36){
                printf("%c", 'A' + (n - 10));
            }else if (n < 62){
                printf("%c", 'a' + (n - 36));
            }else{
                printf("?");
            }
        }
        printf("\n");

        for(int i = 0; i < b->height; i++){
            if(i < 10){
                printf("%d", i);
            }else if (i < 36){
                printf("%c", 'A' + (i - 10));
            }else if (i < 62){
                printf("%c", 'a' + (i - 36));
            }else{
                printf("?");
            }

            for(int j = 0; j < b->width; j++){
                unsigned int bit_index = (i * b->width + j) * 2;
                unsigned int uint_index = bit_index / 32;
                unsigned int remain = bit_index % 32;
                unsigned int cell = (b->u.bits[uint_index] >> remain) & 0x3;
                if(cell == 0x0){
                    printf(".");
                }else if(cell == 0x1){
                    printf("*");
                }else if(cell == 0x2){
                    printf("o");    
                }
            }
            printf("\n");
        }
    }
    else{
        for(int i = 0; i < b->height; i++){
            if(i == 0){
                for(int n = 0; n < b->width + 1; n++){
                    if(n == 0){
                        printf(" ");
                    }else{
                        if(n <= 10){
                            printf("%d", n - 1);
                        }else if (n > 10 && n <= 36){
                            printf("%c", 'A' + (n - 11));
                        }else if (n > 36 && n <= 62){
                            printf("%c", 'a' + (n - 37));
                        }else{
                            printf("?");
                        }
                    }
                }
                printf("\n");
            }

            for(int z = 0; z < b->width + 1; z++){
                if(z == 0){
                    if(i < 10){
                        printf("%d", i);
                    }else if (i >= 10 && i < 36){
                        printf("%c", 'A' + (i - 10));
                    } else if (i >= 36 && i < 62){
                        printf("%c", 'a' + (i - 36));
                    }else{
                        printf("?");
                    }
                }else{
                    if(b->u.matrix[i][z - 1] == EMPTY){
                    printf(".");
                    }else if(b->u.matrix[i][z - 1] == BLACK){
                        printf("*");
                    }else if (b->u.matrix[i][z - 1] == WHITE){
                    printf("o");
                }
                }
            }
            printf("\n");
        }
    }
}

cell board_get(board* b, pos p){
    if(b->type == BITS){
        unsigned int bit_index = (p.r * b->width + p.c) * 2;
        unsigned int uint_index = bit_index / 32;
        unsigned int remain = bit_index % 32;
        unsigned int cell_bits = (b->u.bits[uint_index] >> remain) & 0x3;
        if(cell_bits == 0x0){
            return EMPTY;
        }else if(cell_bits == 0x1){
            return BLACK;
        }else if(cell_bits == 0x2){
            return WHITE;
        }else{
            fprintf(stderr, "Invalid cell bits");
            return EMPTY;
        }
    }
    else{
        return b->u.matrix[p.r][p.c];
    }
}

void board_set(board* b, pos p, cell c){
    if(b->type == BITS){
        if(p.r > b->height && p.c > b->width){
            fprintf(stderr, "Position out of bounds");
            return;
        }
        unsigned int bit_index = (p.r * b->width + p.c) * 2;
        unsigned int uint_index = bit_index / 32;
        unsigned int remain = bit_index % 32;
        unsigned int value = 0;
        if(c == EMPTY){
            value = 0;
        }else if(c == BLACK){
            value = 1;
        }else if(c == WHITE){
            value = 2;
        }else{
            fprintf(stderr, "Invalid cell value");
            return;
        }
        b->u.bits[uint_index] &= ~(0x3 << remain);
        b->u.bits[uint_index] |= (value << remain);
    }
    else{
        if(p.r > b->height && p.c > b->width){
            fprintf(stderr, "Position out of bounds");
            return;
        }
        b->u.matrix[p.r][p.c] = c;
    }
}
