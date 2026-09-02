"""Decision tree classifier model, visualizer, and one-call animation API."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.panel import Panel
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.layout.base import LayoutItem
from animora.layout.tree import TreeLayout
from animora.ml.base import MLComponent, MLTrace
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


@dataclass
class DecisionNode:
    """A node within a binary classification decision tree."""

    node_id: str
    is_leaf: bool
    samples: int
    impurity: float
    prediction: int
    feature_idx: int | None = None
    threshold: float | None = None
    left: DecisionNode | None = None
    right: DecisionNode | None = None


class DecisionTreeModel:
    """Mathematical Decision Tree builder calculating exact Gini impurity or entropy."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        y: Sequence[int] | np.ndarray,
        *,
        max_depth: int = 2,
        min_samples_split: int = 2,
        criterion: str = "gini",
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        self.y = np.asarray(y, dtype=int)
        self.max_depth = max(1, int(max_depth))
        self.min_samples_split = max(2, int(min_samples_split))
        self.criterion = criterion.lower()
        self.trace = MLTrace()
        self.root: DecisionNode | None = None

    def _compute_impurity(self, labels: np.ndarray) -> float:
        """Compute Gini impurity or Shannon entropy for a label subset."""
        if len(labels) == 0:
            return 0.0
        _, counts = np.unique(labels, return_counts=True)
        probs = counts / len(labels)
        if self.criterion == "entropy":
            return float(-np.sum(probs * np.log2(probs + 1e-9)))
        # Gini
        return float(1.0 - np.sum(probs**2))

    def _find_best_split(
        self, X_sub: np.ndarray, y_sub: np.ndarray
    ) -> tuple[int | None, float | None, float]:
        """Find the feature and threshold that maximizes impurity reduction."""
        n_samples, n_features = X_sub.shape
        parent_impurity = self._compute_impurity(y_sub)
        best_gain = -1.0
        best_feat: int | None = None
        best_thresh: float | None = None

        for feat_idx in range(n_features):
            values = np.sort(np.unique(X_sub[:, feat_idx]))
            thresholds = (values[:-1] + values[1:]) / 2.0

            for t in thresholds:
                left_mask = X_sub[:, feat_idx] <= t
                right_mask = ~left_mask
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                left_imp = self._compute_impurity(y_sub[left_mask])
                right_imp = self._compute_impurity(y_sub[right_mask])
                p_left = float(np.sum(left_mask) / n_samples)
                gain = parent_impurity - (p_left * left_imp + (1.0 - p_left) * right_imp)

                if gain > best_gain:
                    best_gain = gain
                    best_feat = feat_idx
                    best_thresh = float(t)

        return best_feat, best_thresh, best_gain

    def fit(self) -> DecisionNode:
        """Construct the decision tree recursively and record trace steps."""
        self.trace = MLTrace()
        node_counter = 0

        def build_node(X_sub: np.ndarray, y_sub: np.ndarray, depth: int) -> DecisionNode:
            nonlocal node_counter
            curr_id = f"node_{node_counter}"
            node_counter += 1

            n_samples = len(y_sub)
            impurity = self._compute_impurity(y_sub)
            vals, counts = np.unique(y_sub, return_counts=True)
            prediction = int(vals[np.argmax(counts)])

            # Check stopping criteria
            if depth >= self.max_depth or n_samples < self.min_samples_split or impurity < 1e-6:
                leaf = DecisionNode(
                    node_id=curr_id,
                    is_leaf=True,
                    samples=n_samples,
                    impurity=impurity,
                    prediction=prediction,
                )
                self.trace.record(
                    name="leaf",
                    description=f"Leaf {curr_id}: class={prediction}, samples={n_samples}",
                    node_id=curr_id,
                    is_leaf=True,
                    prediction=prediction,
                )
                return leaf

            best_feat, best_thresh, gain = self._find_best_split(X_sub, y_sub)
            if best_feat is None or best_thresh is None or gain <= 0:
                leaf = DecisionNode(
                    node_id=curr_id,
                    is_leaf=True,
                    samples=n_samples,
                    impurity=impurity,
                    prediction=prediction,
                )
                return leaf

            desc = f"Split {curr_id}: X[{best_feat}] <= {best_thresh:.2f}, gain={gain:.3f}"
            self.trace.record(
                name="split",
                description=desc,
                node_id=curr_id,
                feature=best_feat,
                threshold=best_thresh,
                gain=gain,
            )

            left_mask = X_sub[:, best_feat] <= best_thresh
            left_child = build_node(X_sub[left_mask], y_sub[left_mask], depth + 1)
            right_child = build_node(X_sub[~left_mask], y_sub[~left_mask], depth + 1)

            return DecisionNode(
                node_id=curr_id,
                is_leaf=False,
                samples=n_samples,
                impurity=impurity,
                prediction=prediction,
                feature_idx=best_feat,
                threshold=best_thresh,
                left=left_child,
                right=right_child,
            )

        self.root = build_node(self.X, self.y, depth=0)
        return self.root


