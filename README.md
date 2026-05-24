# Animora

[![CI](https://github.com/himanshu-jadhav108/Animora/actions/workflows/ci.yml/badge.svg)](https://github.com/himanshu-jadhav108/Animora/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)

> High-level, declarative animation framework built on top of Manim for educational, technical, mathematical, and algorithmic visualization.

---

## 🌟 Overview

**Animora** provides an intuitive, high-level abstraction layer over [Manim](https://www.manim.community/) (Community Edition), inspired by the relationship between Seaborn and Matplotlib. Instead of manually orchestrating low-level vector primitives (`Circle`, `Line`, `Transform`, `FadeIn`), Animora lets you describe **what** you want to visualize:

```python
# Declarative, high-level visualization (coming in v0.1):
from animora.components.dsa import Graph

graph = Graph(edges=[("A", "B"), ("B", "C"), ("A", "C")])
graph.bfs(start="A")
```

---

## 🚀 Quick Start (Development Install)

Animora requires Python 3.10 or higher.

```bash
# 1. Clone the repository
git clone https://github.com/himanshu-jadhav108/Animora.git
cd Animora

# 2. Set up virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

# 3. Install in editable mode with development dependencies
pip install -e ".[dev]"
```

---

## 📐 Architecture & Design

Animora is built around a decoupled 4-layer architecture, pure layout solvers, and a first-class escape hatch (`.manim_object`) for seamless Manim interoperability.

Explore our architectural specifications:
- [Overview & Layered Design](docs/architecture/00-overview.md)
- [Module Boundaries & Responsibilities](docs/architecture/module-boundaries.md)
- [Public API Philosophy & Escape Hatch](docs/architecture/api-philosophy.md)
- [Dependency Policy](docs/architecture/dependency-policy.md)
- [Versioning & Compatibility Strategy](docs/architecture/versioning-strategy.md)

---

## 🧭 Roadmap

- [x] **Phase 0: Product & Architecture** — Layered design, module boundaries, API philosophy.
- [x] **Phase 1: Repository Foundation & Tooling** — Package skeleton, pyproject.toml, CI, tests, linting.
- [ ] **Phase 2: Core Abstractions** — `Component`, `Scene`, `Animation` bridge.
- [ ] **Phase 3: Visual Primitives** — Text, Shape, Arrow, Connector, Group, Panel.
- [ ] **Phase 4: Layout System** — Horizontal, vertical, grid, circular, tree, graph layouts.
- [ ] **Phase 5: Theme Engine** — Design tokens, color palettes, dark/light themes.
- [ ] **Phase 6: Data Visualizations** — Axes, BarChart, LineChart, ScatterPlot, Histogram, Table.
- [ ] **Phase 7: Data Structures** — Array, LinkedList, Stack, Queue, Heap, Tree, BST, Graph, HashTable.
- [ ] **Phase 8: Algorithms** — Search, Sorts, BFS/DFS, Dijkstra, A*, Dynamic Programming.
- [ ] **Phase 9: CLI Tooling** — `animora new / preview / render / doctor`.
- [ ] **Phase 10: Documentation & Tutorials** — Complete documentation site, interactive guides.
- [ ] **Phase 11: Performance & Profiling** — Benchmarks and optimization.
- [ ] **Phase 12: v1.0 Release** — Packaging, changelog, PyPI release.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines, and review our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
