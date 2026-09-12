"""Example 12: Educational Annotation & Callouts System.

Demonstrates attaching semantic callouts, indicators, and pointer arrows to
individual elements in data structures and shapes.
"""

from __future__ import annotations

import manim

from animora.core import Scene
from animora.datastructures import BST, Array
from animora.theme import ModernDark, use_theme


class AnnotationDemoScene(Scene):
    """Educational walkthrough illustrating manual callouts on Array and BST."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Array with Pivot and Swapped Element Annotations
            arr = Array([42, 17, 95, 33, 61])
            arr.move_to([0.0, 1.8, 0.0])
            self.play(arr.animate_create())

            # Annotate maximum element at index 2
            self.play(arr.annotate(2, text="Max Element (95)", direction=manim.UP, box=True))
            self.wait(0.5)

            # 2. BST with Root and Traversal Annotations
            bst = BST([50, 25, 75, 12, 37])
            bst.move_to([0.0, -1.2, 0.0])
            self.play(bst.animate_create())

            # Annotate BST root node
            self.play(bst.annotate(50, text="Root Node", direction=manim.UP, arrow=True))

            # Annotate leaf node
            self.play(bst.annotate(12, text="Leftmost Leaf", direction=manim.DOWN, box=True))
            self.wait(0.5)


if __name__ == "__main__":
    scene = AnnotationDemoScene()
    scene.render()
