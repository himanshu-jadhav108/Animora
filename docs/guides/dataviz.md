# Data Visualization Components

Animora provides educational chart components built on a **Dual-Correctness Architecture**: mathematical data transforms (computational correctness) are isolated from Manim visual animation generation.

---

## 1. Components Catalog

- **`Axes`**: 2D coordinate system providing pure mathematical `c2p(x, y)` and `p2c(point)` mappings.
- **`BarChart`**: Maps categorical and numerical data to proportional bar heights with `animate_grow()` and `animate_highlight_bar()`.
- **`LineChart`**: Connects data coordinates with `Connector` line segments and vertex dots with `animate_draw()`.
- **`ScatterPlot`**: Translates data pairs to scene coordinates with `animate_plot()`.
- **`Histogram`**: Computes statistical frequency distributions matching `numpy.histogram` reference with `animate_grow()`.
- **`Table`**: Tabular grid visualizer arranged via Phase 4 `GridLayout` with `animate_highlight_cell()`.

---

## 2. Usage Example

```python
from animora.core import Scene
from animora.dataviz import BarChart, Table
from animora.theme import ModernDark, use_theme

class ChartDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            chart = BarChart(
                data=[("MergeSort", 45), ("QuickSort", 30), ("BubbleSort", 120)],
            )
            self.play(chart.animate_grow())
            self.play(chart.animate_highlight_bar(1, color="#10B981"))
```
