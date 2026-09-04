<div align="center">

# 🎬 Animora

### *Declarative, High-Level Animation Framework for Python*

[![PyPI Version](https://img.shields.io/badge/pypi-v0.2.0a1-3776AB?logo=pypi&logoColor=white)](https://pypi.org/project/animora/)
[![CI Status](https://img.shields.io/badge/CI-Passing-22c55e?logo=githubactions&logoColor=white)](https://github.com/himanshu-jadhav108/Animora/actions)
[![Docs](https://img.shields.io/badge/Docs-Live-38BDF8?logo=materialformkdocs&logoColor=white)](https://himanshu-jadhav108.github.io/Animora/)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://pypi.org/project/animora/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/Types-MyPy%20Checked-1f425f.svg)](https://mypy-lang.org/)

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-why-animora">Why Animora?</a> •
  <a href="#-features--examples">Features & Examples</a> •
  <a href="#-cli-tooling">CLI Tooling</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="https://himanshu-jadhav108.github.io/Animora/">Documentation</a>
</p>

</div>

---

## 🌟 Overview

**Animora** is to [Manim](https://www.manim.community/) what **Seaborn** is to **Matplotlib**.

Instead of manually calculating pixel coordinates, managing low-level point arrays, and choreographing dozens of vector mobjects, Animora enables you to write **clean, declarative, and composable animations** for educational videos, computer science lectures, technical presentations, and data stories.

```python
from animora.core import Scene
from animora.datastructures import BST
from animora.theme import ModernDark, use_theme


class BinarySearchTreeDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Declaratively initialize a Binary Search Tree
            bst = BST([50, 30, 70, 20, 40])
            self.play(bst.animate_create())

            # 2. Insert key with animated comparison path: 50 -> 30 -> 40 -> 35
            self.play(bst.animate_insert(35))

            # 3. Search target key with instant visual highlight
            self.play(bst.animate_search(35))
```

---

## 💡 Why Animora?

| Capability | Raw Manim | With Animora |
|:---|:---|:---|
| **Programming Model** | Imperative, low-level coordinate positioning | Declarative, component-based composition |
| **Layouts** | Manual `.next_to()`, `.shift()`, and math calculations | Automatic solvers (`Grid`, `Circular`, `Tree`, `Graph`, `Flow`) |
| **Theming & Styling** | Hardcoded hex strings scattered in scripts | Centralized design tokens (`ModernDark`, `PaperLight`, `Cyberpunk`) |
| **Data Structures** | Manual construction of circles, arrows, and text | Stateful `Array`, `BST`, `Graph`, `Heap`, `Stack`, `Queue`, `HashTable` |
| **Algorithm Animations** | Ad-hoc animation choreography | Traced execution (`quick_sort`, `dijkstra`, `a_star`, `binary_search`) |
| **Extensibility** | Fixed to Manim APIs | First-class **Escape Hatch** (`.manim_object`) on all components |

---

## 🚀 Quick Start

### 1. Installation

Install Animora from PyPI:

```bash
pip install animora
```

*(Optional: Install with development dependencies)*
```bash
pip install "animora[dev]"
```

### 2. Verify Your Environment

Animora includes a built-in doctor to verify Python, Manim, and FFmpeg installations:

```bash
animora doctor
```

```text
============================================================
 Animora System & Environment Diagnostics
============================================================
[PASS]   Python       : Python 3.11.8 (>= 3.10 supported)
[PASS]   Animora      : Animora 0.1.0 installed
[PASS]   Manim        : Manim Community 0.18.1 (compatible)
[PASS]   NumPy        : NumPy 1.26.4 installed
[PASS]   NetworkX     : NetworkX 3.2.1 installed
[PASS]   FFmpeg       : FFmpeg binary found at /usr/bin/ffmpeg
============================================================
Status: Environment is fully ready for Animora visualizations.
```

---

## 🛠️ CLI Tooling

Animora comes with a dedicated CLI for rapid prototyping and production export:

```bash
# 1. Scaffold a starter scene from template
animora new my_scene.py

# 2. Fast low-quality preview (instant rendering for iterative design)
animora preview my_scene.py --open

# 3. Full production quality render (1080p 60fps or 4K)
animora render my_scene.py --quality high
```

---

## 📦 Features & Examples

### 1. Visual Primitives & Container Panels
Compose shapes, text, arrows, and containers with semantic state animations:

```python
from animora.core import Scene
from animora.components import Text, Shape, Panel, Arrow
from animora.theme import ModernDark, use_theme


class PrimitivesScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            title = Text("Visual Primitives", font_size=36)
            circle = Shape.circle(radius=0.6, fill_color="#38BDF8")
            rect = Shape.rounded_rectangle(width=2.0, height=1.2, corner_radius=0.15)
            card = Panel(circle, rect, title="Component Container")

            self.play(title.animate_fade_in())
            self.play(card.animate_create())
            self.play(circle.animate_highlight())
```

### 2. Automatic Layout Solvers
Pure geometric layout engines that automatically arrange collections of components:

```python
from animora.components import Group, Shape
from animora.layout import GridLayout, CircularLayout

nodes = [Shape.circle(radius=0.3) for _ in range(8)]
group = Group(*nodes)

# Arrange in a 2x4 Grid
group.arrange(GridLayout(columns=4, col_spacing=0.5, row_spacing=0.5))

# Rearrange into a Circle
group.arrange(CircularLayout(radius=2.0))
```

### 3. Data Visualization
Mathematically rigorous chart components featuring dual-correctness:

```python
from animora.core import Scene
from animora.dataviz import BarChart, Table


class ChartScene(Scene):
    def construct(self) -> None:
        chart = BarChart(
            data=[("MergeSort", 45), ("QuickSort", 30), ("BubbleSort", 120)],
            bar_width=0.7,
        )
        self.play(chart.animate_grow())
        self.play(chart.animate_highlight_bar(1, color="#10B981"))
```

### 4. Algorithm Visualizations & Tracing
Generate step-by-step algorithm animations directly from real execution traces:

```python
from animora.core import Scene
from animora.datastructures import Array
from animora.algorithms import quick_sort


class SortingScene(Scene):
    def construct(self) -> None:
        arr = Array([45, 12, 89, 33, 7, 56])
        self.play(arr.animate_create())

        # Returns a sequence of step-by-step animations (compares, swaps, highlights)
        self.play(*quick_sort(arr))
```

### 5. Multi-Theme Scoping
Dynamically switch between built-in design systems (`ModernDark`, `PaperLight`, `Cyberpunk`, `Monokai`):

```python
from animora.components import Text, Shape, Panel
from animora.theme import Cyberpunk, PaperLight, use_theme

with use_theme(Cyberpunk):
    neon_box = Panel(Shape.circle(), title=Text("Cyberpunk"))

with use_theme(PaperLight):
    clean_box = Panel(Shape.circle(), title=Text("Paper Light"))
```

---

## 🏗️ Architecture & Escape Hatch

Animora follows a strict 4-layer decoupled architecture:

```text
┌────────────────────────────────────────────────────────┐
│ Layer 4: Algorithms & Data Visualization               │
│          (Sorting, Pathfinding, Charts, Trees, Tables) │
├────────────────────────────────────────────────────────┤
│ Layer 3: Layout Engines & Theme System                 │
│          (Grid, TreeLayout, ModernDark, Cyberpunk)     │
├────────────────────────────────────────────────────────┤
│ Layer 2: Visual Primitives & Containers                │
│          (Text, Shape, Connector, Arrow, Group, Panel) │
├────────────────────────────────────────────────────────┤
│ Layer 1: Core Abstractions & Manim Bridge              │
│          (Component, Scene, Animation, .manim_object)  │
└────────────────────────────────────────────────────────┘
```

### The Native Manim Escape Hatch
You are never locked into Animora's abstractions. Every single component exposes its underlying Manim vector entity through `.manim_object`:

```python
import manim
from animora.components import Shape

circle = Shape.circle(radius=1.0)
native_mobject = circle.manim_object  # Access raw Manim VMobject

# Use raw Manim shaders, gradients, or updaters freely
native_mobject.set_color_by_gradient(manim.BLUE, manim.PINK)
```

---

## 🎨 Example Gallery

Check out runnable examples located in the [`examples/`](examples/) directory:

- [`01_basics_and_shapes.py`](examples/01_basics_and_shapes.py) — Visual primitives & container panels.
- [`02_layout_and_grouping.py`](examples/02_layout_and_grouping.py) — Automatic layout solvers.
- [`03_themes_and_styling.py`](examples/03_themes_and_styling.py) — Multi-theme scoping.
- [`04_dataviz_charts.py`](examples/04_dataviz_charts.py) — Bar charts & data visualization.
- [`05_datastructures_bst.py`](examples/05_datastructures_bst.py) — Binary Search Tree with path tracing.
- [`06_algorithms_sorting.py`](examples/06_algorithms_sorting.py) — Quick Sort animation.
- [`07_pathfinding_dijkstra.py`](examples/07_pathfinding_dijkstra.py) — Dijkstra graph shortest path.

---

## 🤝 Contributing

We welcome community contributions! Please read our [Contributing Guide](CONTRIBUTING.md) and review our [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

### Development Setup

```bash
git clone https://github.com/himanshu-jadhav108/Animora.git
cd Animora
pip install -e ".[dev]"
pytest
ruff check src/
mypy src/
```

---

## 👤 Creator

Animora was created by **Himanshu Jadhav** and is developed as an open-source Python animation framework for educational, mathematical, algorithmic, and technical visualization.

<br>

<p align="center">
  <table align="center" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(8px); padding: 20px; max-width: 500px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);">
    <tr>
      <td align="center">
        <h3 style="margin: 0; color: #38bdf8; font-size: 1.6em; font-weight: 800; letter-spacing: -0.5px;">Himanshu Jadhav</h3>
        <p style="color: #94a3b8; font-weight: 500; margin: 4px 0 15px 0;">Artificial Intelligence & Data Science Engineer</p>
        <p style="color: #cbd5e1; font-size: 0.95em; max-width: 400px; line-height: 1.5; margin-bottom: 20px;">
          Passionate about computer vision, mathematical animation engines, declarative developer tooling, and high-performance algorithms.
        </p>
        <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
          <a href="https://github.com/himanshu-jadhav108" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
          <a href="https://www.linkedin.com/in/himanshu-jadhav-328082339" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
          <a href="https://himanshu-jadhav-portfolio.vercel.app/" target="_blank"><img src="https://img.shields.io/badge/Portfolio-FFD700?style=for-the-badge&logo=google-chrome&logoColor=black" alt="Portfolio"></a>
          <a href="https://www.instagram.com/himanshu_jadhav_108" target="_blank"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"></a>
        </div>
      </td>
    </tr>
  </table>
</p>

<br>

---

## 📄 License & Intellectual Property

Animora's source code is released under the **[MIT License](LICENSE)**.

- **Copyright Notice**: [COPYRIGHT.md](COPYRIGHT.md) — Copyright © 2026 Himanshu Jadhav.
- **Brand & Fork Policy**: [TRADEMARKS.md](TRADEMARKS.md) — Guidelines for project branding, naming forks, and derivative works.
- **Third-Party Notices**: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — Dependency attributions and upstream license details.
- **Security Policy**: [SECURITY.md](SECURITY.md) — Vulnerability reporting guidelines and security procedures.

*(The MIT License applies to the source code and does not grant permission to use the Animora name, logo, or branding in a way that implies official affiliation or endorsement.)*

---

## 💖 Acknowledgements

- [Manim Community](https://www.manim.community/) for the foundational vector graphics and mathematical animation engine.
- [NumPy](https://numpy.org/) for high-performance numerical computing and array operations.
- [NetworkX](https://networkx.org/) for graph data structures and force-directed spring layout algorithms.
- [FFmpeg](https://ffmpeg.org/) for specialized media demuxing and video stream encoding.
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for modern, responsive documentation tooling.
- The open-source mathematical visualization and computer science community.

---

<p align="center">
  <b>Animora — Declarative Animation Engine for Python</b>
</p>

