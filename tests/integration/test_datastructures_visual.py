"""Integration tests verifying visual rendering and operation traces of all 9 data structures."""

from __future__ import annotations

import manim

from animora.core.scene import Scene
from animora.datastructures.array import Array
from animora.datastructures.bst import BST
from animora.datastructures.graph import Graph
from animora.datastructures.hash_table import HashTable
from animora.datastructures.heap import Heap
from animora.datastructures.linked_list import LinkedList
from animora.datastructures.queue import Queue
from animora.datastructures.stack import Stack
from animora.datastructures.tree import Tree


class DataStructuresIntegrationScene(Scene):
    """Scene exercising visual operations across data structures."""

    def construct(self) -> None:
        # 1. Array
        arr = Array([10, 20, 30, 40])
        self.play(arr.animate_swap(0, 3, run_time=0.1))
        self.play(arr.animate_highlight(2, run_time=0.1))

        # 2. Stack
        stack = Stack([1, 2])
        self.play(stack.animate_push(3, run_time=0.1))
        self.play(stack.animate_pop(run_time=0.1))

        # 3. Queue
        queue = Queue([1, 2])
        self.play(queue.animate_enqueue(3, run_time=0.1))
        self.play(queue.animate_dequeue(run_time=0.1))

        # 4. LinkedList
        ll = LinkedList([10, 20])
        self.play(ll.animate_insert_tail(30, run_time=0.1))

        # 5. Heap
        heap = Heap([10, 20, 30])
        self.play(heap.animate_insert(5, run_time=0.1))

        # 6. Tree
        tree = Tree("root")
        tree.model.insert_child("root", "child")
        self.play(tree.animate_highlight_node("root", run_time=0.1))

        # 7. BST (insert, search, delete)
        bst = BST([50, 30, 70])
        self.play(bst.animate_insert(40, run_time=0.1))
        self.play(bst.animate_search(70, run_time=0.1))
        self.play(bst.animate_delete(30, run_time=0.1))

        # 8. Graph (highlight node, mark visited, highlight edge)
        g = Graph(nodes=["A", "B"], edges=[("A", "B")])
        self.play(g.animate_highlight_node("A", run_time=0.1))
        self.play(g.animate_mark_visited("B", run_time=0.1))
        self.play(g.animate_highlight_edge("A", "B", run_time=0.1))

        # 9. HashTable
        ht = HashTable(num_buckets=3)
        self.play(ht.animate_insert("key1", 100, run_time=0.1))
        self.play(ht.animate_search("key1", run_time=0.1))


def test_datastructures_visual_rendering_end_to_end() -> None:
    """Verify all 9 data structure components render cleanly in Manim dry-run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = DataStructuresIntegrationScene()
        scene.render()
        assert len(scene.mobjects) >= 1
