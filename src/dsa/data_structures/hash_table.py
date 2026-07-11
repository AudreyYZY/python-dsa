"""
Hash Table implementation using chaining for collision resolution.
"""

from __future__ import annotations
from typing import Any, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Bucket(Generic[K, V]):
    """A single bucket entry holding key-value pairs with the same hash."""

    def __init__(self) -> None:
        self.entries: list[tuple[K, V]] = []

    def find(self, key: K) -> tuple[list[tuple[K, V]], int]:
        """Return (bucket, index) for the key."""
        for i, (k, _) in enumerate(self.entries):
            if k == key:
                return self.entries, i
        return self.entries, -1

    def insert(self, key: K, value: V) -> None:
        entries, idx = self.find(key)
        if idx >= 0:
            entries[idx] = (key, value)
        else:
            entries.append((key, value))

    def delete(self, key: K) -> V | None:
        entries, idx = self.find(key)
        if idx >= 0:
            return entries.pop(idx)[1]
        return None


class HashTable(Generic[K, V]):
    """
    A hash table using separate chaining.

    Default load factor threshold is 0.75 — resizes when exceeded.
    """

    def __init__(self, capacity: int = 16) -> None:
        self._buckets: list[_Bucket[K, V]] = [_Bucket() for _ in range(capacity)]
        self._capacity: int = capacity
        self._size: int = 0

    def _hash(self, key: K) -> int:
        return hash(key) % self._capacity

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._buckets = [_Bucket() for _ in range(new_capacity)]
        self._capacity = new_capacity
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket.entries:
                self.insert(key, value)

    def insert(self, key: K, value: V) -> None:
        if self._size / self._capacity >= 0.75:
            self._resize(self._capacity * 2)
        idx = self._hash(key)
        self._buckets[idx].insert(key, value)
        self._size += 1

    def get(self, key: K, default: Any = None) -> V | Any:
        idx = self._hash(key)
        entries, _ = self._buckets[idx].find(key)
        for k, v in entries:
            if k == key:
                return v  # type: ignore[return-value]
        return default

    def delete(self, key: K) -> V | None:
        idx = self._hash(key)
        val = self._buckets[idx].delete(key)
        if val is not None:
            self._size -= 1
            # Shrink if load factor drops below 0.25
            if self._capacity > 16 and self._size / self._capacity < 0.25:
                self._resize(self._capacity // 2)
        return val

    def contains(self, key: K) -> bool:
        idx = self._hash(key)
        entries, _ = self._buckets[idx].find(key)
        return any(k == key for k, _ in entries)

    def __getitem__(self, key: K) -> V:
        val = self.get(key)
        if val is None and not self.contains(key):
            raise KeyError(key)
        return val  # type: ignore[return-value]

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        if self.delete(key) is None:
            raise KeyError(key)

    def keys(self) -> list[K]:
        result: list[K] = []
        for bucket in self._buckets:
            result.extend(k for k, _ in bucket.entries)
        return result

    def values(self) -> list[V]:
        result: list[V] = []
        for bucket in self._buckets:
            result.extend(v for _, v in bucket.entries)
        return result

    def items(self) -> list[tuple[K, V]]:
        result: list[tuple[K, V]] = []
        for bucket in self._buckets:
            result.extend(bucket.entries)
        return result

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def __repr__(self) -> str:
        return f"HashTable({dict(self.items())!r})"
