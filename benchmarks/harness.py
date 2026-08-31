"""Automated benchmarking harness for Animora."""

from __future__ import annotations

import argparse
import gc
import sys
import time
import tracemalloc
from collections.abc import Callable

import manim
from benchmarks.scenarios.stress_scenes import (
    LargeArrayStressScene,
    LargeGridStressScene,
    LargeTreeStressScene,
)

from animora.algorithms.sorting import (
    merge_sort_trace,
    quick_sort_trace,
)
from animora.components.shape import Shape
from animora.layout.base import LayoutItem
from animora.layout.circular import CircularLayout
from animora.layout.flow import FlowLayout
from animora.layout.grid import GridLayout
from animora.layout.horizontal import HorizontalLayout
from animora.layout.vertical import VerticalLayout


def benchmark_function(func: Callable[[], None], iterations: int = 10) -> tuple[float, float]:
    """Measure execution time (ms) and peak memory delta (KB)."""
    gc.collect()
    tracemalloc.start()

    start_time = time.perf_counter()
    for _ in range(iterations):
        func()
    end_time = time.perf_counter()

    _current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    avg_time_ms = ((end_time - start_time) / iterations) * 1000.0
    peak_mem_kb = peak_mem / 1024.0
    return avg_time_ms, peak_mem_kb


def run_benchmarks() -> dict[str, dict[str, float]]:
    """Execute all benchmark suites and return results dictionary."""
    results: dict[str, dict[str, float]] = {}

    # 1. Component Construction
    def construct_100_shapes() -> None:
        shapes = [Shape.circle(radius=0.5) for _ in range(100)]
        assert len(shapes) == 100

    t_ms, mem_kb = benchmark_function(construct_100_shapes, iterations=20)
    results["Component Construction (100 shapes)"] = {"Time (ms)": t_ms, "Peak Mem (KB)": mem_kb}

    # 2. Layout Solvers at N=100
    items_100 = [LayoutItem(width=1.0, height=1.0) for _ in range(100)]

    for name, layout_solver in [
        ("HorizontalLayout (N=100)", HorizontalLayout()),
        ("VerticalLayout (N=100)", VerticalLayout()),
        ("GridLayout (N=100)", GridLayout(columns=10)),
        ("CircularLayout (N=100)", CircularLayout(radius=5.0)),
        ("FlowLayout (N=100)", FlowLayout()),
    ]:
        t_ms, mem_kb = benchmark_function(
            lambda ls=layout_solver: ls.solve(items_100), iterations=50
        )
        results[f"Layout: {name}"] = {"Time (ms)": t_ms, "Peak Mem (KB)": mem_kb}

    # 3. Algorithm Trace Generation
    data_100 = list(range(100, 0, -1))
    t_ms, mem_kb = benchmark_function(lambda: quick_sort_trace(data_100), iterations=50)
    results["Algorithm: QuickSort Trace (N=100)"] = {"Time (ms)": t_ms, "Peak Mem (KB)": mem_kb}

    t_ms, mem_kb = benchmark_function(lambda: merge_sort_trace(data_100), iterations=50)
    results["Algorithm: MergeSort Trace (N=100)"] = {"Time (ms)": t_ms, "Peak Mem (KB)": mem_kb}

    # 4. Stress Scenes End-to-End Rendering
    def render_stress_scenes() -> None:
        with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
            s1 = LargeArrayStressScene()
            s1.render()
            s2 = LargeTreeStressScene()
            s2.render()
            s3 = LargeGridStressScene()
            s3.render()

    t_ms, mem_kb = benchmark_function(render_stress_scenes, iterations=3)
    results["Stress Scenes Composite Dry-Run"] = {"Time (ms)": t_ms, "Peak Mem (KB)": mem_kb}

    return results


def print_report(results: dict[str, dict[str, float]]) -> None:
    """Print formatted benchmark table."""
    print("=" * 80)
    print(f"{'Benchmark Category / Scenario':<45} | {'Avg Time (ms)':<15} | {'Peak Mem (KB)':<15}")
    print("=" * 80)
    for name, metrics in results.items():
        print(f"{name:<45} | {metrics['Time (ms)']:<15.3f} | {metrics['Peak Mem (KB)']:<15.1f}")
    print("=" * 80)


def main() -> int:
    parser = argparse.ArgumentParser(description="Animora Performance Benchmark Harness")
    parser.add_argument("--report", action="store_true", help="Print benchmark summary report")
    parser.parse_args()

    results = run_benchmarks()
    print_report(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
