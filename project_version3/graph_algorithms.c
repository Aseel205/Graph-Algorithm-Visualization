#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>
#include "data_structures.h"
#include <stdio.h>

#define MAX_NODES 100




// BFS Algorithm
void bfs(Graph* graph, int start) {
    int visited[MAX_NODES] = {0};
    Queue q;
    initQueue(&q);
    visited[start] = 1;
    enqueue(&q, start);

    printf("BFS Traversal: ");
    while (!isQueueEmpty(&q)) {
        int u = dequeue(&q);
        printf("%d \n", u);

        for (int v = 0; v < graph->V; v++) {
            if (graph->adj[u][v] == 1 && !visited[v]) {
                visited[v] = 1;
                enqueue(&q, v);
            }
        }
    }
    printf("\n");
}

// DFS Algorithm
void dfsUtil(Graph* graph, int u, int* visited) {
    visited[u] = 1;
    printf("%d \n", u);

    for (int v = 0; v < graph->V; v++) {
        if (graph->adj[u][v] == 1 && !visited[v]) {
            dfsUtil(graph, v, visited);
        }
    }
}

void dfs(Graph* graph, int start) {
    int visited[MAX_NODES] = {0};
    printf("DFS Traversal: ");
    dfsUtil(graph, start, visited);
    printf("\n");
}

// Dijkstra's Algorithm to find the shortest path from a source node
void dijkstra(Graph* graph, int start) {
    int dist[MAX_NODES];
    bool visited[MAX_NODES] = {false};

    for (int i = 0; i < graph->V; i++) {
        dist[i] = INT_MAX;
    }
    dist[start] = 0;

    for (int i = 0; i < graph->V - 1; i++) {
        int u = -1;
        for (int j = 0; j < graph->V; j++) {
            if (!visited[j] && (u == -1 || dist[j] < dist[u])) {
                u = j;
            }
        }

        visited[u] = true;

        for (int v = 0; v < graph->V; v++) {
            if (graph->adj[u][v] == 1 && !visited[v] && dist[u] != INT_MAX && dist[u] + graph->weights[u][v] < dist[v]) {
                dist[v] = dist[u] + graph->weights[u][v];
            }
        }
    }

    printf("Dijkstra's Shortest Path\n");
    printf ("from node %d:\n", start );
    for (int i = 0; i < graph->V; i++) {
        if (dist[i] == INT_MAX) {
            printf("Node %d is unreachable\n", i);
        } else {
            printf("Distance to node %d: %d\n", i, dist[i]);
        }
    }
}
// Prim's Algorithm for Minimum Spanning Tree
void prim(Graph* graph) {
    printf("prim will start" )   ; 
    int parent[MAX_NODES];
    int key[MAX_NODES];
    bool mstSet[MAX_NODES];

    for (int i = 0; i < graph->V; i++) {
        key[i] = INT_MAX;
        mstSet[i] = false;
    }

    key[0] = 0;  // Start from node 0
    parent[0] = -1;  // No parent for the first node

    for (int count = 0; count < graph->V - 1; count++) {
        int u = -1;
        for (int v = 0; v < graph->V; v++) {
            if (!mstSet[v] && (u == -1 || key[v] < key[u])) {
                u = v;
            }
        }

        mstSet[u] = true;

        for (int v = 0; v < graph->V; v++) {
            if (graph->adj[u][v] == 1 && !mstSet[v] && graph->weights[u][v] < key[v]) {
                parent[v] = u;
                key[v] = graph->weights[u][v];
            }
        }
    }

    printf("Prim's Minimum\nSpanning Tree:\n");
    for (int i = 1; i < graph->V; i++) {
        printf("Edge: %d - %d, Weight: %d\n", parent[i], i, graph->weights[i][parent[i]]);
    }
}

