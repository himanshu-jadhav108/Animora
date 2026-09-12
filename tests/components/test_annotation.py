"""Unit tests for the manual annotation system (Annotation component and Component.annotate)."""

from __future__ import annotations

import manim
import numpy as np

from animora.components.annotation import Annotation
from animora.components.shape import Shape
from animora.core.animation import Animation
from animora.core.scene import Scene
from animora.datastructures.array import Array
from animora.datastructures.bst import BST
from animora.datastructures.graph import Graph


def test_annotation_standalone_construction() -> None:
    """Verify standalone Annotation creation and geometric positioning."""
    circle = Shape.circle(radius=0.5).move_to([0.0, 0.0, 0.0])
    ann = Annotation(
        circle,
        text="Target Circle",
        direction=manim.UP,
        buff=0.5,
        arrow=True,
        box=True,
    )

    assert ann.text == "Target Circle"
    assert ann.target is circle

    # Realize visual objects
    mob = ann.manim_object
    assert isinstance(mob, manim.VGroup)
    assert ann.content_component is not None
    assert ann.arrow_component is not None

    # Content should be positioned above circle
    assert ann.content_component.center[1] > circle.center[1]


def test_annotation_returns_animation() -> None:
    """Verify animate_create and animate_fade_out return valid Animora Animations."""
    circle = Shape.circle(radius=0.5)
    ann = Annotation(circle, text="Sample", arrow=False, box=False)

    anim_create = ann.animate_create(run_time=0.8)
    assert isinstance(anim_create, Animation)
    assert anim_create.component is ann
    assert anim_create.run_time == 0.8
    assert anim_create.to_manim() is not None

    anim_fade = ann.animate_fade_out()
    assert isinstance(anim_fade, Animation)
    assert anim_fade.to_manim() is not None


def test_lazy_build_resilience_array() -> None:
    """Verify Array.annotate works BEFORE Array.manim_object is ever accessed (BUG-001 guard)."""
    # Create array without touching .manim_object
    arr = Array([10, 20, 30, 40])
    assert arr._mobject is None

    # Call annotate directly on unbuilt array index
    anim = arr.annotate(1, text="Second Element", direction=manim.DOWN, buff=0.4)
    assert isinstance(anim, Animation)
    assert isinstance(anim.component, Annotation)

    ann: Annotation = anim.component
    # Accessing annotation should build both array and annotation correctly
    _ = ann.manim_object
    assert arr._mobject is not None
    assert ann.content_component is not None
    assert ann.content_component.center[1] < arr.center[1]


def test_lazy_build_resilience_bst() -> None:
    """Verify BST.annotate works BEFORE BST.manim_object is ever accessed (BUG-001 guard)."""
    # Create BST without touching .manim_object
    bst = BST([50, 25, 75])
    assert bst._mobject is None

    # Call annotate directly on node value
    anim = bst.annotate(25, text="Left Subtree", direction=manim.LEFT, buff=0.5)
    assert isinstance(anim, Animation)
    assert isinstance(anim.component, Annotation)

    ann: Annotation = anim.component
    _ = ann.manim_object
    assert bst._mobject is not None
    assert ann.content_component is not None


def test_lazy_build_resilience_graph() -> None:
    """Verify Graph.annotate works BEFORE Graph.manim_object is ever accessed."""
    graph = Graph(nodes=["A", "B", "C"], edges=[("A", "B"), ("B", "C")])
    assert graph._mobject is None

    anim = graph.annotate("B", text="Hub Node", direction=manim.UP)
    assert isinstance(anim, Animation)
    assert isinstance(anim.component, Annotation)

    ann: Annotation = anim.component
    _ = ann.manim_object
    assert graph._mobject is not None


def test_component_annotate_direct() -> None:
    """Verify Component.annotate on primitive shape with string shortcut."""
    rect = Shape.rectangle(width=2.0, height=1.0)
    # Positional string invocation
    anim = rect.annotate("Framed Rectangle", direction=manim.RIGHT, buff=0.3)
    assert isinstance(anim, Animation)

    ann = anim.component
    assert isinstance(ann, Annotation)
    assert ann.text == "Framed Rectangle"
    assert ann.content_component.center[0] > rect.center[0]


def test_annotation_options_box_and_arrow() -> None:
    """Verify box and arrow toggle options affect components."""
    point = np.array([1.0, 1.0, 0.0])

    # No arrow, with box
    ann_box = Annotation(point, "Boxed", arrow=False, box=True)
    _ = ann_box.manim_object
    assert ann_box.arrow_component is None
    assert ann_box.content_component is not None

    # With arrow, no box
    ann_arrow = Annotation(point, "Plain Arrow", arrow=True, box=False)
    _ = ann_arrow.manim_object
    assert ann_arrow.arrow_component is not None


def test_annotation_scene_render_dry_run() -> None:
    """Verify end-to-end rendering of annotations across Array and BST in Scene."""

    class AnnotationDemoScene(Scene):
        def construct(self) -> None:
            arr = Array([15, 30, 45])
            self.play(arr.animate_create())
            self.play(arr.annotate(0, text="First", direction=manim.UP))

            bst = BST([50, 20, 80])
            bst.move_to([0.0, -1.5, 0.0])
            self.play(bst.animate_create())
            self.play(bst.annotate(80, text="Maximum", direction=manim.RIGHT, box=True))
            self.wait(0.1)

    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        scene = AnnotationDemoScene()
        scene.render()
        assert len(scene.mobjects) >= 2
