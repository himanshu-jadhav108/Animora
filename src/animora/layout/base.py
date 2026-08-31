"""Base data contracts and abstract layout solver interface for Animora."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LayoutItem:
    """Represents an abstract measurable item to be positioned by a layout solver.

    Completely decoupled from Manim and Component instances.
    """

    id: str
    width: float
    height: float
    depth: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LayoutResult:
    """Computed 3D coordinates resulting from a layout solver execution."""

    positions: dict[str, tuple[float, float, float]]
    total_width: float = 0.0
    total_height: float = 0.0

    def get(
        self, item_id: str, default: tuple[float, float, float] = (0.0, 0.0, 0.0)
    ) -> tuple[float, float, float]:
        """Get the 3D position vector for a specific item id."""
        return self.positions.get(item_id, default)

    def __getitem__(self, item_id: str) -> tuple[float, float, float]:
        return self.positions[item_id]

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.positions


class BaseLayout(ABC):
    """Abstract base class for all geometric layout solvers."""

    @abstractmethod
    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        """Compute 3D center positions for the given sequence of items."""
        raise NotImplementedError


__all__ = [
    "BaseLayout",
    "LayoutItem",
    "LayoutResult",
]
