"""
Sorting algorithms.

Each function sorts a list in-place and returns it for convenience.
"""

from __future__ import annotations
import random
from typing import Protocol, TypeVar

T = TypeVar("T")


class Comparable(Protocol):
    def __lt__(self, other: object) -> bool: ...


def bubble_sort(arr: list[T]) -> list[T]:
    """
    Bubble Sort — O(n²) worst/average, O(n) best (already sorted).
    Stable sort. Simple but inefficient for large datasets.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: list[T]) -> list[T]:
    """
    Selection Sort — O(n²) always.
    Minimizes swaps (at most n). Not stable.
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr: list[T]) -> list[T]:
    """
    Insertion Sort — O(n²) worst, O(n) best.
    Stable and adaptive. Great for small/nearly-sorted arrays.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: list[T]) -> list[T]:
    """
    Merge Sort — O(n log n) guaranteed.
    Stable sort. Requires O(n) extra space.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[T], right: list[T]) -> list[T]:
    result: list[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list[T]) -> list[T]:
    """
    Quick Sort — O(n log n) average, O(n²) worst case.
    In-place sort. Not stable. Uses randomized pivot.
    """
    if len(arr) <= 1:
        return arr
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_helper(arr: list[T], low: int, high: int) -> None:
    if low < high:
        pivot_idx = _partition(arr, low, high)
        _quick_sort_helper(arr, low, pivot_idx - 1)
        _quick_sort_helper(arr, pivot_idx + 1, high)


def _partition(arr: list[T], low: int, high: int) -> int:
    # Randomized pivot to avoid O(n²) on sorted input
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def heap_sort(arr: list[T]) -> list[T]:
    """
    Heap Sort — O(n log n) guaranteed.
    In-place sort. Not stable.
    """
    n = len(arr)

    def heapify(size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(size, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)

    return arr


def counting_sort(arr: list[int]) -> list[int]:
    """
    Counting Sort — O(n + k) where k is the range of input.
    Stable sort. Only works on non-negative integers.
    """
    if not arr:
        return arr
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    count: list[int] = [0] * range_val
    output: list[int] = [0] * len(arr)

    for num in arr:
        count[num - min_val] += 1

    for i in range(1, range_val):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1

    return output


SORTING_ALGORITHMS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
    "counting": counting_sort,
}
