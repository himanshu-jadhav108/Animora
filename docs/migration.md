# Migration & Version Compatibility

## Pre-1.0 Development Stability

During development across Phases 0 through 10, **zero public breaking changes** occurred:

- **Phase 2 & 3 Abstractions & Primitives**: The public constructor signatures of `Component`, `Scene`, `Text`, `Shape`, `Connector`, `Arrow`, `Group`, `Panel`, and `Label` have remained 100% backward compatible.
- **Phase 5 Theming**: The introduction of the theme engine was strictly additive. Primitives resolve unassigned (`None`) attributes dynamically against the active theme, strictly enforcing `explicit parameter > active theme > fallback`.
- **Phase 6 & 7 Compositions**: Data visualization (`dataviz`) and data structures (`datastructures`) cleanly composed Phase 3 primitives and Phase 4 layout engines without modifying lower-level APIs.
- **Phase 8 & 9 Algorithms & CLI**: Algorithm visualizations directly drive existing public state-visualization primitives without altering internal contracts.

---

## Deprecation Policy

Starting with Animora `1.0.0`, all deprecations will follow a standard 2-minor-release deprecation warning cycle before removal.
