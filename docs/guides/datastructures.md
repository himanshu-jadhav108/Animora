# Computer Science Data Structures

Animora includes nine stateful data structures (`animora.datastructures`) designed for computer science education. Each structure pairs a pure Python data model (`XModel`) with an animation generation layer (`X`).

---

## 1. Supported Structures

1. **`Array`** (`ArrayListModel`): Linear indexed sequence with `animate_swap()`, `animate_highlight()`, `animate_set()`.
2. **`Stack`** (`StackModel`): LIFO stack with `animate_push()`, `animate_pop()`, `animate_peek()`.
3. **`Queue`** (`QueueModel`): FIFO queue with `animate_enqueue()`, `animate_dequeue()`, `animate_peek()`.
4. **`LinkedList`** (`LinkedListModel`): Singly-linked list with pointer transitions (`animate_insert_tail()`).
5. **`Heap`** (`HeapModel`): Binary min-heap with sift-up/sift-down animations.
6. **`Tree`** (`GenericTreeModel`): N-ary tree positioned via Phase 4 `TreeLayout`.
7. **`BST`** (`BSTModel`): Binary search tree with path-traced insertions and full 3-case deletion (leaf, 1-child, 2-children).
8. **`Graph`** (`GraphModel`): Network positioned via `GraphLayout` with state primitives (`animate_highlight_node()`, `animate_mark_visited()`, `animate_highlight_edge()`).
9. **`HashTable`** (`HashTableChainingModel`): Hash table using Separate Chaining collision handling.

---

## 2. Usage Example: Binary Search Tree

```python
from animora.core import Scene
from animora.datastructures import BST

class BSTDemo(Scene):
    def construct(self) -> None:
        bst = BST([50, 30, 70, 20, 40])
        self.play(bst.animate_create())
        # Traverses [50, 30, 40] before placing 35:
        self.play(bst.animate_insert(35))
        # Search highlight:
        self.play(bst.animate_search(35))
        # Complete 2-children deletion with in-order successor:
        self.play(bst.animate_delete(30))
```
