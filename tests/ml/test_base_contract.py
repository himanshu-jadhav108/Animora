"""Unit tests for ML base classes, MLTrace, and one-call API contract primitives."""

from __future__ import annotations

from typing import Any

from animora.ml.base import MLComponent, MLTrace, MLTraceStep


def test_ml_trace_recording() -> None:
    trace = MLTrace()
    assert len(trace) == 0

    s1 = trace.record("init", "Starting optimization", epoch=0, lr=0.01)
    assert isinstance(s1, MLTraceStep)
    assert s1.step_index == 0
    assert s1.name == "init"
    assert s1.values["epoch"] == 0
    assert s1.values["lr"] == 0.01

    trace.record("step", "Gradient update", loss=0.45)
    assert len(trace) == 2
    assert trace[1].values["loss"] == 0.45

    step_list = list(trace)
    assert len(step_list) == 2
    assert step_list[0].name == "init"
    assert step_list[1].name == "step"


def test_ml_component_contract() -> None:
    class DummyMLComp(MLComponent):
        def _build_mobject(self) -> Any:
            import manim

            return manim.Circle()

    comp = DummyMLComp()
    anim_create = comp.animate_create(run_time=0.5)
    assert anim_create.name == "create_ml_component"
    assert anim_create.run_time == 0.5

    anim_fade = comp.animate_fade_in(run_time=0.2)
    assert anim_fade.name == "fade_in_ml_component"
    assert anim_fade.run_time == 0.2
