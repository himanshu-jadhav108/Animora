# Creating Your First Scene

This tutorial walks you through creating, styling, and rendering your first Animora animation in less than 5 minutes.

---

## 1. Scaffold a Starter Scene

Use the Animora CLI to create a new starter scene file:

```bash
animora new my_first_scene.py
```

This creates a clean, well-commented Python file:

```python
"""Starter Animora scene."""

from __future__ import annotations

from animora.core import Scene
from animora.components import Text, Shape, Panel
from animora.theme import ModernDark, use_theme


class StarterScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Add Text
            title = Text("Hello Animora!", font_size=40)
            title.move_to([0, 2.5, 0])

            # 2. Add Shape in Panel
            circle = Shape.circle(radius=0.7)
            card = Panel(circle, title="My First Primitive")

            # 3. Play semantic animations
            self.play(title.animate_fade_in(run_time=0.8))
            self.play(card.animate_create(run_time=1.0))
            self.play(circle.animate_highlight(run_time=0.8))
            self.wait(1)
```

---

## 2. Preview Your Scene

Render a fast preview using low-quality settings:

```bash
animora preview my_first_scene.py --open
```

The video will render rapidly and open in your default media player.

---

## 3. Render Final High-Quality Export

When you are ready to export your final production video (1080p 60fps or 4K):

```bash
animora render my_first_scene.py --quality high
```
