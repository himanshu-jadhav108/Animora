# Composable Effects Engine & Material Design Architecture

**Document Version:** 1.0.0  
**Status:** Approved Architecture & Prototype Specification  
**Scope:** CPU 2D Cairo Animation Engine (Pure Python / Manim)  
**Target Consumer:** Feature H (Typography Animations) & Visual Primitives  

---

## 1. Architectural Problem & Vision

Educational and technical visualization often requires stylized emphasis—such as glowing keywords, chromatic glitch transitions, gradient reveals, or pulsing beacons. In early Manim projects, these are frequently built as bespoke, hardcoded animation classes (e.g., `CyberpunkGlitchText`, `AuroraTitle`) with embedded hex codes and tightly coupled rendering loops.

This results in a maintenance anti-pattern:
1. **Combinatorial Explosion:** 10 themes $\times$ 10 visual effects = 100 hardcoded classes.
2. **Theme Duplication:** Color tokens and timing curves are duplicated across effects instead of inheriting from `animora.theme`.
3. **Fragile Coupling:** Modifying component geometry breaks the effect, and swapping themes requires changing animation code.

The **Effects Engine** solves this by enforcing an orthogonal separation of concerns:
$$\text{Visual Appearance} = \text{Component} \times \text{Theme (Design Tokens)} \times \text{Choreographic Effect}$$

---

## 2. API Design & Signature Decisions

### Core Abstraction: Decoupled Effect Strategy

An **Effect** in Animora is a pure choreographic strategy that operates on a `Component`'s Manim sub-mobjects using the color palettes and timing tokens of a `Theme`.

```python
# Function-level invocation
from animora.theme.effects import apply_effect

anim = apply_effect(title, effect="gradient_reveal", theme=Cyberpunk, run_time=1.2)
scene.play(anim)

# Or via Component convenience method
scene.play(title.apply_effect("glitch", theme="aurora", run_time=0.8))
```

### Registration & Extensibility Model: Registry Pattern

We considered three design choices for effect definitions:

| Pattern | Pros | Cons | Verdict |
|---|---|---|---|
| **Hardcoded Classes** (`GlitchText`) | Fast to write initially | Combinatorial explosion, unextensible by third parties | **Rejected** |
| **Pure Data Config** (JSON/YAML) | Declarative | Cannot express complex sequential Manim transforms | **Rejected** |
| **Strategy Class + Registry** (`@register_effect`) | Fully composable, type-safe, open-closed principle | Small indirection layer | **Selected** |

Each effect subclasses `BaseEffect` and registers itself using `@register_effect(name)`:

```python
@register_effect("pulse_glow")
class PulseGlowEffect(BaseEffect):
    def build_animation(
        self,
        component: Component,
        theme: Theme,
        run_time: float,
        **kwargs: Any,
    ) -> manim.Animation: ...
```

---

## 3. Integration with the Existing Theme System

The Effects Engine **extends**, rather than duplicates, `animora.theme`:
1. **Dynamic Theme Inheritance:** If `theme` is omitted in `apply_effect(...)`, the engine dynamically retrieves the ambient theme via `get_active_theme()`.
2. **String Lookup:** Passing `theme="cyberpunk"` or `theme="aurora"` dynamically resolves to the corresponding registered `Theme` instance.
3. **Token Usage:** Effects extract `theme.colors.primary`, `theme.colors.secondary`, `theme.colors.accent`, and `theme.timing.*` directly. No hardcoded hex values exist in effect code.

---

## 4. Pure 2D CPU Cairo vs. GPU Shader Boundary

A critical constraint established in `09_FEATURE_CANDIDATE_EVALUATION.md` (Feature J rejection) is that **GPU/OpenGL shaders are explicitly out of scope**. Shaders require headless GPU drivers, EGL contexts, and break deterministic CPU frame-rendering on headless Linux CI containers.

All Animora effects execute in **pure 2D CPU Cairo**:

| Effect | 2D CPU Cairo Implementation | GPU Shader Equivalent (Deferred) |
|---|---|---|
| **`gradient_reveal`** | Submobject color assignment with staggered `FadeIn` lag ratios | Fragment shader gradient ramp |
| **`glitch`** | Rapid discrete sub-character horizontal coordinate displacement and chromatic flicker | Scanline distortion fragment shader |
| **`pulse_glow`** | Dual-pass stroke expansion, opacity breathing, and `Indicate` color highlights | Bloom / Gaussian blur post-processing |

---

## 5. Prototype Implementation Scope (Phase 06)

To validate the architecture without unnecessary bloat, Phase 06 scopes the implementation deliberately:
- **Component Scope:** `Text` (the foundational component for Feature H typography).
- **Themes Supported:** 3 themes (`ModernDark`, `Cyberpunk`, and a new creative palette `Aurora`).
- **Effects Supported:** 3 composable effects (`gradient_reveal`, `glitch`, `pulse_glow`).

### Deliberately Out of Scope for Phase 06:
- Non-Text visual primitives (e.g., 3D meshes, particle physics clouds).
- Full 19-theme aspirational list (deferred to future community/theme expansions).
- Fragment/vertex GLSL shaders (Feature J, deferred).
