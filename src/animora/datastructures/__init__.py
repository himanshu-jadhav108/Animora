"""Stateful, algorithm-aware data structure components for Animora.

Includes Array, Stack, Queue, LinkedList, Heap, Tree, BST, Graph, and HashTable,
with separated pure Python data models and synchronized animation generation layers.
"""

from __future__ import annotations

from animora.datastructures.array import Array, ArrayListModel
from animora.datastructures.bst import BST, BSTModel, BSTNode
from animora.datastructures.graph import Graph, GraphModel
from animora.datastructures.hash_table import HashEntry, HashTable, HashTableChainingModel
from animora.datastructures.heap import Heap, HeapModel
from animora.datastructures.linked_list import LinkedList, LinkedListModel, ListNode
from animora.datastructures.queue import Queue, QueueModel
from animora.datastructures.stack import Stack, StackModel
from animora.datastructures.tree import GenericTreeModel, Tree, TreeNode

__all__: list[str] = [
    "Array",
    "ArrayListModel",
    "BST",
    "BSTModel",
    "BSTNode",
    "GenericTreeModel",
    "Graph",
    "GraphModel",
    "HashEntry",
    "HashTable",
    "HashTableChainingModel",
    "Heap",
    "HeapModel",
    "LinkedList",
    "LinkedListModel",
    "ListNode",
    "Queue",
    "QueueModel",
    "Stack",
    "StackModel",
    "Tree",
    "TreeNode",
]
