# lazymap

A lazy mapping whose values are evaluated when accessed

## Installation

You can install this package with pip.
```sh
$ pip install lazymap
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/python-lazymap)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/python-lazymap.git)

[![PyPI - lazymap](https://img.shields.io/badge/PyPI-lazymap-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/lazymap/)

## Usage

A `LazyMap` is a mapping whose values can be evaluated only when they are accessed. This is useful when you need a mapping which might not need to evaluate all of its values, but it is unknown which values will be needed.

Not all values of a `LazyMap` need to be lazily evaluated. You can also store regular values in a `LazyMap`.

`LazyMap` also supports caching of values, so that they are only evaluated once, although this can be disabled on a per-object or per-key basis.

### Importing

```python
from lazymap import LazyMap
```

### Creating a LazyMap

You can initialize a `LazyMap` and provide it with initial static values, initial lazy values, a default factory function for missing keys, and any combination of the above. Additionally you can enable (default) or disable caching for the entire `LazyMap`.

If a default factory function is provided, it will be called with the key as an argument when a key is accessed which is not in the `LazyMap`.

```python
static = LazyMap({"a": 1, "b": 2})
lazy = LazyMap({"c": lambda: 3})
default = LazyMap(default=lambda key: key * 2)
uncached = LazyMap({"random": lambda: randint(0, 100)}, cache=False)
```

### Creating a LazyMap from keys and a function

You can initialize a `LazyMap` from a set of keys and a function which will be used to evaluate the value of each key. This way, the values are only evaluated when they are accessed.

You can also pass `allow_missing=True` to the `fromkeys` constructor to also use the function as a default factory function for missing keys.

```python
def expensive(key):
	print(f'Calculating value for key {key}...')
	return key * 2

from_keys = LazyMap.fromkeys((1, 2, 3), expensive)
```

### Adding values to a LazyMap

You can add **non-lazy** values to a `LazyMap` just like you would a dictionary.

```python
lazy_map = LazyMap()
lazy_map["a"] = 1 # not lazy
```

You can also add **lazy** values to a `LazyMap` with the `lazy` method.

```python
def get_b():
	print('Calculating value of x...')
	sleep(1)
	return 42

lazy_map.lazy("x", get_x) # lazy
print(lazy_map["x"]) # Calls get_x
```

### Caching values

By default, the lazy values of a `LazyMap` are only evaluated once. The value is then cached and returned on subsequent accesses.

You can also pass `cache=True` or `cache=False` when adding a lazy key with `lazy()` to override the default caching behaviour for that key.

```python
lazy_map = LazyMap()

def get_value():
	sleep(1)
	return randint(0, 100)

lazy_map.lazy("cached", get_value)
lazy_map.lazy("uncached", get_value, cache=False)

print(lazy_map["cached"]) # 42
print(lazy_map["cached"]) # 42
print(lazy_map["uncached"]) # 69
print(lazy_map["uncached"]) # 13
```