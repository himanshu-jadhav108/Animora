"""Example 05: Data Structures (Binary Search Tree with tracked operations)."""

from __future__ import annotations

from animora.core import Scene
from animora.datastructures import BST
from animora.theme import ModernDark, use_theme


class BSTDataStructureScene(Scene):
    """Demonstrates stateful Binary Search Tree insert, search, and delete animations."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Initialize BST
            bst = BST([50, 30, 70, 20, 40])
            self.play(bst.animate_create(run_time=0.8))
            self.wait(0.3)

            # 2. Insert new value (traces comparison path 50 -> 30 -> 40 before placement)
            self.play(bst.animate_insert(35, run_time=1.0))
            self.wait(0.3)

            # 3. Search value
            self.play(bst.animate_search(35, run_time=0.8))
            self.wait(0.5)


if __name__ == "__main__":
    import manim
    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = BSTDataStructureScene()
        scene.render()
