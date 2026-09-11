"""Shared OperationTrace data structure for algorithm visualization tracking.

Records discrete, atomic execution events emitted during algorithm runs,
enabling pure mathematical correctness verification, animation generation,
and pedagogical introspection without coupling to graphics rendering.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


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
    """A single atomic operation step executed by an algorithm.

    Attributes:
        op_type: Semantic categorization of the operation.
        description: Human-readable explanation of the step.
        targets: Indices, node identifiers, or keys affected by this step.
        metadata: Additional contextual properties (e.g. costs, bounds, values).
    """

    op_type: OperationType
    description: str
    targets: tuple[Any, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize operation step to a JSON-compatible dictionary."""
        return {
            "op_type": self.op_type.value,
            "description": self.description,
            "targets": list(self.targets),
            "metadata": dict(self.metadata),
        }


class OperationTrace:
    """Chronological record of atomic operations executed by an algorithm.

    Enables independent computational correctness testing, pedagogical narration,
    and reproducible animation playback.

    Example:
    ```python
    _, trace = bubble_sort_trace([4, 2, 1])
    print(trace.count(OperationType.SWAP))  # Total number of swaps
    swaps = trace.filter(OperationType.SWAP)
    ```
    """

    def __init__(self, steps: Sequence[OperationStep] | None = None) -> None:
        self._steps: list[OperationStep] = list(steps or [])

    def add_step(
        self,
        op_type: OperationType | str,
        description: str,
        targets: Sequence[Any] | None = None,
        **metadata: Any,
    ) -> OperationStep:
        """Record a new operation step in chronological order.

        Args:
            op_type: OperationType enum or matching string value.
            description: Narrative text describing what occurred.
            targets: Elements, indices, or keys affected.
            **metadata: Additional algorithmic variables (costs, bounds, etc.).

        Returns:
            The newly created and recorded OperationStep.
        """
        resolved_type = OperationType(op_type) if isinstance(op_type, str) else op_type
        step = OperationStep(
            op_type=resolved_type,
            description=description,
            targets=tuple(targets or ()),
            metadata=dict(metadata),
        )
        self._steps.append(step)
        return step

    def filter(self, op_type: OperationType | str) -> list[OperationStep]:
        """Return all steps matching the specified operation type."""
        resolved = OperationType(op_type) if isinstance(op_type, str) else op_type
        return [step for step in self._steps if step.op_type == resolved]

    def count(self, op_type: OperationType | str | None = None) -> int:
        """Return the count of steps matching op_type, or total steps if None."""
        if op_type is None:
            return len(self._steps)
        resolved = OperationType(op_type) if isinstance(op_type, str) else op_type
        return sum(1 for step in self._steps if step.op_type == resolved)

    def targets_for(self, op_type: OperationType | str) -> list[tuple[Any, ...]]:
        """Return the sequence of targets for all steps matching op_type."""
        return [step.targets for step in self.filter(op_type)]

    def summary(self) -> dict[str, int]:
        """Return a dictionary counting steps per operation type."""
        counts = Counter(step.op_type.value for step in self._steps)
        return dict(counts)

    def to_dict(self) -> list[dict[str, Any]]:
        """Serialize the entire trace to a list of step dictionaries."""
        return [step.to_dict() for step in self._steps]

    def __len__(self) -> int:
        return len(self._steps)

    def __getitem__(self, index: int) -> OperationStep:
        return self._steps[index]

    def __iter__(self) -> Iterator[OperationStep]:
        return iter(self._steps)

    @property
    def steps(self) -> list[OperationStep]:
        """Return list of recorded steps."""
        return list(self._steps)

    def __repr__(self) -> str:
        return f"<OperationTrace steps={len(self._steps)} summary={self.summary()}>"


# Public Alias
AlgorithmTrace = OperationTrace

__all__ = [
    "AlgorithmTrace",
    "OperationStep",
    "OperationTrace",
    "OperationType",
]
