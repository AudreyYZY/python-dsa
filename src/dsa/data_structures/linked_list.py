"""
Linked List implementations.

Includes singly linked list, doubly linked list, and circular linked list.
Each node stores a value and a reference to the next node.
"""

from __future__ import annotations


class Node:
    """A single node in a linked list."""

    def __init__(self, value: int | float | str):
        self.value = value
        self.next: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class SinglyLinkedList:
    """
    A singly linked list where each node points only to the next node.

    Operations run in O(n) time except for head insertion which is O(1).
    """

    def __init__(self) -> None:
        self.head: Node | None = None
        self._size: int = 0

    # -- basic mutations ---------------------------------------------------

    def append(self, value: int | float | str) -> None:
        """Add a node at the tail — O(n)."""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, value: int | float | str) -> None:
        """Add a node at the head — O(1)."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def delete(self, value: int | float | str) -> bool:
        """
        Delete the first node whose value matches. Returns True if found.
        """
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    # -- lookup ------------------------------------------------------------

    def find(self, value: int | float | str) -> int:
        """Return the index of *value*, or -1 if not found."""
        idx = 0
        current = self.head
        while current:
            if current.value == value:
                return idx
            current = current.next
            idx += 1
        return -1

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: int | float | str) -> bool:
        return self.find(value) >= 0

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"SinglyLinkedList([{', '.join(repr(v) for v in self)}])"

    def reverse(self) -> None:
        """Reverse the list in-place — O(n)."""
        prev: Node | None = None
        current = self.head
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt
        self.head = prev


class _DoublyNode:
    """A node in a doubly linked list with prev pointer."""

    def __init__(self, value: int | float | str):
        self.value = value
        self.next: Node | None = None
        self.prev: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class DoublyLinkedList:
    """
    A doubly linked list where each node points to both next and previous nodes.
    Allows O(1) insert/delete at head and tail.
    """

    def __init__(self) -> None:
        self.head: _DoublyNode | None = None
        self.tail: _DoublyNode | None = None
        self._size: int = 0

    def append(self, value: int | float | str) -> None:
        """Add at tail — O(1)."""
        new_node = _DoublyNode(value)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, value: int | float | str) -> None:
        """Add at head — O(1)."""
        new_node = _DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def delete(self, value: int | float | str) -> bool:
        """Delete first matching node — O(n)."""
        current = self.head
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"DoublyLinkedList([{', '.join(repr(v) for v in self)}])"
