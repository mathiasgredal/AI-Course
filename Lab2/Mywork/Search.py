from __future__ import annotations


class Node:
    def __init__(self, state: str, parent: Node = None, depth: int = 0):
        self.state = state
        self.parent_node = parent
        self.depth = depth

    def path(self) -> list[Node]:
        current_node = self
        path = [self]
        while current_node.parent_node:
            current_node = current_node.parent_node
            path.append(current_node)

        return path

    def expand(self, state_space: StateSpace):
        successors = []
        children = state_space.successor(self.state)
        for child in children:
            s = Node(child, self, self.depth + 1)
            successors = insert(s, successors)

        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Depth: {self.depth}"


def insert(node: Node, queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """Returns a copy of the queue with the node inserted (the fringe)"""
    out = queue.copy()
    if insert_as_first:
        out.insert(0, node)  # inserts in the beginning (Depth-first search)
    else:
        out.append(node)  # inserts at the end (Breadth first search)
    return out


def insert_all(in_list: list[Node], queue: list, insert_as_first: bool = True) -> list[Node]:
    """Inserts all nodes from the input list, into the queue using the insert function defined in this script"""
    for node in in_list:
        queue = insert(node, queue, insert_as_first)

    return queue


def remove_first(queue: list[Node]) -> Node:
    """Removes and returns the first element from the input list"""
    return queue.pop(0)


class StateSpace:
    def __init__(self, state_space: dict = None):
        self.state_space = state_space

    def successor(self, state: str):
        if self.state_space is None:
            print("No state space set")

        return self.state_space[state]


class Searcher:
    def __init__(self, initial_state='A', goal_state='J', state_space: StateSpace = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space

    def tree_search(self, depth_first: bool = True) -> list[Node]:
        """Search the tree for the goal state
        and return the path from the initial state to the goal state.

        If depth_first is False, then the tree_search will use breadth-first instead"""
        fringe = []
        initial_node = Node(self.initial_state)
        fringe = insert(initial_node, fringe)
        while fringe is not None:
            node = remove_first(fringe)
            if node.state == self.goal_state:
                return node.path()
            children = node.expand(self.state_space)
            fringe = insert_all(children, fringe, depth_first)
            print(f"Fringe: {fringe}")

    def run(self, depth_first: bool = True):
        path = self.tree_search(depth_first)
        print("Solution path:")
        for node in path:
            node.display()


if __name__ == '__main__':
    input_state_space = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [],
        'E': [],
        'F': [],
        'G': ['H', 'I', 'J'],
        'H': [],
        'I': [],
        'J': [],
    }

    searcher = Searcher(state_space=StateSpace(input_state_space))
    searcher.run(depth_first=True)
    searcher.run(depth_first=False)
