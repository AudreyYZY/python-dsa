"""
LeetCode problem solutions.
"""

from __future__ import annotations
from collections import Counter
from typing import Optional


class ListNode:
    """Node for singly-linked list problems."""

    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        self.val = val
        self.next = next


class Solution:
    """Collection of LeetCode solutions."""

    # ---- Two Sum (LC #1) ----
    @staticmethod
    def two_sum(nums: list[int], target: int) -> list[int]:
        """
        Given an array of integers, return indices of the two numbers that add up to target.
        Time: O(n), Space: O(n).
        """
        seen: dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

    # ---- Valid Parentheses (LC #20) ----
    @staticmethod
    def is_valid_parentheses(s: str) -> bool:
        """
        Check if a string of brackets is valid.
        Time: O(n), Space: O(n).
        """
        stack: list[str] = []
        mapping = {")": "(", "}": "{", "]": "["}
        for ch in s:
            if ch in mapping:
                if not stack or stack.pop() != mapping[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack

    # ---- Merge Two Sorted Lists (LC #21) ----
    @staticmethod
    def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """Merge two sorted linked lists. Time: O(n+m)."""
        dummy = ListNode()
        current = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        current.next = list1 or list2
        return dummy.next

    # ---- Maximum Subarray (LC #53) ----
    @staticmethod
    def max_sub_array(nums: list[int]) -> int:
        """
        Kadane's algorithm. Find contiguous subarray with largest sum.
        Time: O(n), Space: O(1).
        """
        max_sum = nums[0]
        current_sum = nums[0]
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        return max_sum

    # ---- Product of Array Except Self (LC #238) ----
    @staticmethod
    def product_except_self(nums: list[int]) -> list[int]:
        """
        Return answer[i] = product of all nums except nums[i].
        Time: O(n), Space: O(1) excluding output.
        """
        n = len(nums)
        result = [1] * n
        left = 1
        for i in range(n):
            result[i] *= left
            left *= nums[i]
        right = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right
            right *= nums[i]
        return result

    # ---- Longest Substring Without Repeating Characters (LC #3) ----
    @staticmethod
    def length_of_longest_substring(s: str) -> int:
        """Sliding window. Time: O(n), Space: O(min(n, m))."""
        char_index: dict[str, int] = {}
        left = 0
        max_len = 0
        for right, ch in enumerate(s):
            if ch in char_index and char_index[ch] >= left:
                left = char_index[ch] + 1
            char_index[ch] = right
            max_len = max(max_len, right - left + 1)
        return max_len

    # ---- Valid Anagram (LC #242) ----
    @staticmethod
    def is_anagram(s: str, t: str) -> bool:
        """Check if t is an anagram of s. Time: O(n)."""
        return Counter(s) == Counter(t)

    # ---- Palindrome Number (LC #9) ----
    @staticmethod
    def is_palindrome_number(x: int) -> bool:
        """Check if integer is a palindrome. Time: O(log n)."""
        if x < 0:
            return False
        if x < 10:
            return True
        reversed_half = 0
        original = x
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10
        return x == reversed_half or x == reversed_half // 10

    # ---- Roman to Integer (LC #13) ----
    @staticmethod
    def roman_to_integer(s: str) -> int:
        """Convert Roman numeral string to integer. Time: O(n)."""
        roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        result = 0
        prev_value = 0
        for ch in reversed(s):
            value = roman_values[ch]
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        return result

    # ---- Contains Duplicate (LC #217) ----
    @staticmethod
    def contains_duplicate(nums: list[int]) -> bool:
        """Check if array contains duplicates. Time: O(n)."""
        return len(set(nums)) != len(nums)

    # ---- Move Zeroes (LC #283) ----
    @staticmethod
    def move_zeroes(nums: list[int]) -> None:
        """Move all zeroes to the end in-place. Time: O(n)."""
        last_non_zero = 0
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[last_non_zero], nums[i] = nums[i], nums[last_non_zero]
                last_non_zero += 1

    # ---- Best Time to Buy and Sell Stock (LC #121) ----
    @staticmethod
    def max_profit(prices: list[int]) -> int:
        """Max profit from one buy/sell. Time: O(n)."""
        min_price = float("inf")
        max_profit_val = 0
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit_val:
                max_profit_val = price - min_price
        return max_profit_val

    # ---- Fizz Buzz (LC #412) ----
    @staticmethod
    def fizz_buzz(n: int) -> list[str]:
        """Return FizzBuzz from 1 to n. Time: O(n)."""
        result: list[str] = []
        for i in range(1, n + 1):
            if i % 15 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result
