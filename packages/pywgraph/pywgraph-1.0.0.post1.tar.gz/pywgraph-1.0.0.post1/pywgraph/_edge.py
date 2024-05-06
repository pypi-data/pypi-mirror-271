from typing import TypeVar
from ._groups import Group

T = TypeVar("T")
_default_group = Group(
    "Real numbers with multiplication", 1.0, lambda x, y: x * y, lambda x: 1 / x
)


class DirectedEdge:

    def __init__(self, start: str, end: str) -> None:
        if start == end:
            raise ValueError("Start and end vertices must be different")
        self._start = start
        self._end = end

    @property
    def start(self) -> str:
        return self._start

    @property
    def end(self) -> str:
        return self._end

    @property
    def inverse(self) -> "DirectedEdge":
        return DirectedEdge(self._end, self._start)

    def __hash__(self) -> int:
        return hash((self._start, self._end))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DirectedEdge):
            return self._start == other.start and self._end == other.end
        return False

    def __iter__(self):
        yield self._start
        yield self._end

    def __repr__(self) -> str:
        return f"{self._start} -> {self._end}"


class WeightedDirectedEdge(DirectedEdge):

    def __init__(
        self, start: str, end: str, weight: T, group: Group = _default_group
    ) -> None:
        super().__init__(start, end)
        self._weight = weight
        self._group = group

    @property
    def weight(self) -> T:  # type: ignore
        return self._weight

    @property
    def group(self) -> Group:
        return self._group

    @property
    def inverse(self) -> "WeightedDirectedEdge":
        inverse_weight = self.group.inverse(self._weight)
        return WeightedDirectedEdge(self._end, self._start, inverse_weight, self.group)

    def __iter__(self):
        yield self._start
        yield self._end
        yield self._weight

    def __hash__(self) -> int:
        return hash((self._start, self._end)) ^ self.group._hash_function(self._weight)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, WeightedDirectedEdge):
            weight_equality = self.group._hash_function(
                self._weight
            ) == self.group._hash_function(other._weight)
            return super().__eq__(other) and weight_equality
        return False

    def __repr__(self) -> str:
        super_repr = super().__repr__()
        lines = str(self.weight).split("\n")
        first_line = lines[0]
        following_lines = lines[1:]
        if not following_lines:
            return f"{super_repr}: {first_line}"

        indented_following_lines = "\n".join(
            " " * len(super_repr + ": ") + line for line in following_lines
        )
        return f"{super_repr}: {first_line}\n{indented_following_lines}"


if __name__ == "__main__":
    edge = WeightedDirectedEdge("A", "B", 6)
    print(edge)
    print(edge.inverse)
