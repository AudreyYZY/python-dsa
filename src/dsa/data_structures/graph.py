"""
Graph implementation using adjacency list.
Supports directed and undirected graphs.
Includes BFS, DFS, Dijkstra's shortest path, and cycle detection.
"""

from __future__ import annotations
from typing import Generic, TypeVar
from collections import deque
import heapq

T = TypeVar("T")


class Graph(Generic[T]):
    """
    An adjacency-list graph.

    Parameters
    ----------
    directed : bool, default False
        If True, edges are one-way. Otherwise edges are bidirectional.
    """

    def __init__(self, directed: bool = False) -> None:
        self.adjacency: dict[T, list[T]] = {}
        self._directed = directed

    def add_vertex(self, vertex: T) -> None:
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def add_edge(self, src: T, dst: T) -> None:
        self.add_vertex(src)
        self.add_vertex(dst)
        self.adjacency[src].append(dst)
        if not self._directed:
            self.adjacency[dst].append(src)

    def remove_edge(self, src: T, dst: T) -> bool:
        if src in self.adjacency and dst in self.adjacency[src]:
            self.adjacency[src].remove(dst)
            if not self._directed:
                self.adjacency[dst].remove(src)
            return True
        return False

    def remove_vertex(self, vertex: T) -> None:
        if vertex not in self.adjacency:
            return
        # Remove all edges pointing to this vertex
        for other in self.adjacency:
            if vertex in self.adjacency[other]:
                self.adjacency[other].remove(vertex)
        del self.adjacency[vertex]

    def has_edge(self, src: T, dst: T) -> bool:
        return dst in self.adjacency.get(src, [])

    def neighbors(self, vertex: T) -> list[T]:
        return list(self.adjacency.get(vertex, []))

    def vertices(self) -> list[T]:
        return list(self.adjacency.keys())

    # -- traversals --------------------------------------------------------

    def bfs(self, start: T) -> list[T]:
        """Breadth-first search from *start*. Returns visitation order."""
        if start not in self.adjacency:
            return []
        visited: set[T] = {start}
        queue: deque[T] = deque([start])
        order: list[T] = []
        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self.adjacency[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: T) -> list[T]:
        """Depth-first search from *start* (iterative). Returns visitation order."""
        if start not in self.adjacency:
            return []
        visited: set[T] = set()
        stack: list[T] = [start]
        order: list[T] = []
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            order.append(vertex)
            for neighbor in reversed(self.adjacency[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)
        return order

    def dfs_recursive(self, start: T) -> list[T]:
        """Recursive DFS (use only for small graphs — limited by Python recursion depth)."""
        visited: set[T] = set()

        def _visit(v: T) -> None:
            visited.add(v)
            order.append(v)
            for neighbor in self.adjacency[v]:
                if neighbor not in visited:
                    _visit(neighbor)

        order: list[T] = []
        _visit(start)
        return order

    def has_cycle(self) -> bool:
        """Detect if the graph contains a cycle. O(V + E)."""
        visited: set[T] = set()
        rec_stack: set[T] = set()

        def _has_cycle_from(v: T, parent: T | None) -> bool:
            visited.add(v)
            rec_stack.add(v)
            for neighbor in self.adjacency[v]:
                if neighbor not in visited:
                    if _has_cycle_from(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True
            rec_stack.discard(v)
            return False

        for vertex in self.adjacency:
            if vertex not in visited:
                if _has_cycle_from(vertex, None):
                    return True
        return False

    def dijkstra(self, start: T) -> tuple[dict[T, float], dict[T, T | None]]:
        """
        Dijkstra's shortest path from *start*.
        Assumes unweighted graph (edge weight = 1).
        Returns (distances, predecessors).
        """
        distances: dict[T, float] = {v: float("inf") for v in self.adjacency}
        distances[start] = 0
        predecessors: dict[T, T | None] = {v: None for v in self.adjacency}
        pq: list[tuple[float, T]] = [(0, start)]

        while pq:
            dist_u, u = heapq.heappop(pq)
            if dist_u > distances[u]:
                continue
            for v in self.adjacency[u]:
                alt = dist_u + 1
                if alt < distances[v]:
                    distances[v] = alt
                    predecessors[v] = u
                    heapq.heappush(pq, (alt, v))

        return distances, predecessors

    def shortest_path(self, start: T, end: T) -> list[T] | None:
        """Return the shortest path from *start* to *end*, or None if unreachable."""
        distances, predecessors = self.dijkstra(start)
        if distances[end] == float("inf"):
            return None
        path: list[T] = []
        current: T | None = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        return path

    def __repr__(self) -> str:
        return f"Graph({self.adjacency!r}, directed={self._directed})"
