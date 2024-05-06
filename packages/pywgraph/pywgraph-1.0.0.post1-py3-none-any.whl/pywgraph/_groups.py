from typing import Callable, TypeVar


"""Since I don't find an easy way of providing a way to indicate the elements of the 
group due to the limitations in type hinting in python, the class Group do not have
an attribute for the elements. Instead, it is initialize with a name, neutral element and 
a binary operator, this is, a callable. Is up to the user to ensure that the operation 
and the neutral element are compatible with the group."""

T = TypeVar("T")


class Group:
    def __init__(
        self,
        name: str,
        identity: T,
        operation: Callable[[T, T], T],
        inverse_function: Callable[[T], T],
        hash_function: Callable[[T], int] = hash,
    ) -> None:
        """Abstraction of a mathematical group.

        Parameters
        ----------
        name : str
            Name of the group. Just a brief description.
        identity : T
            Identity element of the group.
        operation : Callable[[T, T], T]
            Binary operator of the group.
        inverse : Callable[[T], T]
            Function that returns the inverse of an element.
        hash_function : Callable[[T], int], optional
            Function that returns the hash of an element, by default hash. Mandatory
            if elements of the group are not hashable.

        Examples
        --------
        Real numbers with multiplication:
        reals_mult = Group(
            name="Real numbers under multiplication",
            identity=1.0,
            operation=lambda x, y: x * y,
            inverse=lambda x: 1 / x
        )"""

        self._name = name
        self._identity = identity
        self._operation = operation
        self._inverse_function = inverse_function
        self._hash_function = hash_function

    @property
    def name(self) -> str:
        return self._name

    @property
    def identity(self) -> T:  # type: ignore
        return self._identity

    @property
    def operation(self) -> Callable[[T, T], T]:
        return self._operation

    @property
    def inverse_function(self) -> Callable[[T], T]:
        return self._inverse_function

    @property
    def hash_function(self) -> Callable[[T], int]:
        return self._hash_function

    def inverse(self, element: T) -> T:
        return self.inverse_function(element)

    def equal(self, a: T, b: T) -> bool:
        return self._hash_function(a) == self._hash_function(b)

    def __call__(self, a: T, b: T) -> T:
        return self.operation(a, b)

    def __repr__(self) -> str:
        return self.name


if __name__ == "__main__":
    reals_prod = Group(
        "Real numbers with product", 1.0, lambda x, y: x * y, lambda x: 1 / x
    )
    print(reals_prod(2, 3))

    reals_sum = Group("Real numbers with sum", 0.0, lambda x, y: x + y, lambda x: -x)
    print(reals_sum(2, 3))

    import numpy as np

    reals_3 = Group(
        "R^3 space",
        np.zeros(3),
        lambda x, y: x + y,
        lambda x: -x,
        lambda x: hash(tuple(x)),
    )
    print(reals_3(np.array([1, 2, 3]), np.array([4, 5, 6])))
    print(reals_3.inverse(np.array([1, 1, 1])))
    print(reals_3.equal(np.array([1, 2, 3]), np.array([1.0, 2, 3])))
