from pywgraph import WeightedDirectedGraph, Group, WeightedDirectedEdge
import numpy as np
from typing import Any  # for typing purposes


def vector_group_multiplication() -> Group:
    group = Group(
        name="Vectors of dimension 2 with multiplication",
        identity=np.ones(2),
        operation=lambda x, y: x * y,
        inverse_function=lambda x: 1 / x,
        hash_function=lambda x: hash(tuple(x)),
    )
    return group


def vector_group_addition() -> Group:
    group = Group(
        name="Vectors of dimension 2 with addition",
        identity=np.zeros(2),
        operation=lambda x, y: x + y,
        inverse_function=lambda x: -x,
        hash_function=lambda x: hash(tuple(x)),
    )
    return group


_array_dict_graph: dict[str, dict[str, Any]] = {
    "A": {
        "B": np.array([1, 2]),
        "C": np.array([3, 4]),
    },
    "B": {
        "C": np.array([-5, 1.3]),
        "D": np.array([2, 1]),
    },
    "C": {
        "D": np.array([-1, 1]),
    },
    "D": {},
    "Z": {},
}


def multiplication_graph() -> WeightedDirectedGraph:
    graph = WeightedDirectedGraph.from_dict(
        _array_dict_graph, vector_group_multiplication()
    )
    return graph


def addition_graph() -> WeightedDirectedGraph:
    graph = WeightedDirectedGraph.from_dict(_array_dict_graph, vector_group_addition())
    return graph


class TestWeightedDirectedGraphArrays:
    # region MultiplicativeGroup
    def test_nodes(self):
        assert multiplication_graph().nodes == {"A", "B", "C", "D", "Z"}

    def test_edges(self):
        assert multiplication_graph().edges == {
            WeightedDirectedEdge(
                "A", "B", np.array([1, 2]), vector_group_multiplication()
            ),
            WeightedDirectedEdge(
                "A", "C", np.array([3, 4]), vector_group_multiplication()
            ),
            WeightedDirectedEdge(
                "B", "C", np.array([-5, 1.3]), vector_group_multiplication()
            ),
            WeightedDirectedEdge(
                "B", "D", np.array([2, 1]), vector_group_multiplication()
            ),
            WeightedDirectedEdge(
                "C", "D", np.array([-1, 1]), vector_group_multiplication()
            ),
        }

    def test_well_defined(self):
        assert multiplication_graph().check_definition()

    def test_fill_reverse_edge_multiplication(self):
        complete_dict = _array_dict_graph.copy()
        complete_dict["B"] = complete_dict["B"] | {"A": np.array([1, 1 / 2])}
        complete_dict["C"] = complete_dict["C"] | {
            "A": np.array([1 / 3, 1 / 4]),
            "B": np.array([-1 / 5, 1 / 1.3]),
        }
        complete_dict["D"] = complete_dict["D"] | {
            "B": np.array([1 / 2, 1 / 1]),
            "C": np.array([-1, 1 / 1]),
        }
        filled_graph = WeightedDirectedGraph.from_dict(
            complete_dict, vector_group_multiplication()
        )
        assert filled_graph == multiplication_graph().add_reverse_edges()

    def test_fill_reverse_edge_addition(self):
        complete_dict = _array_dict_graph.copy()
        complete_dict["B"] = complete_dict["B"] | {"A": np.array([-1, -2])}
        complete_dict["C"] = complete_dict["C"] | {
            "A": np.array([-3, -4]),
            "B": np.array([5, -1.3]),
        }
        complete_dict["D"] = complete_dict["D"] | {
            "B": np.array([-2, -1]),
            "C": np.array([1, -1]),
        }
        filled_graph = WeightedDirectedGraph.from_dict(
            complete_dict, vector_group_addition()
        )
        print(filled_graph)
        print(addition_graph().add_reverse_edges())
        assert filled_graph == addition_graph().add_reverse_edges()
