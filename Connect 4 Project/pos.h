#ifndef POS_H
#define POS_H

struct pos {
    unsigned int r, c;
};

typedef struct pos pos;


typedef struct pq_entry pq_entry;

struct pq_entry {
    pos p;
    pq_entry* next;
};


struct posqueue {
    pq_entry *head, *tail;
    unsigned int len;
};

typedef struct posqueue posqueue;

/*
Creates a new position with the specified row and column values.

Parameters:
- r: The row value for the new position.
- c: The column value for the new position.

Returns:
- A new position with the specified row and column values.
*/
pos make_pos(unsigned int r, unsigned int c);

/*
Creates a new position queue and returns a pointer to it. The queue is 
initially empty.

Parameters:
- None.

Returns:
- A pointer to the newly created position queue.
*/
posqueue* posqueue_new();

/*
Adds a new position to the end of the queue.

Parameters:
- q: A pointer to the queue where the position should be added.
- p: The position to be added to the queue.

*/
void pos_enqueue(posqueue* q, pos p);

/*
Removes and returns the position at the front of the queue. 
If the queue is empty, an error is raised.

Parameters:
- q: A pointer to the queue from which the position should be removed and 
returned.

Returns:
- The position at the front of the queue.
*/
pos pos_dequeue(posqueue* q);

/*
Frees the memory allocated for the position queue. 

Parameters:
- q: A pointer to the queue that should be freed.
*/
void posqueue_free(posqueue* q);

#endif /* POS_H */