// Bellman-Ford Algorithm for Shortest Path with Negative Weights
void bellman_ford(Graph* graph, int start) {
    int dist[MAX_NODES];
    for (int i = 0; i < graph->V; i++) {
        dist[i] = INT_MAX;
    }
    dist[start] = 0;

    // Relax edges repeatedly
    for (int i = 1; i < graph->V; i++) {
        for (int u = 0; u < graph->V; u++) {
            for (int v = 0; v < graph->V; v++) {
                if (graph->adj[u][v] == 1 && dist[u] != INT_MAX && dist[u] + graph->weights[u][v] < dist[v]) {
                    dist[v] = dist[u] + graph->weights[u][v];
                }
            }
        }
    }

    // Check for negative weight cycles
    for (int u = 0; u < graph->V; u++) {
        for (int v = 0; v < graph->V; v++) {
            if (graph->adj[u][v] == 1 && dist[u] != INT_MAX && dist[u] + graph->weights[u][v] < dist[v]) {
                printf("Graph contains a negative weight cycle\n");
                return;
            }
        }
    }

    printf("Bellman-Ford\nShortest Paths");
    printf("from node %d:\n", start);
    for (int i = 0; i < graph->V; i++) {
        if (dist[i] == INT_MAX) {
            printf("Node %d is unreachable\n", i);
        } else {
            printf("Distance to node %d: %d\n", i, dist[i]);
        }
    }
}
// Kruskal's Algorithm for Minimum Spanning Tree
void kruskal(Graph* graph) {
    // Create edge list
    typedef struct {
        int u, v, weight;
    } Edge;
    Edge edges[MAX_NODES * MAX_NODES];
    int edgeCount = 0;

    for (int i = 0; i < graph->V; i++) {
        for (int j = i + 1; j < graph->V; j++) {
            if (graph->adj[i][j] == 1) {
                edges[edgeCount++] = (Edge){i, j, graph->weights[i][j]};
            }
        }
    }

    // Sort edges by weight
    for (int i = 0; i < edgeCount - 1; i++) {
        for (int j = i + 1; j < edgeCount; j++) {
            if (edges[i].weight > edges[j].weight) {
                Edge temp = edges[i];
                edges[i] = edges[j];
                edges[j] = temp;
            }
        }
    }

    UnionFind uf;
    initUnionFind(&uf, graph->V);

    printf("Kruskal's Minimum Spanning Tree:\n");
    for (int i = 0; i < edgeCount; i++) {
        int u = edges[i].u;
        int v = edges[i].v;
        int weight = edges[i].weight;

        if (find(&uf, u) != find(&uf, v)) {
            unionSets(&uf, u, v);
            printf("Edge: %d - %d, Weight: %d\n", u, v, weight);
        }
    }
}




void topologicalSortUtil(Graph* graph, int v, bool* visited, bool* inRecursionStack, Stack* stack) {
    if (inRecursionStack[v]) {
        // If the node is in the current recursion stack, a cycle is detected
        printf("Graph contains a cycle.\n Topological sort is not possible.\n");
        exit(1);  // Exit or handle cycle error as appropriate
    }

    if (visited[v]) {
        return;  // If already visited, no need to process again
    }

    visited[v] = true;
    inRecursionStack[v] = true;  // Mark the node as being in the recursion stack

    for (int i = 0; i < graph->V; i++) {
        if (graph->adj[v][i] == 1) {
            topologicalSortUtil(graph, i, visited, inRecursionStack, stack);
        }
    }

    inRecursionStack[v] = false;  // Remove from the recursion stack after processing

    push(stack, v);  // Push current node to stack
}

void topologicalSort(Graph* graph) {
    bool visited[MAX_NODES] = {false};
    bool inRecursionStack[MAX_NODES] = {false};  // Track nodes in the current recursion stack
    Stack stack;
    initStack(&stack);  // Stack to store the topological order

    for (int i = 0; i < graph->V; i++) {
        if (!visited[i]) {
            topologicalSortUtil(graph, i, visited, inRecursionStack, &stack);
        }
    }

    printf("Topological Sort: ");
    while (!isStackEmpty(&stack)) {
        printf("%d ", pop(&stack));
    }
    printf("\n");
}



