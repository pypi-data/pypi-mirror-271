def _iterate_aux(
    graph, search_path: list[str], visited_nodes: set, end: str
) -> tuple[list[list[str]], set[str]]:
    """Auxiliary function to iterate through the graph. Here the graph parameter must
    be a WeightedDirectedGraph object."""
    current_node = search_path[-1]
    if current_node == end:
        return [[]], visited_nodes

    children = graph.children(current_node)
    new_paths = [
        search_path + [child] for child in children if child not in visited_nodes
    ]
    visited_nodes.update(children)
    return new_paths, visited_nodes


def _find_path(graph, start: str, end: str) -> list[str]:
    """Finds the shortest path between two nodes in a graph. Here the graph parameter must
    be a WeightedDirectedGraph."""
    all_paths = [[start]]
    visited_nodes = {start}
    while (end not in visited_nodes) and (len(all_paths) != 0):
        search_path = all_paths.pop(0)
        new_paths, visited_nodes = _iterate_aux(graph, search_path, visited_nodes, end)
        all_paths.extend(new_paths)

    if all_paths:
        return [path for path in all_paths if path[-1] == end][0]

    return []
