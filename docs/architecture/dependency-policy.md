# Animora Architecture — Dependency Policy & Ecosystem Integration

## 1. Classification Framework

Animora classifies all external dependencies into three strict tiers:

1. **Hard (Runtime) Dependencies**: Required for core library usage. Installed automatically with `pip install animora`.
2. **Optional Extras**: Additional features (e.g. CLI formatting, enhanced export formats) enabled via bracket syntax (e.g. `pip install animora[cli]`, `pip install animora[docs]`).
3. **Development Dependencies**: Tooling required strictly for building, testing, linting, and maintaining the repository.

---

## 2. Dependency Table & Justification

| Package | Classification | Minimum Version | License | Justification |
|---|---|---|---|---|
| **`manim`** | **Hard (Runtime)** | `>=0.18.0, <1.0.0` | MIT | Core vector animation engine and rendering backend (Community Edition). |
| **`numpy`** | **Hard (Runtime)** | `>=1.24.0, <3.0.0` | BSD-3-Clause | Foundational vector, matrix, coordinate transformations, and numerical data processing. |
| **`networkx`** | **Hard (Runtime)** | `>=3.0, <4.0` | BSD-3-Clause | Topological graph representation, shortest-path algorithms, tree hierarchy traversal, and graph layout coordinates. |
| **`click`** / **`typer`** | **Optional (`[cli]`)** | `>=8.0` | MIT / MIT | Clean, modern CLI framework powering `animora new`, `preview`, and `doctor`. |
| **`rich`** | **Optional (`[cli]`)** | `>=13.0` | MIT | Terminal formatting, progress bars, and diagnostics for CLI outputs. |
| **`pytest`** | **Development** | `>=8.0` | MIT | Primary test runner and assertion framework for unit and integration testing. |
| **`pytest-cov`** | **Development** | `>=4.1` | MIT | Code coverage reporting ensuring minimum 90% coverage on core and layouts. |
| **`ruff`** | **Development** | `>=0.3.0` | MIT / Apache-2.0 | Ultra-fast linter and code formatter replacing flake8, isort, and black. |
| **`mypy`** | **Development** | `>=1.9.0` | MIT | Static type checker enforcing strict type safety across all public and internal interfaces. |
| **`flit-core`** / **`hatchling`** | **Build System** | Standard PEP 517 | MIT | Modern, standardized Python packaging backend without legacy `setup.py`. |
| **`mkdocs-material`** | **Development (`[docs]`)**| `>=9.5` | MIT | Modern, fast documentation site generator supporting markdown, search, and syntax highlighting. |

---

## 3. Dependency Policy Rules

1. **Zero Unjustified Dependencies**: No dependency may be added to runtime `dependencies` in `pyproject.toml` unless it provides functionality that would otherwise require hundreds of lines of complex, error-prone custom mathematics or rendering logic.
2. **License Compatibility**: All runtime dependencies must use permissive licenses (MIT, BSD-2/3-Clause, Apache 2.0). Copyleft licenses (GPL, AGPL) are prohibited in hard dependencies to ensure Animora remains universally usable for commercial and educational purposes.
3. **No Heavy Deep Learning Frameworks**: Animora is an animation and visualization engine; deep learning frameworks (PyTorch, TensorFlow) must never become hard dependencies.
4. **Pure Python Where Possible**: Except for precompiled wheels provided by `numpy` and `manim`'s system dependencies (cairo/ffmpeg), Animora core code remains pure Python to guarantee cross-platform compatibility across Windows, macOS, and Linux.
