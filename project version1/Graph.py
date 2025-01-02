import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Enhanced Graph Visualization')

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 102, 204)
DARK_BLUE = (0, 51, 102)
RED = (255, 69, 0)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

# Node class
class Node:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.label})"

# Graph class (Immutable)
class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.selected_node = None
        self.start_node = None

    def add_node(self, x, y):
        label = len(self.nodes)
        new_node = Node(x, y, label)
        new_nodes = self.nodes + [new_node]
        new_edges = self.edges.copy()
        new_edges[label] = []  # New node has no edges initially

        # Return a new graph with the new node added
        return Graph._create_graph(new_nodes, new_edges)

    def add_edge(self, node1_label, node2_label):
        # Check if node1 and node2 exist in the graph
        if node1_label not in self.edges or node2_label not in self.edges:
            return self  # Return the graph unchanged if nodes are not found

        # Handle self-loop correctly
        new_edges = {k: frozenset(v) for k, v in self.edges.items()}
        
        # Add edge between node1 and node2 (including self-loop)
        new_edges[node1_label] = frozenset(new_edges.get(node1_label, set()) | {node2_label})
        new_edges[node2_label] = frozenset(new_edges.get(node2_label, set()) | {node1_label})

        # Return a new graph with the added edge
        return Graph._create_graph(self.nodes, new_edges)

        new_edges = {k: frozenset(v) for k, v in self.edges.items()}
        new_edges[node1_label] = frozenset(new_edges.get(node1_label, set()) | {node2_label})
        new_edges[node2_label] = frozenset(new_edges.get(node2_label, set()) | {node1_label})

        # Return a new graph with the added edge
        return Graph._create_graph(self.nodes, new_edges)

    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - x) ** 2 + (node.y - y) ** 2 <= 20 ** 2:
                return node
        return None

    @staticmethod
    def _create_graph(nodes, edges):
        graph = Graph()
        graph.nodes = nodes
        graph.edges = edges
        return graph

    def __repr__(self):
        return f"Graph({self.nodes}, {self.edges})"

# Draw graph function
def draw_graph(graph, highlight_nodes=[]):
    screen.fill(WHITE)

    # Draw edges
    for node, neighbors in graph.edges.items():
        for neighbor in neighbors:
            pygame.draw.line(screen, GRAY,
                             (graph.nodes[node].x, graph.nodes[node].y),
                             (graph.nodes[neighbor].x, graph.nodes[neighbor].y), 3)

    # Draw nodes
    for node in graph.nodes:
        if graph.start_node and node.label == graph.start_node.label:
            color = GREEN
        elif node.label in highlight_nodes:
            color = RED
        else:
            color = BLUE
        pygame.draw.circle(screen, color, (node.x, node.y), 20)
        pygame.draw.circle(screen, DARK_BLUE, (node.x, node.y), 20, 2)
        font = pygame.font.SysFont(None, 24)
        label = font.render(str(node.label), True, WHITE)
        screen.blit(label, (node.x - 10, node.y - 10))

    pygame.display.update()

# Main function
def main():
    graph = Graph()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                clicked_node = graph.find_node(x, y)

                if clicked_node:
                    if graph.selected_node is None:
                        graph.selected_node = clicked_node
                    else:
                        # Add edge between selected node and clicked node
                        graph = graph.add_edge(graph.selected_node.label, clicked_node.label)
                        graph.selected_node = None
                else:
                    graph = graph.add_node(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Press E to exit
                    running = False
                elif event.key == pygame.K_c:  # Clear the graph
                    graph = Graph()
                elif event.key == pygame.K_r:  # Random graph
                    graph = Graph()
                    num_nodes = random.randint(5, 10)
                    for _ in range(num_nodes):
                        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
                        graph = graph.add_node(x, y)
                    for _ in range(num_nodes * 2):
                        n1, n2 = random.sample(range(num_nodes), 2)
                        graph = graph.add_edge(n1, n2)
                elif event.key == pygame.K_s:  # Select start node for BFS/DFS
                    x, y = pygame.mouse.get_pos()
                    selected_start_node = graph.find_node(x, y)
                    if selected_start_node:
                        graph.start_node = selected_start_node

        draw_graph(graph)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
