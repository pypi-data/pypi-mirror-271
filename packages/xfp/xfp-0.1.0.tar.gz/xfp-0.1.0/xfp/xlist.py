from typing import List, Tuple, Iterable, Iterator, Self, Callable

# from collections import UserList
from copy import deepcopy


class Xlist:  # Xlist(UserList):

    def __init__(self, iterable: Iterable) -> None:

        match iterable:
            case list():
                self.data = self._convert_list(iterable)
            case tuple():
                self.data = self._convert_tuple(iterable)
            case object(__iter__=_):
                self.data = self._convert_iterator(iterable)
            case _:
                raise TypeError(
                    f"Xlist constructed from Iterator, provided : {type(iterable)}"
                )

    @classmethod
    def _convert_list(cls, list: List) -> List:
        return deepcopy(list)

    @classmethod
    def _convert_tuple(cls, tuple: Tuple) -> List:
        return deepcopy(list(tuple))

    @classmethod
    def _convert_iterator(cls, iterator: Iterator) -> List:
        return list(iterator)

    def __eq__(self, other: object) -> bool:
        return self.data == other.data

    def map(self, f: Callable) -> Self:
        return Xlist([f(el) for el in self.data])

    def flatten(self) -> Self:
        return Xlist([inner for outer in self.data for inner in outer])

    def flatMap(self, f: Callable) -> Self:
        return Xlist([i for el in map(f, self.data) for i in el])

    def filter(self, predicate: Callable) -> Self:
        return Xlist([el for el in self.data if predicate(el)])

    def sorted(self, key: None = None, reverse: bool = False) -> Self:
        return Xlist(sorted(self.data, key=key, reverse=reverse))

    def foreach(self, statement: Callable) -> None:
        for el in self.data:
            statement(el)

    def min(self, key: None = None):
        return min(self.data, key=key)

    def max(self, key: None = None):
        return max(self.data, key=key)
