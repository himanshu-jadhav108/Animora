"""Binary search algorithm visualization and operation tracing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

from animora.algorithms.trace import OperationTrace, OperationType
from animora.core.animation import Animation
from animora.datastructures.array import Array
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Algorithm Logic with Operation Tracing (Dual-Correctness)
# -----------------------------------------------------------------------------
def binary_search_trace(data: Sequence[Any], target: Any) -> tuple[int, OperationTrace]:
    """Execute binary search, returning (found_index, operation_trace)."""
    trace = OperationTrace()
    low = 0
    high = len(data) - 1

    while low <= high:
        mid = (low + high) // 2
        trace.add_step(
            OperationType.COMPARE,
            f"Comparing mid element at index {mid} ({data[mid]}) with target ({target})",
            targets=(low, mid, high),
            low=low,
            mid=mid,
            high=high,
            value=data[mid],
        )

        if data[mid] == target:
            trace.add_step(
                OperationType.HIGHLIGHT,
                f"Target {target} found at index {mid}",
                targets=(mid,),
                found=True,
                index=mid,
            )
            return mid, trace
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    trace.add_step(
        OperationType.HIGHLIGHT,
        f"Target {target} not found in array",
        targets=(),
        found=False,
    )
    return -1, trace


# -----------------------------------------------------------------------------
# 2. Animation Generator Orchestration
# -----------------------------------------------------------------------------
def binary_search(
    arr: Array,
    target: Any,
    run_time: float | None = None,
) -> list[Animation]:
    """Generate sequential animations visualizing binary search over the Array component."""
    active_theme = get_active_theme()
    step_duration = run_time or active_theme.timing.normal

    _, trace = binary_search_trace(arr.model.to_list(), target)
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.COMPARE:
            mid = step.metadata["mid"]
            anim = arr.animate_highlight(mid, color=active_theme.colors.accent, run_time=step_duration)
            animations.append(anim)
        elif step.op_type == OperationType.HIGHLIGHT:
            if step.metadata.get("found"):
                idx = step.metadata["index"]
                anim = arr.animate_highlight(idx, color=active_theme.colors.success, run_time=step_duration)
                animations.append(anim)

    return animations


__all__ = [
    "binary_search",
    "binary_search_trace",
]
