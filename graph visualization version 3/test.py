import subprocess

# Example graph data and start node
graph_data = "4\n0 0 0\n1 1 0\n2 2 0\n3 3 0\n5\n0 1 2\n0 2 3\n1 2 1\n1 3 4\n2 3 5"
algorithm = 4
start_node = 0

# Run the C program using subprocess
result = subprocess.run(
    ['graph_algorithms.exe', str(algorithm), graph_data, str(start_node)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Print the output
print(result.stdout.decode())
