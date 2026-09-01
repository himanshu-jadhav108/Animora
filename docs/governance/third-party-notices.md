# Third-Party Notices & Dependency Attribution

This document provides licensing information, attributions, and official project links for third-party libraries, tools, and system dependencies used by **Animora**.

Animora strictly utilizes open-source dependencies under permissive, business-friendly, and educational-friendly licenses (e.g., MIT, BSD-3-Clause, Apache 2.0).

---

## 1. Runtime Dependencies

| Package | Purpose in Animora | License | Copyright / Attribution | Project URL |
| :--- | :--- | :--- | :--- | :--- |
| **Manim** (`>=0.18.0,<1.0.0`) | Foundational vector graphics rendering and mathematical animation engine (Community Edition). | **MIT** | Copyright © 2020–2026 The Manim Community Developers | [manim.community](https://www.manim.community/) |
| **NumPy** (`>=1.24.0,<3.0.0`) | High-performance numerical computing, matrix transformations, and coordinate mathematics. | **BSD-3-Clause** | Copyright © 2005–2026 NumPy Developers | [numpy.org](https://numpy.org/) |
| **NetworkX** (`>=3.0,<4.0`) | Graph and network data structures, topological traversals, and geometric layout algorithms. | **BSD-3-Clause** | Copyright © 2004–2026 NetworkX Developers | [networkx.org](https://networkx.org/) |

---

## 2. Optional Feature Dependencies

| Package | Feature Extra | Purpose | License | Copyright / Attribution | Project URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Click** (`>=8.0`) | `[cli]` | Command-line interface framework powering `animora new`, `preview`, `doctor`, and `render`. | **BSD-3-Clause** | Copyright © 2014 Pallets | [palletsprojects.com/p/click](https://palletsprojects.com/p/click/) |
| **Rich** (`>=13.0`) | `[cli]` | Terminal formatting, progress indicators, syntax highlighting, and CLI diagnostics. | **MIT** | Copyright © 2020 Will McGugan | [github.com/Textualize/rich](https://github.com/Textualize/rich) |
| **Material for MkDocs** (`>=9.5`) | `[docs]` | Modern documentation website generation, theme styling, and search indexing. | **MIT** | Copyright © 2016–2026 Martin Donath | [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/) |

---

## 3. Development & Build Dependencies

| Package | Purpose | License | Project URL |
| :--- | :--- | :--- | :--- |
| **Hatchling** (`>=1.21.0`) | PEP 517 build backend for packaging and wheel generation. | **MIT** | [hatch.pypa.io](https://hatch.pypa.io/) |
| **Pytest** (`>=8.0`) | Primary testing framework and assertion runner. | **MIT** | [pytest.org](https://pytest.org/) |
| **pytest-cov** (`>=4.1`) | Code coverage plugin for Pytest. | **MIT** | [github.com/pytest-dev/pytest-cov](https://github.com/pytest-dev/pytest-cov) |
| **Ruff** (`>=0.3.0`) | Ultra-fast Python code linter and code formatter. | **MIT / Apache-2.0** | [astral.sh/ruff](https://astral.sh/ruff) |
| **MyPy** (`>=1.9.0`) | Static type checker enforcing type safety. | **MIT** | [mypy-lang.org](https://mypy-lang.org/) |

---

## 4. System & External Media Tools

| Tool | Purpose | Typical License | Notes | Project URL |
| :--- | :--- | :--- | :--- | :--- |
| **FFmpeg** | Video encoding, frame composition, and media demuxing used by Manim. | **LGPL v2.1+ / GPL v2+** | Installed independently by the user via OS package managers or official binaries. | [ffmpeg.org](https://ffmpeg.org/) |
| **Cairo** | 2D vector graphics rasterization library used by Manim's rendering pipeline. | **LGPL v2.1 / MPL 1.1** | Provided as system library or via binary wheels (`pycairo`). | [cairographics.org](https://www.cairographics.org/) |
| **Pango** | Text rendering and font shaping engine used for typesetting text and typography. | **LGPL v2.0+** | Provided as system library or via binary wheels (`manimpango`). | [pango.gnome.org](https://pango.gnome.org/) |

---

## 5. Bundled Assets & Templates

- **Documentation Media (`docs/assets/media/*.svg`)**: All visual diagrams, scene figures, and architecture SVGs are original works authored for Animora and licensed under the repository's MIT License.
- **CLI Templates (`src/animora/cli/templates/*.py.template`)**: Starter scene templates provided for `animora new` scaffolding are original Animora code released under the MIT License.
