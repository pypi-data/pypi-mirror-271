from pywgraph import WeightedDirectedGraph, WeightedDirectedEdge


def graph() -> WeightedDirectedGraph:
    nodes = {"A", "B", "C"}
    edges = {
        WeightedDirectedEdge("A", "B", 7),
        WeightedDirectedEdge("A", "C", 9),
        WeightedDirectedEdge("B", "C", 10),
    }
    return WeightedDirectedGraph(nodes, edges)


_dict_graph: dict[str, dict[str, float]] = {
    "A": {"B": 7, "C": 9},
    "B": {"C": 10},
    "C": {},
}


class TestWeightedDirectedGraph:

    def test_nodes(self):
        assert graph().nodes == {"A", "B", "C"}

    def test_edges(self):
        assert graph().edges == {
            WeightedDirectedEdge("A", "B", 7),
            WeightedDirectedEdge("A", "C", 9),
            WeightedDirectedEdge("B", "C", 10),
        }

    def test_well_defined(self):
        assert graph().check_definition()

    def test_bad_defined(self):
        assert (
            WeightedDirectedGraph(
                {"A"}, {WeightedDirectedEdge("A", "B", 7)}
            ).check_definition()
            == False
        )

    def test_children(self):
        assert graph().children("A") == {"B", "C"}

    def test_parents(self):
        assert graph().parents("C") == {"A", "B"}

    def test_equal(self):
        nodes = {"A", "B", "C"}
        edges = {
            WeightedDirectedEdge("A", "B", 7),
            WeightedDirectedEdge("A", "C", 9),
            WeightedDirectedEdge("B", "C", 10),
        }
        same_graph = WeightedDirectedGraph(nodes, edges)
        assert graph() == same_graph

    def test_fill_reverse_edges_inplace(self):
        filled_graph = WeightedDirectedGraph(
            {"A", "B", "C"},
            {
                WeightedDirectedEdge("A", "B", 7),
                WeightedDirectedEdge("B", "A", 1 / 7),
                WeightedDirectedEdge("A", "C", 9),
                WeightedDirectedEdge("C", "A", 1 / 9),
                WeightedDirectedEdge("B", "C", 10),
                WeightedDirectedEdge("C", "B", 1 / 10),
            },
        )
        graph_copy = graph()
        graph_copy.add_reverse_edges(inplace=True)
        assert graph_copy == filled_graph

    def test_fill_reverse_edges(self):
        filled_graph = WeightedDirectedGraph(
            {"A", "B", "C"},
            {
                WeightedDirectedEdge("A", "B", 7),
                WeightedDirectedEdge("B", "A", 1 / 7),
                WeightedDirectedEdge("A", "C", 9),
                WeightedDirectedEdge("C", "A", 1 / 9),
                WeightedDirectedEdge("B", "C", 10),
                WeightedDirectedEdge("C", "B", 1 / 10),
            },
        )
        assert graph().add_reverse_edges() == filled_graph

    def test_from_dict_method(self):
        graph_from_dict = WeightedDirectedGraph.from_dict(_dict_graph)
        assert graph() == graph_from_dict
