# Graph Algorithm Visualization Tool

This project provides an interactive Python-based tool for building and visualizing graphs. Users can add nodes and edges, perform graph operations, and apply algorithms implemented in a C backend. The tool leverages Pygame for visualization and Tkinter for user prompts.

## Features

- **Interactive Graph Building:**
  - Add nodes by clicking on the canvas.
  - Add weighted edges by clicking two nodes and specifying the weight.
  - Remove nodes.
  - Generate random graphs with a specified number of nodes and edges.
  - Clear the entire graph.

- **Zooming:**
  - Use `+` or `-` to zoom in and out of the graph visualization.

- **Graph Algorithms:**
  - Call algorithms implemented in the C backend by pressing keys `1` to `8`.
  - Supported algorithms:
    1. **BFS** (Breadth-First Search)
    2. **DFS** (Depth-First Search)
    3. **Dijkstra's Shortest Path**
    4. **Prim's MST** (Minimum Spanning Tree)
    5. **Bellman-Ford**
    6. **Kruskal's MST**
    7. **Floyd-Warshall**
    8. **Topological Sort**

- **Simulated Terminal Output:**
  - Algorithm results are displayed in a terminal-like area on the right side of the window.
  - View information about selected nodes and edges.

## Controls

### Mouse Controls
- **Left Click:** Add a node or select a node for edge creation.
- **Right Click:** View detailed node information in the terminal.

### Keyboard Controls
- **`r`**: Generate a random graph (requires user input for node and edge counts).
- **`c`**: Clear the graph.
- **`d`**: Delete the node under the cursor.
- **`+` / `-`**: Zoom in or out of the graph visualization.
- **`i`**: Display information about the node under the cursor.
- **`1-8`**: Call algorithms.
  - Algorithms requiring a start node (e.g., BFS, DFS) use the currently selected node.

### Exit
- **`e`**: Quit the application.
- Close the window directly.

## Graph Serialization
The Python program serializes the graph into plain text format and sends it to the C backend via subprocess. The format includes:

1. **Number of nodes**
2. **Node data:** Label, x-coordinate, y-coordinate
3. **Number of edges**
4. **Edge data:** Node1, Node2, weight

The C backend processes the graph and returns the output for visualization.

## Dependencies

- **Python Libraries:**
  - `pygame`
  - `tkinter`
  - `subprocess`
  - `random`

- **C Backend:**
  - Ensure `graph_algorithms.exe` is compiled and available at the specified path.

## Setup and Usage

1. Clone the repository.
2. Install required Python libraries:
   ```bash
   pip install pygame
   ```
3. Ensure `graph_algorithms.exe` is located at the correct path.
4. Run the Python program:
   ```bash
   python main.py
   ```
5. Use the controls described above to interact with the tool.

## File Structure

- **`main.py`**: Python script for graph visualization and user interaction.
- **`graph_algorithms.exe`**: C backend for executing graph algorithms.

## Example Usage

1. **Build a Graph:** Add nodes and connect them with weighted edges.
2. **Run Algorithms:** Select an algorithm (e.g., BFS by pressing `1`). Results are displayed in the terminal area.
3. **Zoom and Explore:** Zoom in or out to better view the graph structure.

---

Developed for graph visualization and algorithm learning.
