"""
Tree implementations: Binary Tree, BST, and AVL Tree.
"""

from __future__ import annotations
from typing import Generic, TypeVar, Optional
import math

T = TypeVar("T")


class TreeNode(Generic[T]):
    """A node in a binary tree."""

    def __init__(self, value: T):
        self.value = value
        self.left: Optional[TreeNode[T]] = None
        self.right: Optional[TreeNode[T]] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.value!r})"


class BinaryTree(Generic[T]):
    """
    A general binary tree with common traversal methods.
    """

    def __init__(self, root_value: Optional[T] = None):
        self.root: Optional[TreeNode[T]] = TreeNode(root_value) if root_value is not None else None

    def insert_left(self, parent: TreeNode[T], value: T) -> TreeNode[T]:
        node = TreeNode(value)
        parent.left = node
        return node

    def insert_right(self, parent: TreeNode[T], value: T) -> TreeNode[T]:
        node = TreeNode(value)
        parent.right = node
        return node

    # -- traversals --------------------------------------------------------

    def inorder(self, node: Optional[TreeNode[T]]) -> list[T]:
        """Left → Root → Right"""
        if not node:
            return []
        return self.inorder(node.left) + [node.value] + self.inorder(node.right)

    def preorder(self, node: Optional[TreeNode[T]]) -> list[T]:
        """Root → Left → Right"""
        if not node:
            return []
        return [node.value] + self.preorder(node.left) + self.preorder(node.right)

    def postorder(self, node: Optional[TreeNode[T]]) -> list[T]:
        """Left → Right → Root"""
        if not node:
            return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.value]

    def level_order(self) -> list[T]:
        """BFS level-order traversal."""
        if not self.root:
            return []
        result: list[T] = []
        queue: list[TreeNode[T]] = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Optional[TreeNode[T]]) -> int:
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def size(self) -> int:
        return self._size(self.root)

    def _size(self, node: Optional[TreeNode[T]]) -> int:
        if not node:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)


class BST(BinaryTree[T]):
    """
    Binary Search Tree: left < parent < right.
    Average O(log n), worst O(n) for unbalanced inserts.
    """

    def __init__(self) -> None:
        self.root: Optional[TreeNode[T]] = None
        self._size: int = 0

    def insert(self, value: T) -> None:
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)
        self._size += 1

    def _insert(self, node: TreeNode[T], value: T) -> None:
        if value < node.value:  # type: ignore[operator]
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)

    def search(self, value: T) -> bool:
        return self._search(self.root, value)

    def _search(self, node: Optional[TreeNode[T]], value: T) -> bool:
        if not node:
            return False
        if value == node.value:
            return True
        return self._search(node.left if value < node.value else node.right, value)  # type: ignore[operator]

    def delete(self, value: T) -> bool:
        if not self.search(value):
            return False
        self.root = self._delete(self.root, value)
        self._size -= 1
        return True

    def _delete(self, node: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        if not node:
            return None
        if value < node.value:  # type: ignore[operator]
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # No children
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Two children: inorder successor
            current = node.right
            while current.left:
                current = current.left
            node.value = current.value
            node.right = self._delete(node.right, current.value)  # type: ignore[arg-type]
        return node

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: T) -> bool:
        return self.search(value)

    def _inorder(self, node: Optional[TreeNode[T]]) -> list[T]:
        if not node:
            return []
        return self._inorder(node.left) + [node.value] + self._inorder(node.right)

    def inorder(self, node: Optional[TreeNode[T]] = None) -> list[T]:
        """Override parent to accept optional node arg for convenience."""
        if node is None:
            return self._inorder(self.root)
        return self._inorder(node)

    def __repr__(self) -> str:
        return f"BST({self.inorder()!r})"


class AVLNode(TreeNode[T]):
    """BST node with balance factor tracking."""

    def __init__(self, value: T) -> None:
        TreeNode.__init__(self, value)
        self.height: int = 0


class AVLTree(BinaryTree[T]):
    """
    AVL Tree: self-balancing BST.
    Every node's left/right subtree heights differ by at most 1.
    All operations O(log n).
    """

    def __init__(self) -> None:
        self.root: Optional[AVLNode[T]] = None
        self._size: int = 0

    def insert(self, value: T) -> None:
        self.root = self._insert(self.root, value)
        self._size += 1

    def _insert(self, node: Optional[AVLNode[T]], value: T) -> AVLNode[T]:
        if not node:
            return AVLNode(value)
        if value < node.value:  # type: ignore[operator]
            node.left = self._insert(node.left, value)  # type: ignore[arg-type]
        elif value > node.value:
            node.right = self._insert(node.right, value)  # type: ignore[arg-type]
        else:
            return node  # duplicates not allowed

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))  # type: ignore[arg-type]
        return self._balance(node)

    def _balance(self, z: AVLNode[T]) -> AVLNode[T]:
        bf = self._get_height(z.left) - self._get_height(z.right)  # type: ignore[arg-type]

        # Left heavy
        if bf > 1:
            if self._get_height(z.left.left or AVLNode(None)) > self._get_height(z.left.right or AVLNode(None)):  # type: ignore[arg-type]
                return self._rotate_right(z)
            z.left = self._rotate_left(z.left)  # type: ignore[arg-type]
            return self._rotate_right(z)

        # Right heavy
        if bf < -1:
            if self._get_height(z.right.right or AVLNode(None)) > self._get_height(z.right.left or AVLNode(None)):  # type: ignore[arg-type]
                return self._rotate_left(z)
            z.right = self._rotate_right(z.right)  # type: ignore[arg-type]
            return self._rotate_left(z)

        return z

    def _rotate_right(self, z: AVLNode[T]) -> AVLNode[T]:
        y = z.left  # type: ignore[attr-defined]
        if y is None:
            return z
        t3 = y.right
        y.right = z
        z.left = t3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))  # type: ignore[arg-type]
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))  # type: ignore[arg-type]
        return y

    def _rotate_left(self, z: AVLNode[T]) -> AVLNode[T]:
        y = z.right
        if y is None:
            return z
        t2 = y.left
        y.left = z
        z.right = t2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))  # type: ignore[arg-type]
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))  # type: ignore[arg-type]
        return y

    @staticmethod
    def _get_height(node: Optional[AVLNode[T]]) -> int:
        return node.height if node else -1

    def search(self, value: T) -> bool:
        return self._search(self.root, value)

    def _search(self, node: Optional[AVLNode[T]], value: T) -> bool:
        if not node:
            return False
        if value == node.value:
            return True
        return self._search(node.left if value < node.value else node.right, value)  # type: ignore[operator]

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: T) -> bool:
        return self.search(value)

    def _inorder(self, node: Optional[AVLNode[T]]) -> list[T]:
        if not node:
            return []
        return self._inorder(node.left) + [node.value] + self._inorder(node.right)

    def inorder(self, node: Optional[AVLNode[T]] = None) -> list[T]:
        """Override parent to accept optional node arg for convenience."""
        if node is None:
            return self._inorder(self.root)
        return self._inorder(node)

    def __repr__(self) -> str:
        return f"AVLTree({self.inorder()!r})"
