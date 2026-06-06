"""Shared OperationTrace data structure for algorithm visualization tracking."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Sequence


class OperationType(str, Enum):
    """Categorization of discrete algorithm execution events."""

    COMPARE = "compare"
    SWAP = "swap"
    SET = "set"
    HIGHLIGHT = "highlight"
    VISIT_NODE = "visit_node"
    HIGHLIGHT_EDGE = "highlight_edge"
    RELAX_EDGE = "relax_edge"
    TABLE_FILL = "table_fill"
    TRY_CHOICE = "try_choice"
    BACKTRACK = "backtrack"


@dataclass(frozen=True)
class OperationStep:
    """A single atomic step executed by an algorithm."""

    op_type: OperationType
    description: str
    targets: tuple[Any, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


class OperationTrace:
    """Chronological record of atomic operations executed by an algorithm.

    Enables independent computational correctness testing and reproducible
    animation playback.
    """

    def __init__(self, steps: Sequence[OperationStep] | None = None) -> None:
        self._steps: list[OperationStep] = list(steps or [])

    def add_step(
        self,
        op_type: OperationType,
        description: str,
        targets: Sequence[Any] | None = None,
        **metadata: Any,
    ) -> OperationStep:
        """Record a new operation step."""
        step = OperationStep(
            op_type=op_type,
            description=description,
            targets=tuple(targets or ()),
            metadata=dict(metadata),
        )
        self._steps.append(step)
        return step

    def __len__(self) -> int:
        return len(self._steps)

    def __getitem__(self, index: int) -> OperationStep:
        return self._steps[index]

    def __iter__(self):
        return iter(self._steps)

    @property
    def steps(self) -> list[OperationStep]:
        """Return list of recorded steps."""
        return list(self._steps)


__all__ = [
    "OperationStep",
    "OperationTrace",
    "OperationType",
]
