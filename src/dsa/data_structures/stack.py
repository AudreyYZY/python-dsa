"""
Stack and Queue implementations.

Stack: LIFO (Last In, First Out)
Queue: FIFO (First In, First Out)
"""

from __future__ import annotations
from typing import TypeVar
import heapq
from collections import deque

T = TypeVar("T")


class Stack:
    """
    A simple stack backed by a Python list.

    All operations are O(1) amortized.
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Push an item onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class MinStack(Stack):
    """
    A stack that supports O(1) retrieval of the minimum element.

    Uses an auxiliary stack to track the running minimum.
    """

    def __init__(self) -> None:
        super().__init__()
        self._min_stack: list[T] = []

    def push(self, item: T) -> None:
        super().push(item)
        if not self._min_stack or item <= self._min_stack[-1]:  # type: ignore[comparison-overlap]
            self._min_stack.append(item)

    def pop(self) -> T:
        item = super().pop()
        if item == self._min_stack[-1]:  # type: ignore[comparison-overlap,index]
            self._min_stack.pop()
        return item

    def get_min(self) -> T:
        """Return the minimum element in O(1)."""
        if not self._min_stack:
            raise IndexError("get_min from empty stack")
        return self._min_stack[-1]  # type: ignore[index]


class Queue:
    """
    A FIFO queue backed by collections.deque for O(1) operations.
    """

    def __init__(self) -> None:
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self) -> T:
        """Remove and return the front item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self) -> T:
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({list(self._items)!r})"


class Deque(Queue):
    """
    A double-ended queue supporting insert/remove from both ends.
    """

    def append_left(self, item: T) -> None:
        """Add to the front."""
        self._items.appendleft(item)

    def append_right(self, item: T) -> None:
        """Add to the back."""
        self._items.append(item)

    def pop_left(self) -> T:
        """Remove from the front."""
        if self.is_empty():
            raise IndexError("pop_left from empty deque")
        return self._items.popleft()

    def pop_right(self) -> T:
        """Remove from the back."""
        if self.is_empty():
            raise IndexError("pop_right from empty deque")
        return self._items.pop()


class PriorityQueue:
    """
    A min-heap based priority queue. Lower values = higher priority.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, T]] = []
        self._counter: int = 0  # tie-breaker for equal priorities

    def push(self, item: T, priority: int = 0) -> None:
        """Push with optional priority (default 0)."""
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> T:
        """Pop highest-priority (lowest number) item."""
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._heap)[2]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    def __repr__(self) -> str:
        return f"PriorityQueue({[(p, i, v) for p, i, v in self._heap]!r})"
