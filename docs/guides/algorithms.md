# Algorithm Animations

Animora provides educational algorithm visualizations (`animora.algorithms`) driven by real execution logic and explicit `OperationTrace` recordings.

---

## 1. Supported Algorithms

- **Binary Search**: `binary_search(arr, target)` — $O(\log N)$ interval comparison tracing.
- **Sorting Algorithms** (Visually Distinguishable):
  - `bubble_sort(arr)` — Adjacent pair compares & swaps.
  - `selection_sort(arr)` — Minimum prefix scanning & swaps.
  - `insertion_sort(arr)` — Key selection & backward shifting.
  - `merge_sort(arr)` — Subarray divide-and-conquer and merge buffer writes.
  - `quick_sort(arr)` — Pivot partitioning and recursive sub-ranges.
- **Graph Traversals**: `bfs(graph, start)` and `dfs(graph, start)`.
- **Shortest Path & Pathfinding**: `dijkstra(graph, start, target)` and `a_star(graph, start, goal, heuristic)`.
- **Dynamic Programming**: `fibonacci_dp(n, table)`.
- **Backtracking**: `n_queens(n, table)`.

---

## 2. Usage Example: Sorting an Array

```python
from animora.core import Scene
from animora.datastructures import Array
from animora.algorithms import quick_sort
from animora.theme import ModernDark, use_theme

class SortingScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            arr = Array([45, 12, 89, 33, 7, 56])
            self.play(arr.animate_create())
            self.play(*quick_sort(arr))
```
