"""Data Structure Walkthrough scene template for trees, graphs, and linear structures."""

from __future__ import annotations

from typing import Any

from animora.datastructures.bst import BST
from animora.templates.base import BaseTemplateScene


class DataStructureWalkthroughTemplate(BaseTemplateScene):
    """Template for demonstrating data structure operations and internal invariants.

    When to use this:
        Use this template when teaching data structure invariants, tree balancing,
        node traversal order, or heap bubbling with synchronized state commentary.

    Layout Architecture:
        - Top: Header & Operation Name
        - Center: Centered hierarchical or linked data structure component
        - Bottom: Contextual narration explaining pointer manipulations
    """

    def __init__(
        self,
        title: str = "Binary Search Tree Invariants",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.ds_title = title

    def construct_template(self) -> None:
        # 1. Header & Narration
        self.setup_header(self.ds_title)
        self.setup_footer_narrator("Constructing initial balanced BST...")

        # 2. Centered BST
        bst = BST([50, 25, 75, 10, 30])
        bst.move_to([0.0, 0.2, 0.0])
        self.play(bst.animate_create(run_time=0.8))

        # 3. Insertion walkthrough
        self.narrate("Inserting value 28: traversing 50 -> left (25) -> right (30)...")
        self.play(bst.animate_insert(28, run_time=0.8))

        self.narrate("Search for 75: checking root (50) -> right child found.")
        self.play(bst.animate_search(75, run_time=0.6))
        self.wait(0.5)


__all__ = [
    "DataStructureWalkthroughTemplate",
]
