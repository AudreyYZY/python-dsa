"""
Greedy algorithms.
"""

from __future__ import annotations
import heapq
from collections import Counter


def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Activity Selection — O(n log n).
    Given (start, end) times, select the maximum number of non-overlapping activities.
    Greedy choice: pick the activity that finishes earliest.
    """
    if not activities:
        return []
    # Sort by finish time
    sorted_acts = sorted(activities, key=lambda x: x[1])
    selected = [sorted_acts[0]]
    for start, end in sorted_acts[1:]:
        if start >= selected[-1][1]:
            selected.append((start, end))
    return selected


def fractional_knapsack(items: list[tuple[float, float, float]], capacity: float) -> float:
    """
    Fractional Knapsack — O(n log n).
    Items are (weight, value, name). Take fractions of items.
    Greedy: pick items with highest value/weight ratio first.
    Returns total value achieved.
    """
    # Calculate value-to-weight ratio
    ratios = [(v / w, i, w, v, name) for i, (w, v, name) in enumerate(items)]
    ratios.sort(reverse=True)

    total_value = 0.0
    remaining = capacity

    for ratio, i, w, v, name in ratios:
        if remaining <= 0:
            break
        take = min(w, remaining)
        total_value += take * (v / w)
        remaining -= take

    return total_value


def huffman_encoding(text: str) -> dict[str, tuple[str, float]]:
    """
    Huffman Encoding — O(n log n).
    Builds a prefix-free code for characters in *text*.
    Returns dict mapping char → (code, frequency).
    """
    freq = Counter(text)
    if len(freq) == 1:
        char = next(iter(freq))
        return {char: ("1", freq[char] / len(text))}

    heap: list[tuple[float, int, str]] = [(f, i, c) for i, (c, f) in enumerate(freq.items())]
    heapq.heapify(heap)
    counter = len(freq)

    while len(heap) > 1:
        f1, i1, s1 = heapq.heappop(heap)
        f2, i2, s2 = heapq.heappop(heap)
        merged = f1 + f2
        heapq.heappush(heap, (merged, counter, s1 + "$" + s2))
        counter += 1

    # Decode the tree
    codebook: dict[str, str] = {}

    def decode(node: str, code: str) -> None:
        if len(node) == 1 and node != "$":
            codebook[node] = code
        else:
            parts = node.split("$", 1)
            if len(parts) == 2:
                decode(parts[0], code + "0")
                decode(parts[1], code + "1")

    if heap:
        decode(heap[0][2], "")

    return {ch: (codebook[ch], freq[ch] / len(text)) for ch in freq}


def jump_game(nums: list[int]) -> bool:
    """
    Jump Game — O(n).
    Can you reach the last index starting from index 0?
    Greedy: track the farthest reachable index.
    """
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
        if max_reach >= len(nums) - 1:
            return True
    return False


GREEDY_ALGORITHMS = {
    "activity_selection": activity_selection,
    "fractional_knapsack": fractional_knapsack,
    "huffman_encoding": huffman_encoding,
    "jump_game": jump_game,
}
