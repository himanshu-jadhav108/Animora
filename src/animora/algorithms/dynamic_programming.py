"""Dynamic Programming visualization with animated memoization table filling."""

from __future__ import annotations

from typing import TYPE_CHECKING

from animora.algorithms.trace import OperationTrace, OperationType
from animora.core.animation import Animation
from animora.dataviz.table import Table
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Algorithm Logic with Operation Tracing (Dual-Correctness)
# -----------------------------------------------------------------------------
def fibonacci_dp_trace(n: int) -> tuple[int, list[int], OperationTrace]:
    """Compute N-th Fibonacci number using bottom-up DP, recording cell fills."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        trace = OperationTrace()
        trace.add_step(OperationType.TABLE_FILL, "Base case: dp[0] = 0", targets=(0,), value=0)
        return 0, [0], trace

    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1

    trace = OperationTrace()
    trace.add_step(OperationType.TABLE_FILL, "Base case: dp[0] = 0", targets=(0,), value=0)
    trace.add_step(OperationType.TABLE_FILL, "Base case: dp[1] = 1", targets=(1,), value=1)

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        trace.add_step(
            OperationType.TABLE_FILL,
            f"Compute dp[{i}] = dp[{i - 1}] ({dp[i - 1]}) + dp[{i - 2}] ({dp[i - 2]}) = {dp[i]}",
            targets=(i,),
            value=dp[i],
            operand_a=dp[i - 1],
            operand_b=dp[i - 2],
        )

    return dp[n], dp, trace


# -----------------------------------------------------------------------------
# 2. Animation Generator Orchestration
# -----------------------------------------------------------------------------
def fibonacci_dp(
    n: int,
    table: Table | None = None,
    run_time: float | None = None,
) -> list[Animation]:
    """Generate animations filling a Table component cell-by-cell for DP Fibonacci."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    _result, _dp_array, trace = fibonacci_dp_trace(n)
    animations: list[Animation] = []

    if table is not None:
        for step in trace:
            idx = step.targets[0]
            if idx < table.num_cols:
                # Row 1 is the DP values row (Row 0 is header)
                anim = table.animate_highlight_cell(
                    1, idx, color=active_theme.colors.success, run_time=duration
                )
                animations.append(anim)

    return animations


__all__ = [
    "fibonacci_dp",
    "fibonacci_dp_trace",
]
