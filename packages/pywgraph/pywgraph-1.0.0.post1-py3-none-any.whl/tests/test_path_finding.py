import pytest
from pywgraph import WeightedDirectedGraph, NodeNotFound


def graph() -> WeightedDirectedGraph:
    dictionary: dict[str, dict[str, float]] = {
        "A": {"B": 1.0, "C": 2.5},
        "B": {"C": 2.5},
        "C": {"A": 1 / 2.5, "D": 1.3},
        "D": {"E": 3.4},
        "E": {"C": 1 / (1.3 * 3.4), "A": 13.0},
        "Z": {},
    }
    return WeightedDirectedGraph.from_dict(dictionary)


class TestPathFinding:

    # region PathFindingTest
    def test_ab(self):
        assert graph().find_path("A", "B") == ["A", "B"]

    def test_ac(self):
        assert graph().find_path("A", "C") == ["A", "C"]

    def test_ad(self):
        assert graph().find_path("A", "D") == ["A", "C", "D"]

    def test_ae(self):
        assert graph().find_path("A", "E") == ["A", "C", "D", "E"]

    def test_ba(self):
        assert graph().find_path("B", "A") == ["B", "C", "A"]

    def test_bc(self):
        assert graph().find_path("B", "C") == ["B", "C"]

    def test_bd(self):
        assert graph().find_path("B", "D") == ["B", "C", "D"]

    def test_be(self):
        assert graph().find_path("B", "E") == ["B", "C", "D", "E"]

    def test_ca(self):
        assert graph().find_path("C", "A") == ["C", "A"]

    def test_cb(self):
        assert graph().find_path("C", "B") == ["C", "A", "B"]

    def test_cd(self):
        assert graph().find_path("C", "D") == ["C", "D"]

    def test_ce(self):
        assert graph().find_path("C", "E") == ["C", "D", "E"]

    def test_da(self):
        assert graph().find_path("D", "A") == ["D", "E", "A"]

    def test_db(self):
        assert graph().find_path("D", "B") == ["D", "E", "A", "B"]

    def test_dc(self):
        assert graph().find_path("D", "C") == ["D", "E", "C"]

    def test_de(self):
        assert graph().find_path("D", "E") == ["D", "E"]

    def test_ea(self):
        assert graph().find_path("E", "A") == ["E", "A"]

    def test_eb(self):
        assert graph().find_path("E", "B") == ["E", "A", "B"]

    def test_ec(self):
        assert graph().find_path("E", "C") == ["E", "C"]

    def test_ed(self):
        assert graph().find_path("E", "D") == ["E", "C", "D"]

    def test_az(self):
        assert graph().find_path("A", "Z") == []

    def test_self_node(self):
        for node in graph().nodes:
            assert graph().find_path(node, node) == [node]

    # region Path weights tests
    def test_path_weight_ab(self):
        path = ["A", "B"]
        assert graph().path_weight(path) == 1.0

    def test_path_weight_empty(self):
        path = []
        assert graph().path_weight(path, 0.0) == 0.0

    def test_path_weight_ae(self):
        path = ["A", "C", "D", "E"]
        assert graph().path_weight(path) == pytest.approx(2.5 * 1.3 * 3.4)

    def test_path_large_path(self): 
        path = ["A", "B", "C", "D", "E", "C", "A"]
        assert graph().path_weight(path) == pytest.approx(1.0)

    def test_path_weight_self_node(self):
        path = ["Z"]
        assert graph().path_weight(path) == 1.0

    def test_weight_between_ab(self):
        assert graph().weight_between("A", "B") == 1.0

    def test_weight_between_az(self):
        assert graph().weight_between("A", "Z", 0.0) == 0.0

    def test_weight_between_ae(self):
        assert graph().weight_between("A", "E") == pytest.approx(2.5 * 1.3 * 3.4)

    def test_weight_between_self_nodes(self):
        for node in graph().nodes:
            assert graph().weight_between(node, node) == 1.0

    # region ExceptionTests
    def test_end_node_not_in_graph_find_path(self):
        with pytest.raises(NodeNotFound):
            graph().find_path("A", "F")

    def test_start_node_not_in_graph_find_path(self):
        with pytest.raises(NodeNotFound):
            graph().find_path("F", "E")

    def test_both_nodes_not_in_graph_find_path(self):
        with pytest.raises(NodeNotFound):
            graph().find_path("F", "G")

    def test_end_node_not_in_graph_weight_between(self):
        with pytest.raises(NodeNotFound):
            graph().weight_between("A", "F")

    def test_start_node_not_in_graph_weight_between(self):
        with pytest.raises(NodeNotFound):
            graph().weight_between("F", "E")

    def test_both_nodes_not_in_graph_weight_between(self):
        with pytest.raises(NodeNotFound):
            graph().weight_between("F", "G")

    def test_invalid_path(self): 
        path = ["A", "E"]
        with pytest.raises(ValueError):
            graph().path_weight(path)
