"""HashTable data structure component using Separate Chaining collision strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
import manim

from animora.components.arrow import Arrow
from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (Separate Chaining Collision Strategy)
# -----------------------------------------------------------------------------
class HashEntry:
    """Key-value entry in a collision chain."""

    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value


class HashTableChainingModel:
    """Pure Python HashTable model using Separate Chaining for collision resolution.

    Collision Strategy Justification:
    Separate Chaining stores colliding entries in linked overflow lists per bucket.
    This provides an intuitive, explicit 2D visual representation (buckets x chains)
    ideal for educational demonstrations.
    """

    def __init__(self, num_buckets: int = 5) -> None:
        self.num_buckets: int = max(1, num_buckets)
        self.buckets: list[list[HashEntry]] = [[] for _ in range(self.num_buckets)]

    def hash_key(self, key: Any) -> int:
        """Compute bucket index for given key."""
        if isinstance(key, int):
            return key % self.num_buckets
        return abs(hash(str(key))) % self.num_buckets

    def insert(self, key: Any, value: Any) -> tuple[int, int]:
        """Insert or update (key, value). Returns (bucket_index, chain_position)."""
        idx = self.hash_key(key)
        chain = self.buckets[idx]

        for pos, entry in enumerate(chain):
            if entry.key == key:
                entry.value = value
                return idx, pos

        chain.append(HashEntry(key, value))
        return idx, len(chain) - 1

    def search(self, key: Any) -> tuple[bool, int, int, Any]:
        """Search key. Returns (found, bucket_idx, chain_pos, value)."""
        idx = self.hash_key(key)
        chain = self.buckets[idx]

        for pos, entry in enumerate(chain):
            if entry.key == key:
                return True, idx, pos, entry.value

        return False, idx, -1, None

    def delete(self, key: Any) -> tuple[bool, int, int]:
        """Delete key. Returns (deleted, bucket_idx, chain_pos)."""
        idx = self.hash_key(key)
        chain = self.buckets[idx]

        for pos, entry in enumerate(chain):
            if entry.key == key:
                chain.pop(pos)
                return True, idx, pos

        return False, idx, -1

    def to_dict(self) -> dict[Any, Any]:
        """Convert all stored entries to a standard Python dictionary."""
        result: dict[Any, Any] = {}
        for chain in self.buckets:
            for entry in chain:
                result[entry.key] = entry.value
        return result


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class HashTable(Component):
    """Visual HashTable component with separate chaining visualization.

    Example:
    ```python
    ht = HashTable(num_buckets=5)
    scene.play(ht.animate_insert("apple", 100))
    scene.play(ht.animate_insert("banana", 200))
    scene.play(ht.animate_search("apple"))
    ```
    """

    def __init__(
        self,
        num_buckets: int = 5,
        *,
        bucket_width: float = 1.4,
        bucket_height: float = 0.7,
        chain_spacing: float = 1.5,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = HashTableChainingModel(num_buckets)
        self._bucket_width = float(bucket_width)
        self._bucket_height = float(bucket_height)
        self._chain_spacing = float(chain_spacing)

        self._bucket_groups: list[Group] = []
        self._chain_nodes: list[list[Group]] = []
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> HashTableChainingModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Build vertical buckets array and horizontal chain nodes."""
        active_theme = get_active_theme()

        self._bucket_groups = []
        self._chain_nodes = [[] for _ in range(self._model.num_buckets)]
        all_mobjects: list[manim.Mobject] = []

        total_h = self._model.num_buckets * (self._bucket_height + 0.15)
        top_y = total_h / 2.0

        for b_idx in range(self._model.num_buckets):
            y = top_y - (b_idx * (self._bucket_height + 0.15))
            b_box = Shape.rounded_rectangle(
                width=self._bucket_width,
                height=self._bucket_height,
                corner_radius=0.08,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.primary,
            ).move_to([-3.0, y, 0.0])

            b_lbl = Text(f"[{b_idx}]", font_size=active_theme.typography.font_size_sm, color=active_theme.colors.primary).move_to(b_box.center)
            b_grp = Group(b_box, b_lbl)
            self._bucket_groups.append(b_grp)
            all_mobjects.append(b_grp.manim_object)

            # Build chain nodes horizontally
            prev_center = b_box.center
            for c_idx, entry in enumerate(self._model.buckets[b_idx]):
                cx = prev_center[0] + self._chain_spacing
                c_box = Shape.rounded_rectangle(
                    width=self._bucket_width * 1.1,
                    height=self._bucket_height * 0.9,
                    corner_radius=0.08,
                    fill_color=active_theme.colors.secondary,
                    fill_opacity=0.85,
                    stroke_color=active_theme.colors.border,
                ).move_to([cx, y, 0.0])

                c_txt = Text(f"{entry.key}:{entry.value}", font_size=active_theme.typography.font_size_xs, color="#FFFFFF").move_to([cx, y, 0.0])
                c_grp = Group(c_box, c_txt)
                self._chain_nodes[b_idx].append(c_grp)
                all_mobjects.append(c_grp.manim_object)

                # Arrow connecting previous item to this chain entry
                arr = Arrow(start=prev_center, end=[cx, y, 0.0], buff=self._bucket_width / 2.0 + 0.1)
                all_mobjects.append(arr.manim_object)
                prev_center = [cx, y, 0.0]

        return manim.VGroup(*all_mobjects)

    def animate_insert(
        self,
        key: Any,
        value: Any,
        run_time: float | None = None,
    ) -> Animation:
        """Insert key-value pair and animate bucket highlight and chain entry."""
        b_idx, c_pos = self._model.insert(key, value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        b_grp = self._bucket_groups[b_idx]
        return Animation(
            component=b_grp,
            manim_animation=manim.Indicate(b_grp.manim_object, color=active_theme.colors.accent),
            run_time=duration,
            name=f"insert({key}, {value}) -> bucket={b_idx}",
        )

    def animate_search(
        self,
        key: Any,
        run_time: float | None = None,
    ) -> Animation:
        """Search key and animate target bucket highlight."""
        found, b_idx, c_pos, val = self._model.search(key)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        target_col = active_theme.colors.success if found else active_theme.colors.error
        b_grp = self._bucket_groups[b_idx]

        return Animation(
            component=b_grp,
            manim_animation=manim.Indicate(b_grp.manim_object, color=target_col),
            run_time=duration,
            name=f"search({key}) -> found={found}",
        )


__all__ = [
    "HashEntry",
    "HashTable",
    "HashTableChainingModel",
]
