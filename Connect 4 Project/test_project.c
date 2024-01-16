#include <criterion/criterion.h>
#include "pos.h"
#include "board.h"
#include "logic.h"
#include <math.h>

//make_pos
Test(pos, make_pos){
    pos p = make_pos(1, 2);
    cr_assert_eq(p.r, 1);
    cr_assert_eq(p.c, 2);
}

//posqueue_new
Test(posqueue, posqueue_new){
    posqueue* q = posqueue_new();
    cr_assert_eq(q->len, 0);
    cr_assert_eq(q->head, NULL);
    cr_assert_eq(q->tail, NULL);
}

//pos_enqueue
Test(posqueue, pos_enqueue){
    posqueue* q = posqueue_new();
    pos p = make_pos(1, 2);
    pos_enqueue(q, p);
    cr_assert_eq(q->len, 1);
    cr_assert_eq(q->head->p.r, 1);
    cr_assert_eq(q->head->p.c, 2);
    cr_assert_eq(q->tail->p.r, 1);
    cr_assert_eq(q->tail->p.c, 2);
    cr_assert_eq(q->head->next, NULL);
    cr_assert_eq(q->tail->next, NULL);
    pos p2 = make_pos(3, 4);
    pos_enqueue(q, p2);
    cr_assert_eq(q->len, 2);
    cr_assert_eq(q->head->p.r, 1);
    cr_assert_eq(q->head->p.c, 2);
    cr_assert_eq(q->tail->p.r, 3);
    cr_assert_eq(q->tail->p.c, 4);
    cr_assert_eq(q->head->next->p.r, 3);
    cr_assert_eq(q->head->next->p.c, 4);
    cr_assert_eq(q->head->next->next, NULL);
    cr_assert_eq(q->tail->next, NULL);
}

//pos_dequeue
Test(posqueue, pos_dequeue){
    posqueue* q = posqueue_new();
    pos p = make_pos(1, 2);
    pos_enqueue(q, p);
    pos p2 = make_pos(3, 4);
    pos_enqueue(q, p2);
    pos p3 = pos_dequeue(q);
    cr_assert_eq(p3.r, 1);
    cr_assert_eq(p3.c, 2);
    cr_assert_eq(q->len, 1);
    cr_assert_eq(q->head->p.r, 3);
    cr_assert_eq(q->head->p.c, 4);
    cr_assert_eq(q->tail->p.r, 3);
    cr_assert_eq(q->tail->p.c, 4);
    cr_assert_eq(q->head->next, NULL);
    cr_assert_eq(q->tail->next, NULL);
    pos p4 = pos_dequeue(q);
    cr_assert_eq(p4.r, 3);
    cr_assert_eq(p4.c, 4);
    cr_assert_eq(q->len, 0);
    cr_assert_eq(q->head, NULL);
    cr_assert_eq(q->tail, NULL);
}


//board_new
Test(board, board_new){
    board* b = board_new(3, 3, MATRIX);
    cr_assert_eq(b->width, 3);
    cr_assert_eq(b->height, 3);
    cr_assert_eq(b->type, MATRIX);
    cr_assert_eq(b->u.matrix[0][0], EMPTY);
    cr_assert_eq(b->u.matrix[0][1], EMPTY);
    cr_assert_eq(b->u.matrix[0][2], EMPTY);
    cr_assert_eq(b->u.matrix[1][0], EMPTY);
    cr_assert_eq(b->u.matrix[1][1], EMPTY);
    cr_assert_eq(b->u.matrix[1][2], EMPTY);
    cr_assert_eq(b->u.matrix[2][0], EMPTY);
    cr_assert_eq(b->u.matrix[2][1], EMPTY);
    cr_assert_eq(b->u.matrix[2][2], EMPTY);
    board_free(b);
}

//board_free
Test(board, board_free){
    board* b = board_new(3, 3, MATRIX);
    board_free(b);
}

//board_show

Test(board, board_show_big){
    board* b = board_new(70, 70, BITS);
    board_show(b);
}

Test(board, board_show_small){
    board* b = board_new(3, 3, BITS);
    pos p = make_pos(1, 2);
    pos p2 = make_pos(2, 1);
    pos p3 = make_pos(0, 0);
    board_set(b, p, BLACK);
    board_set(b, p2, BLACK);
    board_set(b, p3, WHITE);
    board_show(b);
}


//board_get
Test(board, board_get){
    board* b = board_new(3, 3, BITS);
    pos p = make_pos(1, 2);
    pos p2 = make_pos(2, 1);
    pos p3 = make_pos(0, 0);
    board_set(b, p2, BLACK);
    board_set(b, p3, WHITE);
    cr_assert_eq(board_get(b, p), EMPTY);
    cr_assert_eq(board_get(b, p2), BLACK);
    cr_assert_eq(board_get(b, p3), WHITE);

    board_free(b);
}

