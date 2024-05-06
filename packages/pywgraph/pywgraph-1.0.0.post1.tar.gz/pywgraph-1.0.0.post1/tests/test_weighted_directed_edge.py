from pywgraph import WeightedDirectedEdge

def wedge() -> WeightedDirectedEdge:
    """Return a new WeightedDirectedEdge instance."""
    return WeightedDirectedEdge("A", "B", 3.1415)

class TestWeightedDirectedEdge:
    """Test the WeightedDirectedEdge class."""

    def test_weight(self): 
        assert wedge().weight == 3.1415

    def test_start(self):
        assert wedge().start == "A"

    def test_end(self):
        assert wedge().end == "B"

    def test_inverse(self):
        assert wedge().inverse == WeightedDirectedEdge("B", "A", 1/3.1415)

    def test_equal(self):
        assert wedge() == WeightedDirectedEdge("A", "B", 3.1415)