"""
Searching algorithms.
"""

from __future__ import annotations
from typing import Generic, TypeVar

T = TypeVar("T")


def linear_search(arr: list[T], target: T) -> int:
    """
    Linear Search — O(n).
    Works on unsorted arrays. Returns index or -1.
    """
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def binary_search(arr: list[T], target: T) -> int:
    """
    Binary Search — O(log n).
    Requires a SORTED array. Returns index or -1.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binary_search_recursive(arr: list[T], target: T, left: int | None = None, right: int | None = None) -> int:
    """
    Recursive binary search — O(log n).
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    return binary_search_recursive(arr, target, left, mid - 1)


def lower_bound(arr: list[T], target: T) -> int:
    """
    Find the first position where target could be inserted (maintaining order).
    O(log n). Works on sorted arrays.
    """
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(arr: list[T], target: T) -> int:
    """
    Find the first position after the last occurrence of target.
    O(log n).
    """
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def find_first_occurrence(arr: list[T], target: T) -> int:
    """Find the index of the first occurrence of target in a sorted array."""
    idx = binary_search(arr, target)
    if idx == -1:
        return -1
    while idx > 0 and arr[idx - 1] == target:
        idx -= 1
    return idx


def find_last_occurrence(arr: list[T], target: T) -> int:
    """Find the index of the last occurrence of target in a sorted array."""
    idx = binary_search(arr, target)
    if idx == -1:
        return -1
    while idx < len(arr) - 1 and arr[idx + 1] == target:
        idx += 1
    return idx


SEARCHING_ALGORITHMS = {
    "linear": linear_search,
    "binary": binary_search,
    "binary_recursive": binary_search_recursive,
    "lower_bound": lower_bound,
    "upper_bound": upper_bound,
    "first_occurrence": find_first_occurrence,
    "last_occurrence": find_last_occurrence,
}
