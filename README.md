# Animora

[![PyPI Version](https://img.shields.io/pypi/v/animora.svg)](https://pypi.org/project/animora/)
[![CI](https://github.com/himanshu-jadhav108/Animora/actions/workflows/ci.yml/badge.svg)](https://github.com/himanshu-jadhav108/Animora/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://himanshu-jadhav108.github.io/Animora/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)

> **High-level, declarative animation framework built on top of Manim for educational, technical, mathematical, and algorithmic visualization.**

---

## 🌟 Overview

**Animora** provides an intuitive, high-level abstraction layer over [Manim](https://www.manim.community/) (Community Edition), inspired by the relationship between Seaborn and Matplotlib. Instead of manually orchestrating low-level vector primitives, Animora lets you describe **what** you want to visualize:

```python
from animora.core import Scene
from animora.datastructures import BST
from animora.theme import ModernDark, use_theme

class BSTDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            bst = BST([50, 30, 70, 20, 40])
            self.play(bst.animate_create())
            self.play(bst.animate_insert(35))
            self.play(bst.animate_search(35))
```

---

## 🚀 Installation

Install Animora via `pip`:

```bash
pip install animora
```

Verify your environment and media tools:

```bash
animora doctor
```

---

## 🛠️ CLI Quickstart

Scaffold, preview, and render your scenes rapidly:

```bash
# 1. Create a new starter scene
animora new my_scene.py

# 2. Fast preview
animora preview my_scene.py --open

# 3. High quality production render
animora render my_scene.py --quality high
```

---

## 📦 Features & Capabilities

- **Visual Primitives (`animora.components`)**: `Text`, `Shape`, `Connector`, `Arrow`, `Group`, `Panel`, `Label`.
- **Layout Solvers (`animora.layout`)**: `HorizontalLayout`, `VerticalLayout`, `GridLayout`, `CircularLayout`, `TreeLayout`, `GraphLayout`, `FlowLayout`.
- **Theme Engine (`animora.theme`)**: `ModernDark`, `PaperLight`, `Cyberpunk`, `Monokai`, `use_theme()`.
- **Data Visualization (`animora.dataviz`)**: `Axes`, `BarChart`, `LineChart`, `ScatterPlot`, `Histogram`, `Table`.
- **Data Structures (`animora.datastructures`)**: `Array`, `Stack`, `Queue`, `LinkedList`, `Heap`, `Tree`, `BST`, `Graph`, `HashTable`.
- **Algorithm Visualizations (`animora.algorithms`)**: Binary Search, 5 Sorting algorithms, BFS/DFS, Dijkstra, A*, DP, Backtracking.
- **Escape Hatch**: Full interoperability with raw Manim through `.manim_object`.

---

## 🧭 Roadmap Status

- [x] **Phase 0: Product & Architecture** — 4-layer design, module boundaries, API philosophy.
- [x] **Phase 1: Repository Foundation & Tooling** — Pyproject, CI matrix, test suite, linting.
- [x] **Phase 2: Core Abstractions** — `Component`, `Scene`, `Animation` bridge, escape hatch.
- [x] **Phase 3: Visual Primitives** — Text, Shape, Arrow, Connector, Group, Panel.
- [x] **Phase 4: Layout System** — Horizontal, Vertical, Grid, Circular, Tree, Graph, Flow.
- [x] **Phase 5: Theme Engine** — Design tokens, color palettes, dark/light themes.
- [x] **Phase 6: Data Visualizations** — Axes, BarChart, LineChart, ScatterPlot, Histogram, Table.
- [x] **Phase 7: Data Structures** — Array, LinkedList, Stack, Queue, Heap, Tree, BST, Graph, HashTable.
- [x] **Phase 8: Algorithms** — Search, Sorts, BFS/DFS, Dijkstra, A*, Dynamic Programming, Backtracking.
- [x] **Phase 9: CLI Tooling** — `animora new / preview / render / doctor`.
- [x] **Phase 10: Documentation & Examples** — Complete docs site, tutorials, recipes, runnable gallery.
- [x] **Phase 11: Performance & Profiling** — Benchmarks and bounding box caching.
- [x] **Phase 12: Release v0.1.0** — Packaging, changelog, publishing workflows.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines, and review our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
