"""
.. include:: ../README.md
"""

import importlib.metadata as metadata
from collections import defaultdict
from functools import partial
from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    TypeVar,
)

from typing_extensions import Self

__all__ = ("LazyMap", "__version__")

__version__ = metadata.version(__package__ or __name__)


K = TypeVar("K")
V = TypeVar("V")


class LazyMap(Generic[K, V], MutableMapping[K, V]):
    """A mapping that lazily computes values on demand.

    Args:
        data: Initial data to populate the map. If a mutable mapping is provided, it will be used directly, otherwise it will be converted to a dictionary.
        lazy: Initial getters to populate the map. This is a mapping of keys to functions that take no arguments and return the value for the key. If a mutable mapping is provided, it will be used directly, otherwise it will be converted to a dictionary.
        default: A callable that takes a key and returns a default value for that key. If a default factory is not provided, a KeyError will be raised for missing keys.
        cache: Whether to cache the results of lazy evaluations by default.
    """

    def __init__(
        self,
        data: Optional[Mapping[K, V]] = None,
        *,
        lazy: Optional[Mapping[K, Callable[[], V]]] = None,
        default: Optional[Callable[[K], V]] = None,
        cache: bool = True,
    ) -> None:
        self._data = _make_mutable(data)
        self._lazy = _make_mutable(lazy)
        self._default = default
        self._cache: MutableMapping[K, bool] = defaultdict(lambda: cache)

    @classmethod
    def fromkeys(
        cls,
        keys: Iterable[K],
        getter: Callable[[K], V],
        *,
        cache: bool = True,
        allow_missing: bool = False,
    ) -> Self:
        """Create a new LazyMap with the given keys and getter.

        Args:
            keys: The keys to populate the map with.
            getter: A function that takes a key and returns the value for that key.
            cache: Whether to cache the results of the getter.
            allow_missing: Whether to allow using the getter for unknown keys.
        """
        return cls(
            lazy={key: partial(getter, key) for key in keys},
            default=getter if allow_missing else None,
            cache=cache,
        )

    def lazy(
        self, key: K, getter: Callable[[], V], cache: Optional[bool] = None
    ) -> None:
        """Set a lazy value.

        Args:
            key: The key for the value.
            getter: A function that takes no arguments and returns the value.
            cache: Whether to cache the result of the getter for this key.
        """
        self._lazy[key] = getter
        self._data.pop(key, None)
        self._cache.pop(key, None)
        if cache is not None:
            self._cache[key] = cache

    def __getitem__(self, key: K) -> V:
        try:
            return self._data[key]
        except KeyError:
            pass
        value = self._getter_of(key)()
        if self._cache[key]:
            self[key] = value
        return value

    def __setitem__(self, key: K, value: V) -> None:
        self._data[key] = value
        self._lazy.pop(key, None)
        self._cache.pop(key, None)

    def __delitem__(self, key: K) -> None:
        if key not in self:
            raise KeyError(key)
        self._data.pop(key, None)
        self._lazy.pop(key, None)
        self._cache.pop(key, None)

    def __iter__(self) -> Iterator[K]:
        return iter((*self._data, *self._lazy))

    def __len__(self) -> int:
        return len(self._data) + len(self._lazy)

    def __contains__(self, key: object) -> bool:
        return key in self._data or key in self._lazy

    def __repr__(self) -> str:
        items = ", ".join(f"{k!r}: {self._data.get(k, '<lazy>')}" for k in self)
        return f"{type(self).__name__}({{{items}}})"

    def __str__(self) -> str:
        return f"{type(self).__name__}({{{', '.join(f'{k!r}: {v!r}' for k, v in self.items())}}})"

    def _getter_of(self, key: K) -> Callable[[], V]:
        try:
            return self._lazy[key]
        except KeyError:
            pass
        if self._default is None:
            raise KeyError(key) from None
        return partial(self._default, key)


def _make_mutable(mapping: Optional[Mapping[K, V]]) -> MutableMapping[K, V]:
    if mapping is None:
        return {}
    if isinstance(mapping, MutableMapping):
        return mapping
    return dict(mapping)