// Floyd-Warshall Algorithm for All-Pairs Shortest Path
void floyd_warshall(Graph* graph) {
    int dist[MAX_NODES][MAX_NODES];

    // Initialize distance matrix
    for (int i = 0; i < graph->V; i++) {
        for (int j = 0; j < graph->V; j++) {
            if (i == j) {
                dist[i][j] = 0;
            } else if (graph->adj[i][j] == 1) {
                dist[i][j] = graph->weights[i][j];
            } else {
                dist[i][j] = INT_MAX;
            }
        }
    }

    // Apply Floyd-Warshall algorithm
    for (int k = 0; k < graph->V; k++) {
        for (int i = 0; i < graph->V; i++) {
            for (int j = 0; j < graph->V; j++) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX && dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }

    printf("Floyd-Warshall \n All-Pairs Shortest Paths:\n");
    printf("Shortest Paths:\n");
    for (int i = 0; i < graph->V; i++) {
        for (int j = 0; j < graph->V; j++) {
            if (dist[i][j] == INT_MAX) {
                printf("INF ");
            } else {
                printf("%d ", dist[i][j]);
            }
        }
        printf("\n");
    }
}
 
bool bfsMaxFlow(Graph* graph, int source, int sink, int parent[]) {
    int visited[MAX_NODES] = {0};
    Queue q;
    initQueue(&q);
    visited[source] = 1;
    enqueue(&q, source);

    while (!isQueueEmpty(&q)) {
        int u = dequeue(&q);

        for (int v = 0; v < graph->V; v++) {
            // Only consider the edge if there's available capacity
            if (graph->weights[u][v] > 0 && !visited[v]) {
                visited[v] = 1;
                enqueue(&q, v);
                parent[v] = u;
                if (v == sink) return true;  // If we reached the sink, return true
            }
        }
    }

    return false;
}

// Ford-Fulkerson algorithm to calculate the max flow
void maxFlow(Graph* graph, int source, int sink) {
    int parent[MAX_NODES];  // Array to store the path
    int maxFlow = 0;

    // Augment the flow while there's a path from source to sink
    while (bfsMaxFlow(graph, source, sink, parent)) {
        int pathFlow = INT_MAX;

        // Find the maximum flow in the path found by BFS
        for (int v = sink; v != source; v = parent[v]) {
            int u = parent[v];
            pathFlow = (pathFlow < graph->weights[u][v]) ? pathFlow : graph->weights[u][v];
        }

        // Update residual capacities of the edges and reverse edges
        for (int v = sink; v != source; v = parent[v]) {
            int u = parent[v];
            graph->weights[u][v] -= pathFlow;  // Decrease the flow on the forward edge
            graph->weights[v][u] += pathFlow;  // Increase the flow on the reverse edge
        }

        maxFlow += pathFlow;  // Add the flow of this path to the total max flow
    }

    // Print the result
    printf("Max Flow from node %d to node %d: %d\n", source, sink, maxFlow);
}


void graph_metrics(Graph* graph) {
    int node_count = graph->V;
    int edge_count = 0;

    // Calculate edge count
    for (int i = 0; i < graph->V; i++) {
        for (int j = 0; j < graph->V; j++) {
            if (graph->adj[i][j]) {
                edge_count++;
            }
        }
    }
    edge_count /= 2;  // Since the graph is undirected

    // Calculate density
    float density = (2.0 * edge_count) / (node_count * (node_count - 1));

    printf("Graph Metrics:\n");
    printf("Node Count: %d\n", node_count);
    printf("Edge Count: %d\n", edge_count);
    printf("Density: %.2f\n", density);

}






void parse_graph(Graph* graph, const char* graph_data) {
    int node_count, edge_count;
    const char* ptr = graph_data;

    // Parse number of nodes
    sscanf(ptr, "%d", &node_count);
    graph->V = node_count;

    // Initialize adjacency and weights matrices
    for (int i = 0; i < node_count; i++) {
        for (int j = 0; j < node_count; j++) {
            graph->adj[i][j] = 0;  // No edges by default
            graph->weights[i][j] = -1;  // -1 indicates no connection
        }
    }

    // Move to node definitions
    ptr = strchr(ptr, '\n') + 1;  // Move to the line after the node count

    // Parse nodes (but node coordinates are not used in the graph struct)
    for (int i = 0; i < node_count; i++) {
        int label, x, y;
        sscanf(ptr, "%d %d %d", &label, &x, &y);
        ptr = strchr(ptr, '\n') + 1;  // Move to the next line
    }

    // Parse number of edges
    sscanf(ptr, "%d", &edge_count);
    ptr = strchr(ptr, '\n') + 1;  // Move to the line after the edge count

    // Parse edges
    for (int i = 0; i < edge_count; i++) {
        int node1, node2, weight;
        sscanf(ptr, "%d %d %d", &node1, &node2, &weight);

        // Update adjacency matrix
        graph->adj[node1][node2] = 1;
        graph->adj[node2][node1] = 1;

        // Update weights matrix
        graph->weights[node1][node2] = weight;
        graph->weights[node2][node1] = weight;

        ptr = strchr(ptr, '\n') + 1;  // Move to the next line
    }
}

void print_graph(const Graph* graph) {
    printf("Graph:\n");
    printf("Number of vertices: %d\n", graph->V);
    
    printf("\nAdjacency Matrix:\n");
    for (int i = 0; i < graph->V; i++) {
        for (int j = 0; j < graph->V; j++) {
            printf("%d ", graph->adj[i][j]);
        }
        printf("\n");
    }

    printf("\nWeights Matrix:\n");
    for (int i = 0; i < graph->V; i++) {
        for (int j = 0; j < graph->V; j++) {
            if (graph->weights[i][j] == 0) {
                printf("- ");  // Print '-' for edges with no weight
            } else {
                printf("%d ", graph->weights[i][j]);
            }
        }
        printf("\n");
    }
}


// Main function to run the correct algorithm based on input
int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <algorithm> <graph_data>\n", argv[0]);
        return 1;
    }

    int algorithm = atoi(argv[1]);  // Algorithm number (1 - BFS, 2 - DFS, 3 - Dijkstra, 4 - Prim's, 5 - Bellman-Ford, 6 - Kruskal's, 7 - Floyd-Warshall, 8 - Topological Sort)
    const char* graph_data = argv[2];  // Graph data passed from Python

    Graph graph;
    parse_graph(&graph, graph_data);  // Parse the graph from the Python input
    
   // print_graph(&graph);



    int start_node = atoi(argv[3]);  // Starting node for the algorithm

    // Run the appropriate algorithm
    switch (algorithm) {

        case 0:
            graph_metrics(&graph);  // Call the graph metrics function
            break;
        case 1:
            bfs(&graph, start_node);  // Call the graph bfs algorithm
            break;
        case 2:
            dfs(&graph, start_node);   // Call the graph dfs algorithm
            break;
        case 3:
            dijkstra(&graph, start_node);   // Call the graph dijkstra algorithm 
            break;
        case 4:
           prim(&graph);  // Call Prim's Algorithm
            break;
        case 5:
            bellman_ford(&graph, start_node);  // Call Bellman-Ford Algorithm
            break;
        case 6:
            kruskal(&graph);  // Call Kruskal's Algorithm
            break;
        case 7:
            floyd_warshall(&graph);  // Call Floyd-Warshall Algorithm
            break;
        case 8:
            topologicalSort(&graph);  // Call Topological Sort
            break;
        case 9:
            maxFlow(&graph, start_node, atoi(argv[4]));  
            break;
        default:
            printf("Invalid algorithm choice. Use 1 for BFS, 2 for DFS, 3 for Dijkstra, 4 for Prim's, 5 for Bellman-Ford, 6 for Kruskal's, 7 for Floyd-Warshall, or 8 for Topological Sort.\n");
    }

    return 0;
}
