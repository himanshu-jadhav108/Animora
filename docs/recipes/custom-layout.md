# Recipe: Custom Layout Solvers

## Goal
Implement a custom geometric layout solver (e.g. SpiralLayout) and apply it to any `Group` of Animora components.

---

## Solution

Inherit from `BaseLayout` and implement the `solve()` method:

```python
import numpy as np
from typing import Sequence
from animora.layout.base import BaseLayout, LayoutItem, LayoutResult
from animora.components import Group, Shape

class SpiralLayout(BaseLayout):
    def __init__(self, step_radius: float = 0.5, angle_step: float = 0.5) -> None:
        self.step_radius = step_radius
        self.angle_step = angle_step

    def solve(self, items: Sequence[LayoutItem], **kwargs) -> LayoutResult:
        positions: list[tuple[float, float, float]] = []
        for i, _ in enumerate(items):
            r = self.step_radius * i
            theta = self.angle_step * i
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            positions.append((float(x), float(y), 0.0))
        return LayoutResult(positions=positions)

# Apply to components
circles = [Shape.circle(radius=0.3) for _ in range(10)]
group = Group(*circles)
group.arrange(SpiralLayout())
```
