from pywgraph import DirectedEdge


def edge() -> DirectedEdge:
    return DirectedEdge("A", "B")


class TestDirectedEdge:
    def test_start_edge(self):
        assert edge().start == "A"

    def test_end_edge(self):
        assert edge().end == "B"

    def test_inverse_edge(self): 
        assert edge().inverse == DirectedEdge("B", "A")

    def test_equality_edge(self):
        assert edge() == DirectedEdge("A", "B")

    def test_inequality_edge(self):
        assert edge() != DirectedEdge("A", "C")
        