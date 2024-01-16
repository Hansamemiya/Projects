#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pos.h"

pos make_pos(unsigned int r, unsigned int c){
    pos p;
    p.r = r;
    p.c = c;
    return p;
}

posqueue* posqueue_new(){
    posqueue* new = (posqueue*)malloc(sizeof(posqueue));
    new->head = NULL;
    new->tail = NULL;
    new->len = 0;
    return new;
}

void pos_enqueue(posqueue* q, pos p){
    pq_entry* entry_p = (pq_entry*)malloc(sizeof(pq_entry));
    entry_p->p = p;
    entry_p->next = NULL;
    if(q->len == 0){
        q->head = entry_p;
        q->tail = entry_p;
    }else{
        q->tail->next = entry_p;
        q->tail = entry_p;
    }
    q->len++;
}

pos pos_dequeue(posqueue* q){
    if(q->len == 0){
        fprintf(stderr, "ERROR: pos_dequeue() called on empty queue\n");
        return make_pos(0, 0); //THIS IS THE NULL CASE IF EMPTY QUEUE
    }

    pq_entry* pos_free = q->head;
    pos pos_return = q->head->p;

    q->head = q->head->next;
    free(pos_free);
    q->len--;

    if(q->len == 0){
        q->tail = NULL;
    }

    return pos_return;
}

void posqueue_free(posqueue* q){
    while(q->len > 0){
        pos_dequeue(q);
    }
    free(q);
}


