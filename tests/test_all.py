"""
Unit tests for data structures and algorithms.
"""

from __future__ import annotations
import sys
import os
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dsa.data_structures.linked_list import SinglyLinkedList, DoublyLinkedList
from dsa.data_structures.stack import Stack, MinStack, Queue, PriorityQueue
from dsa.data_structures.hash_table import HashTable
from dsa.data_structures.tree import BST, AVLTree, BinaryTree
from dsa.data_structures.graph import Graph
from dsa.algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    counting_sort,
)
from dsa.algorithms.searching import binary_search, linear_search
from dsa.algorithms.dynamic_programming import (
    fibonacci,
    knapsack_01,
    edit_distance,
    longest_increasing_subsequence,
)
from dsa.algorithms.greedy import activity_selection, jump_game
from dsa.leetcode import Solution


class TestSinglyLinkedList(unittest.TestCase):
    def test_append_and_iterate(self):
        ll = SinglyLinkedList()
        for v in [3, 1, 4, 1, 5]:
            ll.append(v)
        self.assertEqual(len(ll), 5)
        self.assertEqual(list(ll), [3, 1, 4, 1, 5])

    def test_prepend(self):
        ll = SinglyLinkedList()
        ll.prepend(3)
        ll.prepend(2)
        ll.prepend(1)
        self.assertEqual(list(ll), [1, 2, 3])

    def test_delete(self):
        ll = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        self.assertTrue(ll.delete(2))
        self.assertEqual(list(ll), [1, 3])
        self.assertFalse(ll.delete(99))

    def test_reverse(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3, 4]:
            ll.append(v)
        ll.reverse()
        self.assertEqual(list(ll), [4, 3, 2, 1])

    def test_find(self):
        ll = SinglyLinkedList()
        ll.append(10)
        ll.append(20)
        self.assertEqual(ll.find(10), 0)
        self.assertEqual(ll.find(20), 1)
        self.assertEqual(ll.find(99), -1)


class TestStackAndQueue(unittest.TestCase):
    def test_stack(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(len(s), 2)

    def test_min_stack(self):
        ms = MinStack()
        ms.push(5)
        ms.push(3)
        ms.push(7)
        self.assertEqual(ms.get_min(), 3)
        ms.pop()
        self.assertEqual(ms.get_min(), 3)
        ms.pop()
        self.assertEqual(ms.get_min(), 5)

    def test_queue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.peek(), 2)

    def test_priority_queue(self):
        pq = PriorityQueue()
        pq.push("low", priority=3)
        pq.push("high", priority=1)
        pq.push("medium", priority=2)
        self.assertEqual(pq.pop(), "high")
        self.assertEqual(pq.pop(), "medium")


class TestHashTable(unittest.TestCase):
    def test_insert_get(self):
        ht = HashTable()
        ht["name"] = "Alice"
        ht["age"] = 30
        self.assertEqual(ht["name"], "Alice")
        self.assertEqual(ht["age"], 30)

    def test_delete(self):
        ht = HashTable()
        ht["x"] = 1
        del ht["x"]
        self.assertNotIn("x", ht)

    def test_contains(self):
        ht = HashTable()
        ht["key"] = "val"
        self.assertIn("key", ht)
        self.assertNotIn("missing", ht)


class TestBST(unittest.TestCase):
    def test_insert_search(self):
        bst = BST()
        for v in [5, 3, 7, 1, 4, 6, 8]:
            bst.insert(v)
        for v in [1, 3, 4, 5, 6, 7, 8]:
            self.assertIn(v, bst)
        self.assertNotIn(99, bst)

    def test_delete(self):
        bst = BST()
        for v in [5, 3, 7, 1, 4]:
            bst.insert(v)
        bst.delete(3)
        self.assertNotIn(3, bst)
        self.assertEqual(len(bst), 4)

    def test_inorder_sorted(self):
        bst = BST()
        for v in [5, 3, 7, 1, 4]:
            bst.insert(v)
        self.assertEqual(bst.inorder(), [1, 3, 4, 5, 7])


class TestAVLTree(unittest.TestCase):
    def test_balance(self):
        avl = AVLTree()
        for v in [1, 2, 3, 4, 5, 6, 7]:
            avl.insert(v)
        self.assertEqual(len(avl), 7)
        self.assertEqual(avl.inorder(), [1, 2, 3, 4, 5, 6, 7])

    def test_search(self):
        avl = AVLTree()
        avl.insert(10)
        avl.insert(5)
        avl.insert(15)
        self.assertIn(10, avl)
        self.assertNotIn(99, avl)


