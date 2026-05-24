# Welcome to Animora

**Animora** is a high-level, declarative animation framework built on top of [Manim](https://www.manim.community/) (Community Edition) for creating educational, technical, mathematical, and algorithmic visualizations.

---

## 💡 The Animora Philosophy

Just as **Seaborn** sits on top of Matplotlib to make statistical plots intuitive, **Animora** sits on top of Manim to make technical and algorithmic animation effortless:

```python
# Coming soon in v0.1:
from animora.components.dsa import Graph

graph = Graph(edges=[("A", "B"), ("B", "C"), ("A", "C")])
graph.bfs(start="A")
```

---

## 📖 Architecture & Design Specifications

During Phase 0, complete architectural specifications were established:

- [System Overview & Layered Architecture](architecture/00-overview.md)
- [Module Boundaries & Responsibilities](architecture/module-boundaries.md)
- [Public API Philosophy & Escape Hatch Design](architecture/api-philosophy.md)
- [Dependency Policy](architecture/dependency-policy.md)
- [Versioning & Compatibility Strategy](architecture/versioning-strategy.md)

---

## 🛠️ Development Status

Animora is currently in active foundational development. Follow along on our [GitHub Repository](https://github.com/himanshu-jadhav108/Animora).
