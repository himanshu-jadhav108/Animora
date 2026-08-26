# API Stability & Semantic Versioning Policy

## 1. Versioning Guarantee for v0.1.0

Animora follows [Semantic Versioning 2.0.0](https://semver.org/).

As a `0.1.0` release:
- **Public API Surface**: The public API includes all classes, methods, and functions documented in the [API Reference](reference/api.md) and exported from `animora`.
- **Zero Casual Breaking Changes**: While minor version bumps prior to `1.0.0` may introduce refinements, all changes will be documented with deprecation warnings across at least one minor release cycle.
- **Escape Hatch Invariant**: The `.manim_object` property on all `Component` classes is a permanent architectural guarantee and will never be removed.

---

## 2. Supported Python & Environment Matrix

- **Python**: `>= 3.10` (tested on 3.10, 3.11, 3.12)
- **Platforms**: Linux (Ubuntu), macOS, Windows
- **Core Dependencies**: `manim >= 0.18.0`, `numpy >= 1.24.0`, `networkx >= 3.0`
