# Animora Architecture — Versioning & Compatibility Strategy

## 1. Python Version Support Policy

### Supported Python Versions: Python `>= 3.10`

Animora sets its minimum Python runtime floor at **Python 3.10**.

### Technical Justification
1. **Structural Pattern Matching (`match / case`)**: Extensively used in `animora.layout` and `animora.components` for AST parsing, layout tree traversal, and state transition dispatching.
2. **Modern Union Syntax (`TypeA | TypeB`)**: Native PEP 604 union types avoid boilerplate imports from `typing` and provide clean, readable type signatures across all public components.
3. **`typing.ParamSpec` and `Concatenate`**: Crucial for typing high-level animation decorators and builder functions.
4. **Active Ecosystem Support**: Python 3.10+ is supported by all major Linux distributions, macOS Homebrew, and Windows installers, ensuring broad accessibility while avoiding legacy compatibility baggage.

---

## 2. Manim Version Pinning & Upgrade Strategy

### Target Range: `manim >= 0.18.0, < 1.0.0`

Animora pins to a **compatible minor range** of [Manim Community Edition](https://github.com/ManimCommunity/manim).

### Strategy Rationale
- **Semantic Stability**: Manim Community Edition follows Semantic Versioning in its `0.x` series. Major breaking changes occur rarely and are signaled via deprecation cycles in minor releases.
- **Avoiding Stale Pins**: Hard-pinning to a single patch release (e.g. `manim == 0.18.1`) causes severe dependency conflicts when users install Animora alongside other Manim plugins or customized environments.
- **Upper Bound Guard (`< 1.0.0`)**: Protects against unexpected breaking API shifts when Manim eventually transitions to version `1.0.0`.

### Manim Upgrade Protocol
1. CI runs a weekly matrix build against the latest published `manim` release.
2. When Manim publishes a new minor release, automated tests verify that Animora's `.manim_object` bridge and animation wrappers remain 100% compatible.
3. Any deprecation warnings emitted by Manim internals are resolved in the next Animora patch/minor release.

---

## 3. Animora Semantic Versioning (SemVer 2.0.0)

Animora strictly adheres to [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **`0.x` Initial Development Phase (Phases 0–9)**:
  - `0.1.0`: Core abstractions, primitives, layouts, themes, data visualization.
  - `0.2.0`: Computer science data structures and collections.
  - `0.3.0`: Algorithms, traversal animations, and CLI tooling.
  - *Note*: During `0.x`, minor versions may introduce breaking changes if necessary, but all breaking changes will be clearly documented in `CHANGELOG.md`.

- **`1.0.0` Production Release (Phases 10–12)**:
  - Represents full API stability, comprehensive documentation, and production test coverage.
  - **PATCH** (`1.0.x`): Backwards-compatible bug fixes and performance improvements.
  - **MINOR** (`1.x.0`): New components, new layouts, new themes, or non-breaking API additions.
  - **MAJOR** (`x.0.0`): Breaking changes to the public API surface.

---

## 4. Deprecation Policy (Post-1.0)

1. Any public API element scheduled for removal must be marked with `@deprecated` / `warnings.warn(..., DeprecationWarning)` for at least **one full minor release cycle** before removal.
2. Deprecation messages must specify the exact replacement method or property and provide the scheduled removal version.
