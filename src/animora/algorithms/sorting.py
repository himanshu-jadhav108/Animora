"""Sorting algorithm visualizations and operation tracing for Array components."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from animora.algorithms.trace import OperationTrace, OperationType
from animora.core.animation import Animation
from animora.datastructures.array import Array
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Bubble Sort
# -----------------------------------------------------------------------------
def bubble_sort_trace(data: Sequence[Any]) -> tuple[list[Any], OperationTrace]:
    """Execute bubble sort, recording adjacent comparisons and swaps."""
    arr = list(data)
    trace = OperationTrace()
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            trace.add_step(
                OperationType.COMPARE,
                f"Compare adjacent elements at {j} ({arr[j]}) and {j + 1} ({arr[j + 1]})",
                targets=(j, j + 1),
            )
            if arr[j] > arr[j + 1]:
                trace.add_step(
                    OperationType.SWAP,
                    f"Swap {arr[j]} and {arr[j + 1]}",
                    targets=(j, j + 1),
                )
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr, trace


def bubble_sort(arr: Array, run_time: float | None = None) -> list[Animation]:
    """Generate animations for Bubble Sort on an Array."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    _, trace = bubble_sort_trace(arr.model.to_list())
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.COMPARE:
            i, j = step.targets
            animations.append(
                arr.animate_highlight(i, color=active_theme.colors.accent, run_time=duration)
            )
        elif step.op_type == OperationType.SWAP:
            i, j = step.targets
            animations.append(arr.animate_swap(i, j, run_time=duration))

    return animations


# -----------------------------------------------------------------------------
# 2. Selection Sort
# -----------------------------------------------------------------------------
def selection_sort_trace(data: Sequence[Any]) -> tuple[list[Any], OperationTrace]:
    """Execute selection sort, recording minimum scans and final swaps."""
    arr = list(data)
    trace = OperationTrace()
    n = len(arr)

    for i in range(n):
        min_idx = i
        trace.add_step(OperationType.HIGHLIGHT, f"Set current index {i} as minimum", targets=(i,))
        for j in range(i + 1, n):
            trace.add_step(
                OperationType.COMPARE,
                f"Compare candidate {j} ({arr[j]}) with current min {min_idx} ({arr[min_idx]})",
                targets=(j, min_idx),
            )
            if arr[j] < arr[min_idx]:
                min_idx = j
                trace.add_step(
                    OperationType.HIGHLIGHT,
                    f"New minimum found at {min_idx} ({arr[min_idx]})",
                    targets=(min_idx,),
                )

        if min_idx != i:
            trace.add_step(
                OperationType.SWAP,
                f"Swap minimum {arr[min_idx]} to index {i}",
                targets=(i, min_idx),
            )
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr, trace


def selection_sort(arr: Array, run_time: float | None = None) -> list[Animation]:
    """Generate animations for Selection Sort on an Array."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    _, trace = selection_sort_trace(arr.model.to_list())
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.HIGHLIGHT:
            idx = step.targets[0]
            animations.append(
                arr.animate_highlight(idx, color=active_theme.colors.warning, run_time=duration)
            )
        elif step.op_type == OperationType.SWAP:
            i, j = step.targets
            animations.append(arr.animate_swap(i, j, run_time=duration))

    return animations


# -----------------------------------------------------------------------------
# 3. Insertion Sort
# -----------------------------------------------------------------------------
def insertion_sort_trace(data: Sequence[Any]) -> tuple[list[Any], OperationTrace]:
    """Execute insertion sort, recording shift-back comparisons and placement."""
    arr = list(data)
    trace = OperationTrace()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        trace.add_step(OperationType.HIGHLIGHT, f"Selected key {key} at index {i}", targets=(i,))

        while j >= 0:
            trace.add_step(
                OperationType.COMPARE, f"Compare {key} with {arr[j]} at index {j}", targets=(i, j)
            )
            if arr[j] > key:
                trace.add_step(
                    OperationType.SET, f"Shift {arr[j]} to {j + 1}", targets=(j + 1,), value=arr[j]
                )
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        trace.add_step(
            OperationType.SET, f"Place key {key} at index {j + 1}", targets=(j + 1,), value=key
        )
        arr[j + 1] = key

    return arr, trace


def insertion_sort(arr: Array, run_time: float | None = None) -> list[Animation]:
    """Generate animations for Insertion Sort on an Array."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    _, trace = insertion_sort_trace(arr.model.to_list())
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.HIGHLIGHT:
            idx = step.targets[0]
            animations.append(
                arr.animate_highlight(idx, color=active_theme.colors.primary, run_time=duration)
            )
        elif step.op_type == OperationType.SET:
            idx = step.targets[0]
            val = step.metadata["value"]
            animations.append(arr.animate_set(idx, val, run_time=duration))

    return animations


