"""Unit tests for the public AlgorithmTrace / OperationTrace API."""

from __future__ import annotations

from animora.algorithms.trace import (
    AlgorithmTrace,
    OperationTrace,
    OperationType,
)


def test_operation_trace_creation_and_alias() -> None:
    """Verify OperationTrace instantiation and AlgorithmTrace alias equality."""
    trace = OperationTrace()
    assert isinstance(trace, AlgorithmTrace)
    assert len(trace) == 0

    trace.add_step(OperationType.COMPARE, "Compare 0 and 1", targets=[0, 1])
    trace.add_step("swap", "Swap 0 and 1", targets=[0, 1])

    assert len(trace) == 2
    assert trace[0].op_type == OperationType.COMPARE
    assert trace[1].op_type == OperationType.SWAP


def test_operation_trace_filter_and_count() -> None:
    """Verify filter and count methods by enum and string value."""
    trace = OperationTrace()
    trace.add_step(OperationType.COMPARE, "Comp 1", targets=[0, 1])
    trace.add_step(OperationType.COMPARE, "Comp 2", targets=[1, 2])
    trace.add_step(OperationType.SWAP, "Swap 1", targets=[1, 2])
    trace.add_step(OperationType.HIGHLIGHT, "Highlight", targets=[2])

    assert trace.count() == 4
    assert trace.count(OperationType.COMPARE) == 2
    assert trace.count("compare") == 2
    assert trace.count(OperationType.SWAP) == 1
    assert trace.count(OperationType.SET) == 0

    comparisons = trace.filter(OperationType.COMPARE)
    assert len(comparisons) == 2
    assert all(step.op_type == OperationType.COMPARE for step in comparisons)

    targets = trace.targets_for(OperationType.COMPARE)
    assert targets == [(0, 1), (1, 2)]


def test_operation_trace_summary_and_serialization() -> None:
    """Verify summary dictionary and to_dict serialization."""
    trace = OperationTrace()
    trace.add_step(OperationType.VISIT_NODE, "Visit A", targets=["A"], cost=0.0)
    trace.add_step(OperationType.RELAX_EDGE, "Relax A->B", targets=["A", "B"], weight=2.5)

    summary = trace.summary()
    assert summary == {"visit_node": 1, "relax_edge": 1}

    serialized = trace.to_dict()
    assert len(serialized) == 2
    assert serialized[0]["op_type"] == "visit_node"
    assert serialized[0]["targets"] == ["A"]
    assert serialized[0]["metadata"]["cost"] == 0.0
    assert serialized[1]["metadata"]["weight"] == 2.5
