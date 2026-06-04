"""Unit tests verifying HashTable separate chaining collision handling."""

from __future__ import annotations

from animora.datastructures.hash_table import HashTableChainingModel


def test_hash_table_chaining_and_collisions() -> None:
    """Verify insert, search, and delete with deliberate hash collisions."""
    ht = HashTableChainingModel(num_buckets=3)

    # Insert keys that collide mod 3 (0, 3, 6)
    ht.insert(0, "zero")
    ht.insert(3, "three")
    ht.insert(6, "six")

    # All three should be in bucket 0 chain
    assert len(ht.buckets[0]) == 3
    assert ht.to_dict() == {0: "zero", 3: "three", 6: "six"}

    # Search
    found, b_idx, pos, val = ht.search(3)
    assert found is True
    assert b_idx == 0
    assert pos == 1
    assert val == "three"

    # Search non-existing
    found, _, _, _ = ht.search(99)
    assert found is False

    # Delete
    deleted, b_idx, pos = ht.delete(3)
    assert deleted is True
    assert len(ht.buckets[0]) == 2
    assert ht.to_dict() == {0: "zero", 6: "six"}
