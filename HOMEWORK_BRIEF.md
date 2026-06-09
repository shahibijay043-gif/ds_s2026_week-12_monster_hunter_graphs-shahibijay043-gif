# Week 12: Monster Hunter Graphs

## Due
**Sunday 2026-05-24, 23:59 KST**

## Story

The Hunter Guild has reports of monsters appearing across the city: vampires in the old theater, swamp things near the marsh, ghosts in the train station, and something deeply unpleasant under the library.

Your job is not to fight them yet.

Your job is to build the map.

Represent the monster activity network as a graph so the guild can understand:

- which locations are connected
- which routes exist in both directions
- which routes have danger scores
- which locations are major threat hubs
- which sightings should be handled first

## What You Will Build

You will complete graph helper functions in:

```text
src/challenges.py
```

You will test them with:

```text
tests/test_challenges.py
```

You will also complete the student README.

```text
README.md
```

## Required Problems

### Problem 1: Build the Hunter Map

Implement:

```python
def build_hunter_map(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Build an undirected adjacency list from route pairs."""
```

Given route pairs, return an undirected adjacency list.

Example:

```python
edges = [
    ("Old Theater", "Train Station"),
    ("Train Station", "Library Basement"),
]
```

Expected result:

```python
{
    "Old Theater": ["Train Station"],
    "Train Station": ["Old Theater", "Library Basement"],
    "Library Basement": ["Train Station"],
}
```

Rules:

- Each route works both directions.
- Include every location that appears in the input.
- Do not add duplicate neighbors if the same route appears more than once.
- Neighbor order does not matter for grading.

---

### Problem 2: Build the Weighted Hunter Map

Implement:

```python
def build_weighted_hunter_map(
    edges: list[tuple[str, str, int]]
) -> dict[str, dict[str, int]]:
    """Build an undirected weighted graph from route triples."""
```

The third value is a **danger score**.

Example:

```python
edges = [
    ("Old Theater", "Train Station", 4),
    ("Train Station", "Library Basement", 7),
]
```

Expected result:

```python
{
    "Old Theater": {"Train Station": 4},
    "Train Station": {"Old Theater": 4, "Library Basement": 7},
    "Library Basement": {"Train Station": 7},
}
```

Rules:

- Each route works both directions.
- Danger scores must be positive integers.
- If a danger score is `0` or negative, raise `ValueError`.
- If the same route appears more than once, keep the **lowest danger score**.

---

### Problem 3: Map Summary

Implement:

```python
def map_summary(graph: dict[str, list[str]]) -> dict[str, int]:
    """Return the number of locations and undirected routes."""
```

Example:

```python
graph = {
    "A": ["B", "C"],
    "B": ["A"],
    "C": ["A"],
}
```

Expected result:

```python
{"locations": 3, "routes": 2}
```

Rules:

- Count locations using the number of keys.
- Count undirected routes only once.
- An empty graph should return `{"locations": 0, "routes": 0}`.

---

### Problem 4: Most Connected Location

Implement:

```python
def most_connected_location(graph: dict[str, list[str]]) -> str | None:
    """Return the location with the most neighbors."""
```

Rules:

- Return `None` for an empty graph.
- If there is a tie, return the alphabetically first location.

Example:

```python
graph = {
    "Old Theater": ["Train Station"],
    "Train Station": ["Old Theater", "Library Basement"],
    "Library Basement": ["Train Station"],
}
```

Expected result:

```python
"Train Station"
```

---

## Stretch Problem: Priority Hunt Order

Implement:

```python
def priority_hunt_order(reports: list[tuple[int, str]]) -> list[str]:
    """Return monster sighting locations from most urgent to least urgent."""
```

Rules:

- Lower priority number means more urgent.
- Use `heapq`.
- If priorities tie, alphabetical order is acceptable.

Example:

```python
reports = [
    (3, "Old Theater"),
    (1, "Library Basement"),
    (2, "Train Station"),
]
```

Expected result:

```python
["Library Basement", "Train Station", "Old Theater"]
```

## Requirements

- Python 3.11+
- Standard library only
- Use type hints on public functions
- Public functions must have docstrings
- Run tests with:

```bash
pytest -q
```

## README Requirements

Your `README.md` must include:

- Summary
- Approach
- Complexity
- Edge-case checklist
- Assistance & Sources

## Standards Evidence

This assignment provides evidence for:

- **S1:** Python + Testing Fundamentals
- **S3:** Big-O Reasoning
- **S11:** Heaps + Priority Queue
- **S12:** Graphs + BFS/DFS + Dijkstra preparation
- **E5:** Space Complexity + Tradeoffs, optional
- **E6:** Optimization Techniques, optional
