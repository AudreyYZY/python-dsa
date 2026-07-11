"""
Dynamic Programming algorithms.
"""

from __future__ import annotations
from typing import Optional


def fibonacci(n: int) -> int:
    """
    Fibonacci — O(n) iterative.
    Returns the nth Fibonacci number (F(0)=0, F(1)=1).
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_memo(n: int, memo: Optional[dict[int, int]] = None) -> int:
    """
    Fibonacci with memoization — O(n) time, O(n) space.
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def climb_stairs(n: int) -> int:
    """
    Climbing Stairs — O(n).
    You can take 1 or 2 steps at a time. How many distinct ways to reach the top?
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """
    0/1 Knapsack — O(n * W).
    Each item can be taken at most once.
    Returns maximum value achievable.
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp[n][capacity]


def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Longest Common Subsequence — O(m * n).
    Returns the length of the LCS.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def edit_distance(s1: str, s2: str) -> int:
    """
    Edit Distance (Levenshtein) — O(m * n).
    Minimum number of insertions, deletions, or substitutions.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


def coin_change(coins: list[int], amount: int) -> int:
    """
    Coin Change — O(amount * len(coins)).
    Returns the minimum number of coins needed. -1 if impossible.
    """
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


def longest_increasing_subsequence(nums: list[int]) -> int:
    """
    Longest Increasing Subsequence — O(n log n) with binary search.
    """
    if not nums:
        return 0
    tails: list[int] = []
    for num in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < num:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(num)
        else:
            tails[lo] = num
    return len(tails)


DP_ALGORITHMS = {
    "fibonacci": fibonacci,
    "fibonacci_memo": fibonacci_memo,
    "climb_stairs": climb_stairs,
    "knapsack_01": knapsack_01,
    "lcs": longest_common_subsequence,
    "edit_distance": edit_distance,
    "coin_change": coin_change,
    "lis": longest_increasing_subsequence,
}
