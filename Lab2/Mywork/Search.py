from __future__ import annotations


class Node:
    def __init__(self, state, parent: Node = None, depth: int = 0):
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
    def __init__(self, initial_state, goal_state, state_space: StateSpace = None):
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

    searcher = Searcher('A', 'J', state_space=StateSpace(input_state_space))
    print("Depth-first")
    searcher.run(depth_first=True)
    print("Breadth-first")
    searcher.run(depth_first=False)

    vacuum_space = {
        ('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
        ('B', 'Dirty', 'Dirty'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
        ('B', 'Dirty', 'Clean'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Clean')],
        ('A', 'Dirty', 'Clean'): [('B', 'Dirty', 'Clean'), ('A', 'Clean', 'Clean'), ('A', 'Dirty', 'Clean')],
        ('A', 'Clean', 'Dirty'): [('B', 'Clean', 'Dirty'), ('A', 'Clean', 'Dirty')],
        ('B', 'Clean', 'Dirty'): [('B', 'Clean', 'Dirty'), ('A', 'Clean', 'Dirty'), ('A', 'Clean', 'Clean')],
        ('B', 'Clean', 'Clean'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Clean')],
        ('A', 'Clean', 'Clean'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Clean')],
    }

    print("Vacuum world")
    searcher = Searcher(initial_state=('A', 'Dirty', 'Dirty'), goal_state=('B', 'Clean', 'Clean'),
                        state_space=StateSpace(vacuum_space))
    print("Depth-first")
    # searcher.run(depth_first=True)
    print("Breadth-first")
    searcher.run(depth_first=False)

    # tuple_format = ("farmer", "wolf", "goat", "cabbage")  # W for west, E for East
    farmer_space = {
        ('W', 'W', 'W', 'W'): [('E', 'E', 'W', 'W'), ('E', 'W', 'E', 'W'), ('E', 'W', 'W', 'E')],
        # depth 1
        ('E', 'E', 'W', 'W'): [],  # done the goat ate the cabbage
        ('E', 'W', 'E', 'W'): [('W', 'W', 'W', 'W'), ('W', 'W', 'E', 'W')],
        ('E', 'W', 'W', 'E'): [],  # Done the wolf ate the goat
        # All results from depth 1 explored
        # Depth 2
        ('W', 'W', 'E', 'W'): [('E', 'W', 'E', 'W'), ('E', 'E', 'E', 'W'), ('E', 'W', 'E', 'E')],
        # Depth 3
        ('E', 'E', 'E', 'W'): [('W', 'E', 'W', 'W'), ('W', 'E', 'E', 'W'), ('W', 'W', 'E', 'W')],
        ('E', 'W', 'E', 'E'): [('W', 'W', 'E', 'E'), ('W', 'W', 'E', 'W'), ('W', 'W', 'W', 'E')],
        # Depth 4
        ('W', 'E', 'W', 'W'): [('E', 'E', 'W', 'W'), ('E', 'E', 'E', 'W'), ('E', 'E', 'W', 'E')],
        ('W', 'E', 'E', 'W'): [],  # Done the wolf ate the goat
        ('W', 'W', 'E', 'W'): [('E', 'W', 'E', 'W'), ('E', 'E', 'E', 'W'), ('E', 'W', 'E', 'E')],
        ('W', 'W', 'E', 'E'): [],  # Done the goat ate the cabbage
        ('W', 'W', 'W', 'E'): [('E', 'W', 'W', 'E'), ('E', 'E', 'W', 'E'), ('E', 'W', 'E', 'E')],
        # Depth 5
        ('E', 'E', 'W', 'E'): [('W', 'E', 'W', 'E'), ('W', 'W', 'W', 'E'), ('W', 'E', 'W', 'W')],
        # Depth 6
        ('W', 'E', 'W', 'E'): [('E', 'E', 'W', 'E'), ('E', 'E', 'E', 'E')],
    }

    print("Farmer world")
    searcher = Searcher(initial_state=('W', 'W', 'W', 'W'), goal_state=('E', 'E', 'E', 'E'),
                        state_space=StateSpace(farmer_space))
    print("Depth-first")
    # searcher.run(depth_first=True)
    print("Breadth-first")
    searcher.run(depth_first=False)
