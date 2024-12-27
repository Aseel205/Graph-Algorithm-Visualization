import subprocess
import pygame
import sys
import random
import tkinter as tk
from tkinter.simpledialog import askinteger
import time 
from pygame.locals import *
from pygame import font


exe_path = r'C:\Users\aseel\OneDrive\Desktop\mini project\project3\graph_algorithms.exe'  # Absolute path to the executable

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Algorithm Visualization")

# Colors
WHITE, BLACK, RED, GREEN, BLUE, GRAY, YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200), (255, 255, 0)
TERMINAL_HEIGHT = 200  # Height for the terminal output area
GRAPH_HEIGHT = HEIGHT - TERMINAL_HEIGHT  # Height for the graph visualization area

# Node and Graph classes
class Node:
    def __init__(self, x, y, label):
        self.x, self.y, self.label = x, y, label

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.start_node = None

    def add_node(self, x, y):
        label = len(self.nodes)
        self.nodes.append(Node(x, y, label))
        self.edges[label] = {}

    def add_edge(self, node1, node2, weight=1):
        if node1 in self.edges and node2 in self.edges:
            self.edges[node1][node2] = weight
            self.edges[node2][node1] = weight

    def remove_node(self, node_label):
        self.edges.pop(node_label, None)  
        for node in self.edges.values():
            if node_label in node:
                node.pop(node_label, None)  

        self.nodes = [node for node in self.nodes if node.label != node_label]


    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - x) ** 2 + (node.y - y) ** 2 <= 25 ** 2:
                return node
        return None

    def generate_random_graph(self, num_nodes, num_edges):
        self.nodes = []
        self.edges = {}
        # Adjust node placement to ensure it stays within the graph visualization area
        for i in range(num_nodes):
            x = random.randint(50, WIDTH - WIDTH // 3 - 50)  # Constrain to the left side
            y = random.randint(50, GRAPH_HEIGHT - 50)  # Constrain to the graph area height
            self.add_node(x, y)
        for _ in range(num_edges):
            node1, node2 = random.sample(range(num_nodes), 2)
            weight = random.randint(1, 20)
            self.add_edge(node1, node2, weight)


def draw_graph(graph, zoom_level):
    graph_surface = pygame.Surface((WIDTH - WIDTH // 3, HEIGHT))  # Full height, exclude terminal width
    graph_surface.fill(WHITE)  # Background for the graph area

    for node1, neighbors in graph.edges.items():
        if node1 >= len(graph.nodes):  # Check if the node exists in the graph
            continue  # Skip invalid nodes
        for node2, weight in neighbors.items():
            if node2 >= len(graph.nodes):  # Check if the connected node exists
                continue  # Skip invalid nodes

            # Scale edge positions based on zoom level
            start_x, start_y = graph.nodes[node1].x * zoom_level, graph.nodes[node1].y * zoom_level
            end_x, end_y = graph.nodes[node2].x * zoom_level, graph.nodes[node2].y * zoom_level
            
            color = GRAY
            pygame.draw.line(graph_surface, color, (start_x, start_y), (end_x, end_y), 2)

            # Calculate midpoint for the weight label (scaled)
            mid_x = (start_x + end_x) // 2
            mid_y = (start_y + end_y) // 2
            font = pygame.font.SysFont(None, 20)
            weight_text = font.render(str(weight), True, BLACK)
            graph_surface.blit(weight_text, (mid_x, mid_y))

    for node in graph.nodes:
        color = GREEN if node == graph.start_node else BLUE

        # Scale node position and size
        scaled_x = int(node.x * zoom_level)
        scaled_y = int(node.y * zoom_level)
        scaled_radius = int(20 * zoom_level)

        # Draw the node (scaled)
        pygame.draw.circle(graph_surface, color, (scaled_x, scaled_y), scaled_radius)
        pygame.draw.circle(graph_surface, BLACK, (scaled_x, scaled_y), scaled_radius, 2)

        # Render label (scaled position)
        font = pygame.font.SysFont(None, 24)
        label = font.render(str(node.label), True, WHITE)
        graph_surface.blit(label, (scaled_x - 10, scaled_y - 10))

    # Display zoom percentage
    zoom_percentage = int(zoom_level * 100)  # Convert zoom level to percentage
    font = pygame.font.SysFont(None, 30)
    zoom_text = font.render(f"Zoom: {zoom_percentage}%", True, BLACK)
    graph_surface.blit(zoom_text, (10, 10))  # Display in the top-left corner

    screen.blit(graph_surface, (0, 0))  # Place graph visualization on the left



# Function to serialize the graph into a plain text format
def serialize_graph(graph):
    graph_data = []
    graph_data.append(f"{len(graph.nodes)}")  # Number of nodes
    for node in graph.nodes:
        graph_data.append(f"{node.label} {node.x} {node.y}")  # Node format: label x y
    
    edge_count = sum(len(neighbors) for neighbors in graph.edges.values()) // 2  # Total number of edges (undirected)
    graph_data.append(f"{edge_count}")
    for node1, neighbors in graph.edges.items():
        for node2, weight in neighbors.items():
            if node1 < node2:  # Ensure each edge is only added once (undirected)
                graph_data.append(f"{node1} {node2} {weight}")  # Edge format: node1 node2 weight
    
    return "\n".join(graph_data)

# Function to call the C algorithm and capture output for display
def call_c_algorithm(algorithm, graph, start_node):
    try:
        # Serialize the graph data
        graph_data = serialize_graph(graph)  # Convert the graph to plain text
        start_node_label = start_node.label if start_node else -1  # Default to -1 if no start node

        # Run the C program with the algorithm number, graph data, and start node
        result = subprocess.run([exe_path, str(algorithm), graph_data, str(start_node_label)], capture_output=True, text=True)
        return result.stdout  # Return the output from the C program
    except Exception as e:
        print(f"Error calling {algorithm}: {e}")
        return None

def handle_key_event(key, graph, selected_node):
    print(f"Key pressed: {key}")  # Debugging: Print the key pressed

    # Map keys to algorithms (1-8)
    algorithm_keys = {
        pygame.K_0:0,   
        pygame.K_1: 1,  # BFS
        pygame.K_2: 2,  # DFS
        pygame.K_3: 3,  # Dijkstra
        pygame.K_4: 4,  # Prim's
        pygame.K_5: 5,  # Bellman-Ford
        pygame.K_6: 6,  # Kruskal's
        pygame.K_7: 7,  # Floyd-Warshall
        pygame.K_8: 8,  # Topological Sort
        pygame.K_9: 9,   # MaxFlow
       
    }

    # Check if the key corresponds to an algorithm
    if key in algorithm_keys:
        algorithm = algorithm_keys[key]
        print(f"Selected algorithm: {algorithm}")  # Debugging: Print selected algorithm

        # Check if start node is requiredq
        if algorithm in {1, 2, 3, 5} and not graph.start_node:  # BFS, DFS, Dijkstra, Bellman-Ford need a start node
            print("No start node selected.")  # Debugging: Notify the user
            return

        # Call the C algorithm
        if graph.start_node:
            print(f"Running algorithm {algorithm} with start node: {graph.start_node.label}")  # Debugging
            output = call_c_algorithm(algorithm, graph, graph.start_node)  # Pass start node
        else:
            print(f"Running algorithm {algorithm} without a start node.")  # Debugging
            output = call_c_algorithm(algorithm, graph, None)  # No start node needed

        # Update terminal output if there's a result
        if output:
            update_terminal_output(output)
    else:
        print("Invalid key pressed. Please press 1 to 8 for the algorithms.")  # Debugging: Invalid key


# Function to simulate the terminal output in the Pygame window
terminal_output = []  # To store lines of output that simulate the terminal
def update_terminal_output(output):
    global terminal_output
    lines = output.splitlines()
    terminal_output.extend(lines)
    if len(terminal_output) > 20:  # Limit the number of lines to 20
        terminal_output = terminal_output[-20:]


def draw_terminal():
    terminal_surface = pygame.Surface((WIDTH // 3, HEIGHT))  # Terminal occupies the right side
    terminal_surface.fill(GRAY)  # Background color for terminal

    terminal_font = pygame.font.SysFont('Courier', 18)  # Monospaced font for terminal text
    y_offset = 10  # Initial vertical offset for text in the terminal area

    # Draw each line in terminal_output and update the y_offset
    for line in terminal_output:
        text_surface = terminal_font.render(line, True, BLACK)  # Black text for terminal
        terminal_surface.blit(text_surface, (10, y_offset))  # Add text to terminal surface
        y_offset += 22  # Line spacing

        # Stop drawing if we exceed the available space for the terminal area
        if y_offset > HEIGHT - 10:  # 10 is a small buffer to avoid cutting off
            break

    screen.blit(terminal_surface, (WIDTH - WIDTH // 3, 0))  # Place terminal on the right side of the screen

def get_node_info(node, graph):
    """Get detailed information about the clicked node."""
    edges = []
    for neighbor, weight in graph.edges.get(node.label, {}).items():
        edges.append(f"Node {neighbor} with weight {weight}")
    edges_info = "\n".join(edges) if edges else "No edges connected"
    return f"Node {node.label} at ({node.x}, {node.y})\nConnected Edges:\n{edges_info}"


def calculate_metrics(graph):
    """Calculate and return real-time graph metrics."""
    num_nodes = len(graph.nodes)
    num_edges = sum(len(neighbors) for neighbors in graph.edges.values()) // 2  # Undirected edges
    density = (2 * num_edges) / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0

    # Count connected components using a simple BFS/DFS approach
    visited = set()
    components = 0

    def dfs(node_label):
        stack = [node_label]
        while stack:
            node = stack.pop()
            for neighbor in graph.edges.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

    for node in graph.nodes:
        if node.label not in visited:
            visited.add(node.label)
            dfs(node.label)
            components += 1

    return num_nodes, num_edges, density, components


def draw_metrics(graph):
    """Draw the real-time metrics in the lower-right area of the sidebar."""
    metrics_surface = pygame.Surface((WIDTH // 3, HEIGHT // 3))  # Use a third of the sidebar for metrics
    metrics_surface.fill(WHITE)  # Background color for metrics area

    # Calculate metrics
    num_nodes, num_edges, density, components = calculate_metrics(graph)

    # Render metrics
    font = pygame.font.SysFont('Courier', 20)  # Font for metrics
    metrics_text = [
        f"Nodes: {num_nodes}",
        f"Edges: {num_edges}",
        f"Density: {density:.3f}",
        f"Components: {components}"
    ]

    y_offset = 10  # Initial vertical offset
    for text in metrics_text:
        rendered_text = font.render(text, True, BLACK)  # Black text
        metrics_surface.blit(rendered_text, (10, y_offset))  # Draw text on metrics surface
        y_offset += 30  # Line spacing

    # Place the metrics surface in the lower-right area of the sidebar
    screen.blit(metrics_surface, (WIDTH - WIDTH // 3, HEIGHT - HEIGHT // 3))


def main():
    pygame.init()
    pygame.mixer.init()

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph Visualization")  # Set a cool title for the window

    # Load and set window icon (your logo image)
    logo = pygame.image.load('logo.png')
    pygame.display.set_icon(logo)

    # Load sound effect for adding a node
    add_node_sound = pygame.mixer.Sound("vee_pop.mp3")

    graph = Graph()  # Initialize the graph
    running = True  # Main loop control
    selected_node = None  # Node selection for edge creation
    zoom_level = 1.0  # Default zoom level
    root = tk.Tk()
    root.withdraw()  # Hide the root window for tkinter

    current_node_under_cursor = None  # To store the node under the cursor

    # Splash Screen - Show logo
    screen.fill(WHITE)
    logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(logo, logo_rect)  # Display logo
    pygame.display.update()
    time.sleep(5)  # Display the logo for 5 seconds

    while running:
        screen.fill(WHITE)  # Clear the screen
        for event in pygame.event.get():  # Check for events
            if event.type == pygame.QUIT:  # Close the window
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
                x, y = pygame.mouse.get_pos()
                if x < WIDTH - WIDTH // 3 and zoom_level == 1:  # Allow clicks only when zoom level is 1
                    clicked_node = graph.find_node(x / zoom_level, y / zoom_level)  # Adjust for zoom
                    if clicked_node:
                        if selected_node == clicked_node:
                            graph.start_node = clicked_node
                            selected_node = None
                        elif selected_node:
                            weight = askinteger(
                                "Edge Weight",
                                f"Enter weight for edge ({selected_node.label}, {clicked_node.label}):"
                            )
                            if weight is not None:
                                graph.add_edge(selected_node.label, clicked_node.label, weight)
                            selected_node = None
                        else:
                            selected_node = clicked_node
                    else:
                        graph.add_node(x / zoom_level, y / zoom_level)  # Adjust for zoom
                        add_node_sound.play()  # Play sound when adding a node
                        selected_node = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Generate random graph
                    num_nodes = askinteger("Number of Nodes", "Enter the number of nodes:")
                    num_edges = askinteger("Number of Edges", "Enter the number of edges:")
                    if num_nodes is not None and num_edges is not None:
                        graph.generate_random_graph(num_nodes, num_edges)
                elif event.key == pygame.K_c:  # Clear the graph
                    graph = Graph()
                elif event.key == pygame.K_e:  # Exit the program
                    running = False
                    # Special exit effect
                    screen.fill(WHITE)

                    # Load the goodbye image
                    goodbye_image = pygame.image.load('goodbye.png')
                    image_rect = goodbye_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                    # Blit the goodbye image onto the screen
                    screen.blit(goodbye_image, image_rect)
                    pygame.display.update()  # Update the display to show the goodbye image
                    time.sleep(3)  # Show the goodbye image for 3 seconds
                    
            
                elif event.key == pygame.K_d:  # Delete a node
                    x, y = pygame.mouse.get_pos()
                    if x < WIDTH - WIDTH // 3 and zoom_level == 1:  # Ensure click is in the graph visualization area
                        clicked_node = graph.find_node(x / zoom_level, y / zoom_level)  # Adjust for zoom
                        if clicked_node:
                            graph.remove_node(clicked_node.label)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Zoom in
                    zoom_level += 0.1  # Increase zoom by 10%
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Zoom out
                    zoom_level -= 0.1  # Decrease zoom by 10%
                elif event.key == pygame.K_i and current_node_under_cursor:  # "I" key for info
                    node_info = get_node_info(current_node_under_cursor, graph)  # Get info for the node
                    update_terminal_output(node_info)  # Display info in the terminal
                else:
                    handle_key_event(event.key, graph, selected_node)

            elif event.type == pygame.MOUSEMOTION:  # Check for mouse motion
                x, y = pygame.mouse.get_pos()
                current_node_under_cursor = graph.find_node(x / zoom_level, y / zoom_level)  # Adjust for zoom

        # Draw the graph with the current zoom level
        draw_graph(graph, zoom_level)

        # Draw the zoom percentage
        font = pygame.font.SysFont(None, 24)
        zoom_percent = f"Zoom: {int(zoom_level * 100)}%"
        zoom_text = font.render(zoom_percent, True, BLACK)
        screen.blit(zoom_text, (WIDTH - 200, 10))  # Position it near the top-right corner

        # Draw the terminal output on the right side
        draw_terminal()

        # Draw real-time metrics in the lower-right area
        draw_metrics(graph)

        # Update the display
        pygame.display.update()

    pygame.quit()  # Quit pygame
    sys.exit()  # Exit the program

if __name__ == "__main__":
    main()



