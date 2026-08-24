# Recipe: Mid-Scene Theme Switching

## Goal
Switch themes dynamically within a single scene to showcase dark and light mode contrasts.

---

## Solution

Use the `with use_theme(Theme):` context manager for block-level theme scoping:

```python
from animora.core import Scene
from animora.components import Text, Shape, Panel
from animora.theme import ModernDark, PaperLight, use_theme

class MultiThemeScene(Scene):
    def construct(self) -> None:
        # 1. Dark Mode Box
        with use_theme(ModernDark):
            dark_title = Text("Dark Theme")
            dark_card = Panel(Shape.circle(), title=dark_title).move_to([-3, 0, 0])

        # 2. Light Mode Box
        with use_theme(PaperLight):
            light_title = Text("Light Theme")
            light_card = Panel(Shape.circle(), title=light_title).move_to([3, 0, 0])

        self.play(dark_card.animate_create())
        self.play(light_card.animate_create())
```
