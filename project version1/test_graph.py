import pytest
from Graph import Graph  # Replace with actual path to your Graph class

def test_empty_graph():
    graph = Graph()
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0

def test_immutable_behavior():
    graph = Graph()
    graph_with_node = graph.add_node(100, 100)  # Assuming node added at position (100, 100)
    assert len(graph.nodes) == 0  # Original graph has no nodes
    assert len(graph_with_node.nodes) == 1  # New graph has 1 node

def test_self_loop():
    graph = Graph()
    graph_with_node = graph.add_node(100, 100)
    graph_with_loop = graph_with_node.add_edge(0, 0)  # Assuming node 0 is created
    # Check that node 0 has a self-loop
    assert 0 in graph_with_loop.edges[0]  # Check that node 0 has a self-loop in its edge list


def test_isolated_nodes():
    graph = Graph()
    graph_with_nodes = graph.add_node(100, 100).add_node(200, 200)
    # No edges yet, so neighbors should be empty
    assert len(graph_with_nodes.edges[0]) == 0  # Node 0 has no neighbors
    assert len(graph_with_nodes.edges[1]) == 0  # Node 1 has no neighbors

def test_large_graph():
    graph = Graph()
    num_nodes = 1000
    graph_with_nodes = graph
    for i in range(num_nodes):
        graph_with_nodes = graph_with_nodes.add_node(i * 10, i * 10)

    assert len(graph_with_nodes.nodes) == num_nodes  # Check correct number of nodes

    for i in range(num_nodes - 1):
        graph_with_nodes = graph_with_nodes.add_edge(i, i + 1)  # Add edges between consecutive nodes

    # Count unique edges (bidirectional)
    unique_edges = set()
    for node, neighbors in graph_with_nodes.edges.items():
        for neighbor in neighbors:
            unique_edges.add(frozenset([node, neighbor]))  # Use frozenset to ignore order

    assert len(unique_edges) == num_nodes - 1  # Correct number of unique edges

def test_graph_connectivity():
    graph = Graph()
    graph_with_nodes = graph.add_node(100, 100).add_node(200, 200).add_node(300, 300)
    graph_with_edges = graph_with_nodes.add_edge(0, 1)  # Connect node 0 and node 1
    assert 1 in graph_with_edges.edges[0]  # Node 0 should be connected to node 1
    assert 2 not in graph_with_edges.edges[0]  # Node 0 should not be connected to node 2