class DecisionTreeVisualizer(MLComponent):
    """Visualizes a decision tree graph using Phase 4 TreeLayout and Panels."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        y: Sequence[int] | np.ndarray,
        *,
        max_depth: int = 2,
        criterion: str = "gini",
        feature_names: Sequence[str] | None = None,
        class_names: Sequence[str] | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.model = DecisionTreeModel(X, y, max_depth=max_depth, criterion=criterion)
        self.root = self.model.fit()
        self.feature_names = list(feature_names) if feature_names is not None else None
        self.class_names = list(class_names) if class_names is not None else None

        self.nodes_map: dict[str, DecisionNode] = {}
        self.edges: list[tuple[str, str]] = []
        self._collect_tree_structure(self.root)

        super().__init__(config=config, **kwargs)

    def _collect_tree_structure(self, node: DecisionNode) -> None:
        self.nodes_map[node.node_id] = node
        if not node.is_leaf:
            if node.left:
                self.edges.append((node.node_id, node.left.node_id))
                self._collect_tree_structure(node.left)
            if node.right:
                self.edges.append((node.node_id, node.right.node_id))
                self._collect_tree_structure(node.right)

    def _create_node_card(self, node: DecisionNode) -> Panel:
        """Create a styled Panel card representing the decision node."""
        active_theme = get_active_theme()
        if node.is_leaf:
            pred_name = (
                self.class_names[node.prediction]
                if self.class_names and node.prediction < len(self.class_names)
                else f"Class {node.prediction}"
            )
            title = f"Leaf: {pred_name}"
            body_txt = Text(
                f"samples: {node.samples}\nimp: {node.impurity:.2f}",
                font_size=13,
                color=active_theme.colors.text_muted,
            )
        else:
            if (
                self.feature_names
                and node.feature_idx is not None
                and node.feature_idx < len(self.feature_names)
            ):
                feat_name = self.feature_names[node.feature_idx]
            else:
                feat_name = f"X[{node.feature_idx}]"
            title = f"{feat_name} <= {node.threshold:.2f}"
            body_txt = Text(
                f"samples: {node.samples}\nimp: {node.impurity:.2f}",
                font_size=13,
                color=active_theme.colors.text_muted,
            )

        card = Panel(
            body_txt,
            title=title,
            padding=0.15,
            width=2.1,
            height=1.1,
        )
        return card

    def _build_mobject(self) -> manim.Mobject:
        # Solve layout positions via TreeLayout
        layout_items = [LayoutItem(id=node_id, width=2.1, height=1.1) for node_id in self.nodes_map]
        layout = TreeLayout(
            edges=self.edges,
            root_id=self.root.node_id,
            node_spacing=1.2,
            level_spacing=1.6,
        )
        result = layout.solve(layout_items)

        group = manim.VGroup()
        node_positions = result.positions

        # Draw connecting branch lines
        for parent_id, child_id in self.edges:
            p_pos = node_positions[parent_id]
            c_pos = node_positions[child_id]
            line = manim.Line(p_pos, c_pos, color="#64748B", stroke_width=2.0)
            group.add(line)

        # Draw node cards
        for node_id, node in self.nodes_map.items():
            card = self._create_node_card(node)
            card.move_to(node_positions[node_id])
            group.add(card.manim_object)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generating tree branches and decision nodes."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        layout_items = [LayoutItem(id=node_id, width=2.1, height=1.1) for node_id in self.nodes_map]
        layout = TreeLayout(
            edges=self.edges,
            root_id=self.root.node_id,
            node_spacing=1.2,
            level_spacing=1.6,
        )
        result = layout.solve(layout_items)
        node_positions = result.positions

        # 1. Animate root
        root_card = self._create_node_card(self.root)
        root_card.move_to(node_positions[self.root.node_id])
        animations.append(root_card.animate_create(run_time=0.6))

        # 2. Animate branches and children level-by-level
        for parent_id, child_id in self.edges:
            p_pos = node_positions[parent_id]
            c_pos = node_positions[child_id]
            child_node = self.nodes_map[child_id]
            child_card = self._create_node_card(child_node)
            child_card.move_to(c_pos)

            branch_line = manim.Line(
                p_pos, c_pos, color=active_theme.colors.border, stroke_width=2.0
            )

            branch_anim = manim.AnimationGroup(
                manim.Create(branch_line),
                child_card.animate_create().to_manim(),
            )
            animations.append(
                Animation(
                    component=self,
                    manim_animation=branch_anim,
                    run_time=0.5,
                    name=f"split_to_{child_id}",
                )
            )

        return animations


def decision_tree(
    X: Sequence[Sequence[float]] | np.ndarray,
    y: Sequence[int] | np.ndarray,
    *,
    max_depth: int = 2,
    criterion: str = "gini",
    feature_names: Sequence[str] | None = None,
    class_names: Sequence[str] | None = None,
) -> list[Animation]:
    """One-call functional API to animate decision tree building."""
    viz = DecisionTreeVisualizer(
        X,
        y,
        max_depth=max_depth,
        criterion=criterion,
        feature_names=feature_names,
        class_names=class_names,
    )
    return viz.animate()


__all__ = [
    "DecisionNode",
    "DecisionTreeModel",
    "DecisionTreeVisualizer",
    "decision_tree",
]