# -----------------------------------------------------------------------------
# 4. Merge Sort
# -----------------------------------------------------------------------------
def merge_sort_trace(data: Sequence[Any]) -> tuple[list[Any], OperationTrace]:
    """Execute merge sort, recording divide steps and merge assignments."""
    arr = list(data)
    trace = OperationTrace()

    def _merge_sort_rec(left: int, right: int) -> None:
        if left >= right:
            return
        mid = (left + right) // 2
        trace.add_step(
            OperationType.HIGHLIGHT,
            f"Divide range [{left}, {right}] at mid {mid}",
            targets=(left, mid, right),
        )
        _merge_sort_rec(left, mid)
        _merge_sort_rec(mid + 1, right)

        # Merge
        merged: list[Any] = []
        i = left
        j = mid + 1

        while i <= mid and j <= right:
            trace.add_step(
                OperationType.COMPARE,
                f"Compare {arr[i]} at {i} with {arr[j]} at {j}",
                targets=(i, j),
            )
            if arr[i] <= arr[j]:
                merged.append(arr[i])
                i += 1
            else:
                merged.append(arr[j])
                j += 1

        while i <= mid:
            merged.append(arr[i])
            i += 1
        while j <= right:
            merged.append(arr[j])
            j += 1

        for idx, val in enumerate(merged):
            trace.add_step(
                OperationType.SET,
                f"Write merged value {val} at {left + idx}",
                targets=(left + idx,),
                value=val,
            )
            arr[left + idx] = val

    _merge_sort_rec(0, len(arr) - 1)
    return arr, trace


def merge_sort(arr: Array, run_time: float | None = None) -> list[Animation]:
    """Generate animations for Merge Sort on an Array."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    _, trace = merge_sort_trace(arr.model.to_list())
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.SET:
            idx = step.targets[0]
            val = step.metadata["value"]
            animations.append(arr.animate_set(idx, val, run_time=duration))

    return animations


# -----------------------------------------------------------------------------
# 5. Quick Sort
# -----------------------------------------------------------------------------
def quick_sort_trace(data: Sequence[Any]) -> tuple[list[Any], OperationTrace]:
    """Execute quick sort, recording pivot partitions and swaps."""
    arr = list(data)
    trace = OperationTrace()

    def _quick_sort_rec(low: int, high: int) -> None:
        if low >= high:
            return

        pivot = arr[high]
        trace.add_step(
            OperationType.HIGHLIGHT, f"Selected pivot {pivot} at index {high}", targets=(high,)
        )
        i = low - 1

        for j in range(low, high):
            trace.add_step(
                OperationType.COMPARE,
                f"Compare {arr[j]} at {j} with pivot {pivot}",
                targets=(j, high),
            )
            if arr[j] < pivot:
                i += 1
                if i != j:
                    trace.add_step(
                        OperationType.SWAP,
                        f"Swap {arr[i]} at {i} with {arr[j]} at {j}",
                        targets=(i, j),
                    )
                    arr[i], arr[j] = arr[j], arr[i]

        if i + 1 != high:
            trace.add_step(
                OperationType.SWAP,
                f"Place pivot {pivot} at partition boundary {i + 1}",
                targets=(i + 1, high),
            )
            arr[i + 1], arr[high] = arr[high], arr[i + 1]

        pivot_idx = i + 1
        _quick_sort_rec(low, pivot_idx - 1)
        _quick_sort_rec(pivot_idx + 1, high)

    _quick_sort_rec(0, len(arr) - 1)
    return arr, trace


def quick_sort(arr: Array, run_time: float | None = None) -> list[Animation]:
    """Generate animations for Quick Sort on an Array."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    _, trace = quick_sort_trace(arr.model.to_list())
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.HIGHLIGHT:
            idx = step.targets[0]
            animations.append(
                arr.animate_highlight(idx, color=active_theme.colors.accent, run_time=duration)
            )
        elif step.op_type == OperationType.SWAP:
            i, j = step.targets
            animations.append(arr.animate_swap(i, j, run_time=duration))

    return animations


__all__ = [
    "bubble_sort",
    "bubble_sort_trace",
    "insertion_sort",
    "insertion_sort_trace",
    "merge_sort",
    "merge_sort_trace",
    "quick_sort",
    "quick_sort_trace",
    "selection_sort",
    "selection_sort_trace",
]