//board_set
Test(board, board_set){
    board* b = board_new(3, 3, BITS);
    pos p = make_pos(1, 2);
    board_set(b, p, BLACK);
    cr_assert_eq(board_get(b, p), BLACK);
    board_free(b);
}


//// LOGIC /////////////////

//new_game
Test(game, new_game) {
    int width = 3;
    int height = 3;
    int win_condition = 3;
    enum type board_type = BITS;

    game* g = new_game(width, height, win_condition, board_type);

    cr_assert_eq(g->run, win_condition);
    cr_assert_eq(g->b->width, width);
    cr_assert_eq(g->b->height, height);
    cr_assert_eq(g->b->type, board_type);

    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
                pos p = {i, j};
                cr_assert_eq(board_get(g->b, p), EMPTY);
        }
    }
    cr_assert_eq(g->black_queue->len, 0);
    cr_assert_eq(g->black_queue->head, NULL);
    cr_assert_eq(g->black_queue->tail, NULL);

    cr_assert_eq(g->white_queue->len, 0);
    cr_assert_eq(g->white_queue->head, NULL);
    cr_assert_eq(g->white_queue->tail, NULL);

    cr_assert_eq(g->player, BLACKS_TURN);
    cr_assert_eq(g->last_rotation, NO_ROTATION);

    // Free memory
    game_free(g);
}

//place_piece
Test(place_piece, valid_move_black_turn) {
    game* g = new_game(3, 3, 3, BITS);
    pos p = {0, 0};

    place_piece(g,p);
    cr_assert(board_get(g->b, p) == BLACK);
    cr_assert_eq(g->player, WHITES_TURN);
    cr_assert_eq(g->last_rotation, NO_ROTATION);

    //board_show(g->b);
    game_free(g);
}

//rotate
//TEST ILLEGAL ROTATION

Test(rotate, test1_clock){
    game* g = new_game(3, 3, 3, BITS);
    pos p1 = {0,0};
    pos p2 = {0,1};
    pos p3 = {1,1};
    place_piece(g, p1);
    place_piece(g, p2);
    place_piece(g, p3);
    board_show(g->b);
    
    rotate(g, true);
    board_show(g->b);
}

Test(rotate, test2_counter){
    game* g = new_game(3, 3, 3, BITS);
    pos p1 = {0,0};
    pos p2 = {0,1};
    pos p3 = {1,1};
    place_piece(g, p1);
    place_piece(g, p2);
    place_piece(g, p3);
    board_show(g->b);
    
    rotate(g, false);
    board_show(g->b);
}


Test(rotate, test2_counter_size){
    game* g = new_game(3, 2, 3, BITS);
    pos p1 = {0,0};
    pos p2 = {0,1};
    pos p3 = {1,1};
    place_piece(g, p1);//black
    place_piece(g, p2);//whitecd
    place_piece(g, p3);//black
    board_show(g->b);
    
    rotate(g, false);//white
    board_show(g->b);
    cr_assert_eq(g->player, BLACKS_TURN);
    cr_assert_eq(g->last_rotation, COUNTERCLOCKWISE);

    //test if queues were updated
    pos dequeuedPos = pos_dequeue(g->black_queue);
    cr_assert_eq(dequeuedPos.r, 1);
    cr_assert_eq(dequeuedPos.c, 0);

    pos dequeuedPos2 = pos_dequeue(g->black_queue);
    cr_assert_eq(dequeuedPos2.r, 0);
    cr_assert_eq(dequeuedPos2.c, 1);

    pos dequeuedPos3 = pos_dequeue(g->white_queue);
    cr_assert_eq(dequeuedPos3.r, 0);
    cr_assert_eq(dequeuedPos3.c, 0);
}

Test(rotate, illegal){
    game* g = new_game(3, 2, 3, BITS);
    rotate(g, false); //BLACK
    cr_assert(!rotate(g, true)); //WHITE
    cr_assert(g->player == WHITES_TURN);
}



Test(uplift, easy){
    game* g = new_game(3, 3, 3, BITS);
    pos p1 = {2,2};
    pos p2 = {0, 0};
    place_piece(g, p1);//black
    place_piece(g, p2);//white

    board_show(g->b);

    uplift(g, BLACK);
    board_show(g->b);
    cr_assert(g->player == WHITES_TURN);

    //test if queues were updated
    pos dequeuedPos = pos_dequeue(g->black_queue);
    cr_assert_eq(dequeuedPos.r, 0);
    cr_assert_eq(dequeuedPos.c, 2);

    pos dequeuedPos3 = pos_dequeue(g->white_queue);
    cr_assert_eq(dequeuedPos3.r, 0);
    cr_assert_eq(dequeuedPos3.c, 0);
    game_free(g);
}

