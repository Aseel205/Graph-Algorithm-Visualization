#include <stdio.h>
#include <stdlib.h>
#include "data_structures.h"

#define MAX_QUEUE_SIZE 100

// Vector Data Structure

// Function to initialize the vector
void initVector(Vector* v) {
    v->size = 0;
    v->capacity = 2;
    v->data = (int*)malloc(v->capacity * sizeof(int));
}

// Function to add an element to the vector
void pushBack(Vector* v, int value) {
    if (v->size == v->capacity) {
        v->capacity *= 2;
        v->data = (int*)realloc(v->data, v->capacity * sizeof(int));
    }
    v->data[v->size++] = value;
}

// Function to get the element at a particular index
int get(Vector* v, int index) {
    if (index >= 0 && index < v->size) {
        return v->data[index];
    }
    return -1; // Return an invalid value
}

// Function to free the memory allocated for the vector
void freeVector(Vector* v) {
    free(v->data);
}

// Queue Data Structure

// Function to initialize the queue
void initQueue(Queue* q) {
    q->front = 0;
    q->rear = 0;
}

// Function to check if the queue is empty
int isQueueEmpty(Queue* q) {
    return q->front == q->rear;
}

// Function to enqueue (add an element)
void enqueue(Queue* q, int value) {
    if ((q->rear + 1) % MAX_QUEUE_SIZE == q->front) {
        printf("Queue is full\n");
        return;
    }
    q->data[q->rear] = value;
    q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
}

// Function to dequeue (remove an element)
int dequeue(Queue* q) {
    if (isQueueEmpty(q)) {
        printf("Queue is empty\n");
        return -1; // Return an invalid value
    }
    int value = q->data[q->front];
    q->front = (q->front + 1) % MAX_QUEUE_SIZE;
    return value;
}

// Stack Data Structure

// Function to initialize the stack
void initStack(Stack* s) {
    s->top = -1;
}

// Function to check if the stack is empty
int isStackEmpty(Stack* s) {
    return s->top == -1;
}

// Function to push an element onto the stack
void push(Stack* s, int value) {
    if (s->top == MAX - 1) {
        printf("Stack Overflow\n");
        return;
    }
    s->items[++(s->top)] = value;
}

// Function to pop an element from the stack
int pop(Stack* s) {
    if (isStackEmpty(s)) {
        printf("Stack Underflow\n");
        return -1; // Return an invalid value
    }
    return s->items[(s->top)--];
}

// Function to peek the top element of the stack
int peek(Stack* s) {
    if (isStackEmpty(s)) {
        printf("Stack is empty\n");
        return -1; // Return an invalid value
    }
    return s->items[s->top];
}

// Union-Find Data Structure

// Initialize Union-Find
void initUnionFind(UnionFind* uf, int size) {
    uf->size = size;
    uf->parent = (int*)malloc(size * sizeof(int));
    uf->rank = (int*)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        uf->parent[i] = i;
        uf->rank[i] = 0;
    }
}

// Find with path compression
int find(UnionFind* uf, int u) {
    if (uf->parent[u] != u) {
        uf->parent[u] = find(uf, uf->parent[u]);
    }
    return uf->parent[u];
}

// Union by rank
void unionSets(UnionFind* uf, int u, int v) {
    int rootU = find(uf, u);
    int rootV = find(uf, v);
    if (rootU != rootV) {
        if (uf->rank[rootU] > uf->rank[rootV]) {
            uf->parent[rootV] = rootU;
        } else if (uf->rank[rootU] < uf->rank[rootV]) {
            uf->parent[rootU] = rootV;
        } else {
            uf->parent[rootV] = rootU;
            uf->rank[rootU]++;
        }
    }
}
