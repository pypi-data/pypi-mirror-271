"""
base
===============================================================================
"""
from __future__ import annotations

from collections.abc import Set as AbstractSet
from typing import Any, TYPE_CHECKING, Union

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

if TYPE_CHECKING:
    from pathlib import Path


class BaseReperoire(set):
    itemtype = Any

    def __and__(self, other: AbstractSet) -> Self:
        return self.__class__(set(self) & other)

    def __or__(self, other: AbstractSet) -> Self:
        return self.__class__(set(self) | other)

    def __sub__(self, other: AbstractSet) -> Self:
        return self.__class__(set(self) - other)

    def __xor__(self, other: AbstractSet) -> Self:
        return self.__class__(set(self) ^ other)

    def __iand__(self, other: AbstractSet) -> Self:
        _other = set(other)
        self._check_type_squence(_other)
        return super().__iand__(_other)

    def __ior__(self, other: AbstractSet) -> Self:
        _other = set(other)
        self._check_type_squence(_other)
        return super().__ior__(_other)

    def __isub__(self, other: AbstractSet) -> Self:
        _other = set(other)
        self._check_type_squence(_other)
        return super().__isub__(_other)

    def __ixor__(self, other: AbstractSet) -> Self:
        _other = set(other)
        self._check_type_squence(_other)
        return super().__ixor__(_other)

    def _check_type_squence(self, iterable:set):
        if not all(isinstance(i, self.itemtype) for i in iterable):
            raise TypeError(f"expected sequence of type {self.itemtype}")

    def add(self, elem):
        if not isinstance(elem, self.itemtype):
            raise TypeError(f"expected {self.itemtype}, got {type(elem)}")
        super().add(elem)

    def union(self, *others: AbstractSet) -> Self:
        result = self.__class__(super().union(*others))
        self._check_type_squence(result)
        return result

    def update(self, values):
        _values = set(values)
        self._check_type_squence(_values)
        super().update(_values)

    def open(self, path: Union[str, Path]) -> None:
        raise NotImplementedError

    @property
    def as_set(self) -> set:
        return set(self)

    @classmethod
    def fromFile(cls, path: Union[str, Path]) -> Self:
        result = cls()
        result.open(path)
        return result
