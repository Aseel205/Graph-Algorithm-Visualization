# Graph Algorithm Visualization

This project is an interactive Python application for visualizing and interacting with graphs. Users can construct graphs by adding nodes and edges, apply various graph algorithms, and view results dynamically. The application integrates with a C program to execute algorithms like BFS, DFS, and Dijkstra.

## Features

### Graph Construction

- Add nodes by clicking in the graph area.
- Create edges between nodes with specified weights.
- Delete nodes.
- Generate random graphs with a given number of nodes and edges.
- Clear all nodes and edges to reset the graph.

### Graph Interaction

- Visualize nodes and edges dynamically.
- Zoom in and out of the graph.
- Get detailed information about a specific node and its connections.

### Algorithm Execution

- Apply graph algorithms implemented in a C program.
- Results are displayed in a terminal-style output area within the application.

### Visualization

- **Graph Area**: Displays nodes and edges on the left side of the screen.
- **Terminal Area**: Shows algorithm results and node information on the right side.

## Controls

### Mouse

- **Left Click**:
  - Add a node by clicking on an empty area.
  - Select a node by clicking on it.
  - Create an edge between two selected nodes (prompts for weight).
  - Double-click a node to set it as the start node for algorithms.

### Keyboard

#### Graph Management:

- `R`: Generate a random graph (prompts for number of nodes and edges).
- `C`: Clear the graph.
- `D`: Delete a node under the mouse pointer.
- `E`: Exit the application.

#### Zoom:

- `+` or `KP+`: Zoom in.
- `-` or `KP-`: Zoom out.

#### Node Information:

- `I`: Display information about the node under the mouse pointer.

#### Algorithm Execution:

- `1`: Breadth-First Search (BFS).
- `2`: Depth-First Search (DFS).
- `3`: Dijkstra's Algorithm.
- `4`: Prim's Algorithm.
- `5`: Bellman-Ford Algorithm.
- `6`: Kruskal's Algorithm.
- `7`: Floyd-Warshall Algorithm.
- `8`: Topological Sort.

## Implementation Details

### Graph Representation

- **Nodes**: Represented by the `Node` class, which stores coordinates `(x, y)` and a unique label.
- **Edges**: Stored in a dictionary within the `Graph` class. Each node maintains a dictionary of neighbors and their edge weights.

### Graph Serialization

The graph is serialized into plain text format for communication with the C program. The format includes:

- Number of nodes and their positions.
- Number of edges and their details (start node, end node, weight).

### Integration with C

- The serialized graph is passed to the C program via `subprocess.run()`.
- The C program executes the selected algorithm and returns the results.
- Results are displayed in the terminal area within the application.

### Visualization

- **Graph Area**:
  - Nodes and edges are drawn dynamically based on user interactions.
  - Zoom level allows scaling of the graph.
- **Terminal Area**:
  - Displays output from the C program.
  - Provides additional information about selected nodes and actions.

## Requirements

### Python Dependencies

- `pygame`: For rendering the graphical interface.
- `tkinter`: For input dialogs.

### C Program

- Ensure the C program `graph_algorithms.exe` is compiled and located at the specified path in the script.

### System Requirements

- Python 3.x
- Windows or compatible OS

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/graph-algorithm-visualization.git
   ```

2. Install Python dependencies:

   ```bash
   pip install pygame
   ```

3. Compile the C program and place it in the correct path.

4. Run the Python script:

   ```bash
   python main.py
   ```

## Future Enhancements

- Add more algorithms.
- Improve UI responsiveness.
- Add support for directed graphs.

