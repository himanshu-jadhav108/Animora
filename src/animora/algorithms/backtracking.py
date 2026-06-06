"""Backtracking algorithm visualization with animated state decision trees (N-Queens)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from animora.algorithms.trace import OperationTrace, OperationType
from animora.core.animation import Animation
from animora.dataviz.table import Table
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Algorithm Logic with Operation Tracing (Dual-Correctness)
# -----------------------------------------------------------------------------
def n_queens_trace(n: int = 4) -> tuple[list[list[int]], OperationTrace]:
    """Solve N-Queens backtracking problem, recording placements and backtracks.

    Returns (solutions, operation_trace) where each solution is a list of column
    indices for each row.
    """
    trace = OperationTrace()
    solutions: list[list[int]] = []
    board: list[int] = [-1] * n

    def _is_safe(row: int, col: int) -> bool:
        for prev_row in range(row):
            prev_col = board[prev_row]
            # Column conflict or diagonal conflict
            if prev_col == col or abs(prev_col - col) == abs(prev_row - row):
                return False
        return True

    def _solve(row: int) -> None:
        if row == n:
            solutions.append(list(board))
            trace.add_step(
                OperationType.HIGHLIGHT,
                f"Valid N-Queens solution found: {list(board)}",
                targets=tuple(enumerate(board)),
                solution=list(board),
            )
            return

        for col in range(n):
            trace.add_step(
                OperationType.TRY_CHOICE,
                f"Try placing Queen at row {row}, column {col}",
                targets=(row, col),
                row=row,
                col=col,
            )

            if _is_safe(row, col):
                board[row] = col
                _solve(row + 1)
                # Backtrack
                board[row] = -1
                trace.add_step(
                    OperationType.BACKTRACK,
                    f"Backtrack from row {row}, column {col}",
                    targets=(row, col),
                    row=row,
                    col=col,
                )
            else:
                trace.add_step(
                    OperationType.BACKTRACK,
                    f"Conflict detected at row {row}, column {col}",
                    targets=(row, col),
                    row=row,
                    col=col,
                )

    _solve(0)
    return solutions, trace


# -----------------------------------------------------------------------------
# 2. Animation Generator Orchestration
# -----------------------------------------------------------------------------
def n_queens(
    n: int = 4,
    table: Table | None = None,
    run_time: float | None = None,
) -> list[Animation]:
    """Generate animations for N-Queens backtracking exploration."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.fast

    solutions, trace = n_queens_trace(n)
    animations: list[Animation] = []

    if table is not None:
        for step in trace:
            if step.op_type == OperationType.TRY_CHOICE:
                r, c = step.targets
                anim = table.animate_highlight_cell(r, c, color=active_theme.colors.warning, run_time=duration)
                animations.append(anim)
            elif step.op_type == OperationType.BACKTRACK:
                r, c = step.targets
                anim = table.animate_highlight_cell(r, c, color=active_theme.colors.error, run_time=duration)
                animations.append(anim)
            elif step.op_type == OperationType.HIGHLIGHT:
                for r, c in step.targets:
                    anim = table.animate_highlight_cell(r, c, color=active_theme.colors.success, run_time=duration)
                    animations.append(anim)

    return animations


__all__ = [
    "n_queens",
    "n_queens_trace",
]