class TestGraph(unittest.TestCase):
    def test_bfs(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        result = g.bfs("A")
        self.assertEqual(result[0], "A")
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_dfs(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        result = g.dfs("A")
        self.assertEqual(result[0], "A")

    def test_shortest_path(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("A", "D")
        g.add_edge("D", "C")
        path = g.shortest_path("A", "C")
        self.assertIsNotNone(path)
        self.assertEqual(path, ["A", "B", "C"])

    def test_has_cycle_directed(self):
        g = Graph(directed=True)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        self.assertTrue(g.has_cycle())

    def test_no_cycle_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        self.assertFalse(g.has_cycle())


class TestSorting(unittest.TestCase):
    def _test_sort(self, fn):
        self.assertEqual(fn([3, 1, 4, 1, 5, 9, 2, 6]), [1, 1, 2, 3, 4, 5, 6, 9])
        self.assertEqual(fn([]), [])
        self.assertEqual(fn([1]), [1])
        self.assertEqual(fn([2, 2, 2]), [2, 2, 2])

    def test_bubble_sort(self):
        self._test_sort(bubble_sort)

    def test_selection_sort(self):
        self._test_sort(selection_sort)

    def test_insertion_sort(self):
        self._test_sort(insertion_sort)

    def test_merge_sort(self):
        self._test_sort(merge_sort)

    def test_quick_sort(self):
        self._test_sort(quick_sort)

    def test_heap_sort(self):
        self._test_sort(heap_sort)

    def test_counting_sort(self):
        self.assertEqual(counting_sort([4, 2, 2, 8, 3, 3, 1]), [1, 2, 2, 3, 3, 4, 8])


class TestSearching(unittest.TestCase):
    def test_binary_search(self):
        arr = [1, 3, 5, 7, 9, 11, 13]
        self.assertEqual(binary_search(arr, 7), 3)
        self.assertEqual(binary_search(arr, 1), 0)
        self.assertEqual(binary_search(arr, 13), 6)
        self.assertEqual(binary_search(arr, 4), -1)

    def test_linear_search(self):
        arr = ["apple", "banana", "cherry"]
        self.assertEqual(linear_search(arr, "banana"), 1)
        self.assertEqual(linear_search(arr, "grape"), -1)


class TestDynamicProgramming(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(10), 55)

    def test_knapsack(self):
        weights = [1, 3, 4]
        values = [15, 20, 30]
        self.assertEqual(knapsack_01(weights, values, 5), 45)

    def test_edit_distance(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)

    def test_lis(self):
        self.assertEqual(longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]), 4)


class TestGreedy(unittest.TestCase):
    def test_activity_selection(self):
        acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
        result = activity_selection(acts)
        self.assertGreaterEqual(len(result), 4)

    def test_jump_game(self):
        self.assertTrue(jump_game([2, 3, 1, 1, 4]))
        self.assertFalse(jump_game([3, 2, 1, 0, 4]))


class TestLeetCode(unittest.TestCase):
    def test_two_sum(self):
        self.assertEqual(Solution.two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_valid_parentheses(self):
        self.assertTrue(Solution.is_valid_parentheses("()[]{}"))
        self.assertFalse(Solution.is_valid_parentheses("(]"))

    def test_max_sub_array(self):
        self.assertEqual(Solution.max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_product_except_self(self):
        self.assertEqual(Solution.product_except_self([1, 2, 3, 4]), [24, 12, 8, 6])

    def test_length_of_longest_substring(self):
        self.assertEqual(Solution.length_of_longest_substring("abcabcbb"), 3)

    def test_max_profit(self):
        self.assertEqual(Solution.max_profit([7, 1, 5, 3, 6, 4]), 5)

    def test_is_anagram(self):
        self.assertTrue(Solution.is_anagram("listen", "silent"))
        self.assertFalse(Solution.is_anagram("hello", "bello"))

    def test_roman_to_integer(self):
        self.assertEqual(Solution.roman_to_integer("III"), 3)
        self.assertEqual(Solution.roman_to_integer("IV"), 4)
        self.assertEqual(Solution.roman_to_integer("MCMXCIV"), 1994)


if __name__ == "__main__":
    unittest.main()
