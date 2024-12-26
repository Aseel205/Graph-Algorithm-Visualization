#ifndef DATA_STRUCTURES_H
#define DATA_STRUCTURES_H

#define MAX_QUEUE_SIZE 100
#define MAX 100
#define MAX_NODES 100

// Vector Data Structure
typedef struct {
    int* data;
    int size;
    int capacity;
} Vector;

// Queue Data Structure
typedef struct {
    int data[MAX_QUEUE_SIZE];
    int front;
    int rear;
} Queue;

// Stack Data Structure
typedef struct {
    int items[MAX];
    int top;
} Stack;

// Union-Find Data Structure
typedef struct {
    int* parent;
    int* rank;
    int size;
} UnionFind;


// Graph Data Structure
typedef struct Graph {
    int V;  // Number of vertices
    int adj[MAX_NODES][MAX_NODES];  // Adjacency matrix
    int weights[MAX_NODES][MAX_NODES];  // Edge weights
} Graph;

// Vector functions
void initVector(Vector* v);
void pushBack(Vector* v, int value);
int get(Vector* v, int index);
void freeVector(Vector* v);

// Queue functions
void initQueue(Queue* q);
int isQueueEmpty(Queue* q);
void enqueue(Queue* q, int value);
int dequeue(Queue* q);

// Stack functions
void initStack(Stack* s);
int isStackEmpty(Stack* s);
void push(Stack* s, int value);
int pop(Stack* s);
int peek(Stack* s);

// Union-Find functions
void initUnionFind(UnionFind* uf, int size);
int find(UnionFind* uf, int u);
void unionSets(UnionFind* uf, int u, int v);

#endif // DATA_STRUCTURES_H