Test(uplift, fail){
    game* g = new_game(3, 3, 3, BITS);
    pos p1 = {2,2};
    place_piece(g, p1);//black

    cr_assert(!uplift(g, WHITE));
}

//No change
Test(uplift, no_change){
    game* g = new_game(3, 3, 3, BITS);
    pos p1 = {0,0};
    place_piece(g, p1);//black
    board_show(g->b);
    cr_assert(uplift(g, BLACK)); //White
    board_show(g->b);
    cr_assert_eq(g->player, BLACKS_TURN);
    game_free(g);
}


//Blocked
Test(uplift, blocked){
    game* g = new_game(3, 3, 3, BITS);
    pos p1 = {1,0};
    pos p2 = {0,0};
    place_piece(g, p1);//black
    place_piece(g, p2);//white

    board_show(g->b);

    cr_assert(uplift(g, BLACK));
    cr_assert_eq(g->player, WHITES_TURN);

    pos dequeuedPos = pos_dequeue(g->black_queue);
    cr_assert_eq(dequeuedPos.r, 1);
    cr_assert_eq(dequeuedPos.c, 0);

    pos dequeuedPos3 = pos_dequeue(g->white_queue);
    cr_assert_eq(dequeuedPos3.r, 0);
    cr_assert_eq(dequeuedPos3.c, 0);

    board_show(g->b);
    game_free(g);
}



//game_outcome
Test(game_outcome, horizontal){
    game* g = new_game(3, 3, 3, BITS);
    pos bp1 = {0,0};
    pos bp2 = {0,1};
    pos bp3 = {0,2};
    pos wp1 = {1,0};
    pos wp2 = {1,1};
    place_piece(g, bp1);
    place_piece(g, wp1);
    place_piece(g, bp2);
    place_piece(g, wp2);
    place_piece(g, bp3);

    board_show(g->b);

    cr_assert_eq(game_outcome(g), BLACK_WIN);
    game_free(g);
}

Test(game_outcome, vertical){
    game* g = new_game(3, 3, 3, BITS);
    pos bp1 = {0,0};
    pos bp2 = {1,0};
    pos bp3 = {2,0};
    pos wp1 = {1,2};
    pos wp2 = {1,1};
    place_piece(g, bp1);
    place_piece(g, wp1);
    place_piece(g, bp2);
    place_piece(g, wp2);
    place_piece(g, bp3);

    board_show(g->b);

    cr_assert_eq(game_outcome(g), BLACK_WIN);
    game_free(g);
}

Test(game_outcome, diagonal){
    game* g = new_game(3, 3, 3, BITS);
    pos bp1 = {0,0};
    pos bp2 = {1,1};
    pos bp3 = {2,2};
    pos wp1 = {1,0};
    pos wp2 = {1,2};
    place_piece(g, bp1);
    place_piece(g, wp1);
    place_piece(g, bp2);
    place_piece(g, wp2);
    place_piece(g, bp3);

    board_show(g->b);

    cr_assert_eq(game_outcome(g), BLACK_WIN);
    game_free(g);
}


Test(game_outcome, nowin){
    game* g = new_game(3, 3, 3, BITS);
    pos bp1 = {0,0};
    pos bp2 = {1,1};
    pos wp1 = {1,0};
    pos wp2 = {1,2};
    place_piece(g, bp1);
    place_piece(g, wp1);
    place_piece(g, bp2);
    place_piece(g, wp2);

    board_show(g->b);

    cr_assert_eq(game_outcome(g), IN_PROGRESS);
    game_free(g);
}

Test(game_outcome, tie){
    game* g = new_game(3, 3, 3, BITS);
    pos bp1 = {0,0};
    pos bp2 = {0,2};
    pos bp3 = {1,1};
    pos bp4 = {2,1};
    pos bp5 = {1,2};
    pos wp1 = {0,1};
    pos wp2 = {1,0};
    pos wp3 = {2,2};
    pos wp4 = {2,0};
    place_piece(g, bp1);
    place_piece(g, wp1);
    place_piece(g, bp2);
    place_piece(g, wp2);
    place_piece(g, bp3);
    place_piece(g, wp3);
    place_piece(g, bp4);
    place_piece(g, wp4);
    place_piece(g, bp5);

    board_show(g->b);

    cr_assert_eq(game_outcome(g), DRAW);
    game_free(g);
}