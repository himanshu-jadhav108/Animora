# Theming & Design Tokens

Animora features a centralized design token system covering color palettes, typography scales, spacing, stroke widths, corner radii, and animation timing curves.

---

## 1. Built-in Themes

| Theme | Visual Tone | Background | Primary | Accent |
|---|---|---|---|---|
| **`ModernDark`** *(Default)* | Slate Dark Mode | `#0F172A` | `#38BDF8` | `#F59E0B` |
| **`PaperLight`** | Clean Light Mode | `#FFFFFF` | `#2563EB` | `#D97706` |
| **`Cyberpunk`** | High-Contrast Neon | `#0A0A0F` | `#EC4899` | `#10B981` |
| **`Monokai`** | Code Editor Palette | `#272822` | `#A6E22E` | `#F92672` |

---

## 2. Dynamic Scoping with `use_theme()`

Apply themes cleanly across a block of component creation:

```python
from animora.components import Text, Shape
from animora.theme import Cyberpunk, use_theme

with use_theme(Cyberpunk):
    # Components created here inherit Cyberpunk colors & styles
    title = Text("Neon Cyberpunk Title")
    node = Shape.circle()
```

---

## 3. Creating Custom Themes

```python
from animora.theme import ModernDark

solarized = ModernDark.merge(
    name="solarized",
    colors={
        "background": "#002B36",
        "surface": "#073642",
        "primary": "#268BD2",
        "accent": "#B58900",
    },
)
```

---

## 4. Animation Timing & Easing Presets

Animora provides named timing presets (`animora.theme.presets`) that standardize transition speeds and easing curves across educational presentations:

| Preset | Speed Multiplier | Easing / Curve | Recommended Use Case |
|---|---|---|---|
| **`SNAPPY`** | `0.6×` | Rapid ease-out | UI transitions, quick data adjustments |
| **`SMOOTH`** | `1.0×` | Standard smooth | Default educational pacing |
| **`CINEMATIC`** | `1.6×` | Smooth ease-in-out | Hero introductions, full scene wipes |
| **`PLAYFUL`** | `1.1×` | Bouncy ease-out | Interactive demos, casual walkthroughs |
| **`EDUCATIONAL`** | `1.8×` | Deliberate ease-in-out | Step-by-step algorithmic explanations |
| **`SLOW_MO`** | `3.0×` | Gradual ease-in-out | Micro-step inspections, race conditions |

```python
from animora.theme.presets import CINEMATIC, get_timing_preset

# Access pre-configured durations and curves:
duration = CINEMATIC.normal  # Scaled based on active theme
curve = CINEMATIC.easing_function

# Or retrieve by name string:
snappy_preset = get_timing_preset("snappy")
```

