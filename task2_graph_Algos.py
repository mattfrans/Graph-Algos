def read_graph(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            v1, v2, weight, _ = line.strip().split('\t')
            weight = float(weight)
            if v1 not in graph:
                graph[v1] = {}
            if v2 not in graph:
                graph[v2] = {}
            graph[v1][v2] = weight
            graph[v2][v1] = weight
    return graph

def dijkstra(graph, start, end):
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node, weight in destinations.items():
            weight = weight_to_current_node + weight
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    path = path[::-1]
    return path

def max_path(graph, start, end, visited=None, path=None):
    if visited is None:
        visited = []
    if path is None:
        path = [start]

    visited.append(start)

    if start == end:
        return path

    max_path_weight = 0
    max_path = None
    for node in set(graph[start].keys()) - set(visited):
        new_path = max_path(graph, node, end, visited[:], path + [node])
        if new_path:
            new_path_weight = sum(graph[n1][n2] for n1, n2 in zip(new_path[:-1], new_path[1:]))
            if new_path_weight > max_path_weight:
                max_path_weight = new_path_weight
                max_path = new_path

    return max_path

def main():
    file_name = input("edges_1_27307.csv")
    graph = read_graph(file_name)

    print("Nodes of the graph: ", list(graph.keys()))

    while True:
        u, v = input("Enter a pair of nodes (u, v): ").split()
        min_path = dijkstra(graph, u, v)
        max_path_ = max_path(graph, u, v)

        print(f"Minimum weighted path from {u} to {v}: {min_path} with weight {sum(graph[n1][n2] for n1, n2 in zip(min_path[:-1], min_path[1:]))}")
        print(f"Maximum weighted path from {u} to {v}: {max_path_} with weight {sum(graph[n1][n2] for n1, n2 in zip(max_path_[:-1], max_path_[1:]))}")

        cont = input("Continue with a new pair of nodes? (y/n): ").lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
