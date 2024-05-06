class NodeNotFound(Exception):
    """Exception raised when a node is not found in a graph."""

    def __init__(self, nodes: str | set[str]) -> None:
        self.nodes = nodes
        super().__init__(f"Nodes {nodes} not found in the graph.")
