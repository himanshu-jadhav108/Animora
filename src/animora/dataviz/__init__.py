"""Data visualization components for Animora.

Includes animated chart and tabular visualization components:
Axes, BarChart, LineChart, ScatterPlot, Histogram, and Table.
"""

from __future__ import annotations

from animora.dataviz.axes import Axes
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.histogram import Histogram
from animora.dataviz.line_chart import LineChart
from animora.dataviz.scatter_plot import ScatterPlot
from animora.dataviz.table import Table

__all__: list[str] = [
    "Axes",
    "BarChart",
    "Histogram",
    "LineChart",
    "ScatterPlot",
    "Table",
]
