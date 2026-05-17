# Animora

> High-level, declarative animation framework built on top of Manim for educational, technical, mathematical, and algorithmic visualization.

---

## 🌟 Overview

**Animora** provides an intuitive, high-level abstraction layer over [Manim](https://www.manim.community/) (Community Edition), inspired by the relationship between Seaborn and Matplotlib. Instead of manually orchestrating low-level vector primitives (`Circle`, `Line`, `Transform`, `FadeIn`), Animora lets you describe **what** you want to visualize:

```python
# Coming in v0.1:
graph = Graph(edges)
graph.bfs(start="A")
```

---

## 📐 Architecture & Design

Animora is designed with a strict 4-layer architecture, pure layout solvers, and a first-class escape hatch (`.manim_object`) for seamless Manim interoperability.

Explore the architecture specifications:
- [Overview & Layered Design](docs/architecture/00-overview.md)
- [Module Boundaries & Responsibilities](docs/architecture/module-boundaries.md)
- [Public API Philosophy & Escape Hatch](docs/architecture/api-philosophy.md)
- [Dependency Policy](docs/architecture/dependency-policy.md)
- [Versioning & Compatibility Strategy](docs/architecture/versioning-strategy.md)

---

## 🚀 Roadmap

- **Phase 0**: Product & Architecture *(Completed)*
- **Phase 1**: Foundation, Tooling, & CI *(In Progress)*
- **Phase 2**: Core Abstractions (`Component`, `Scene`, `Animation`)
- **Phase 3**: Visual Primitives
- **Phase 4**: Layout System
- **Phase 5**: Theme Engine
- **Phase 6**: Data Visualizations
- **Phase 7**: Data Structures
- **Phase 8**: Algorithms
- **Phase 9**: CLI Tooling
- **Phase 10**: Documentation & Tutorials
- **Phase 11**: Performance & Profiling
- **Phase 12**: v1.0 Release

---

## 📄 License

MIT License.
