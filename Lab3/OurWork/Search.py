from __future__ import annotations


class Node:
    def __init__(self, state, parent: Node = None, depth: int = 0, path_cost: int = 0, heuristic: int = 0,
                 alpha: float = 1):
        self.state = state
        self.parent_node = parent
        self.depth = depth
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.alpha = alpha

    def path(self) -> list[Node]:
        current_node = self
        path = [self]
        while current_node.parent_node:
            current_node = current_node.parent_node
            path.append(current_node)

        return path

    def wighted_sum(self, alpha: float) -> float:
        return self.path_cost + self.heuristic * alpha

    def compare(self, other: Node, alpha: float) -> float:
        """Returns r < 0  if other is larger, 0 if equal and r > 0 if self is larger.

        Alpha is a weight that is applied to the heuristic. It can be used to change the behaviour of A-star (if infinite A-star effectively becomes greedy best first)"""

        return self.wighted_sum(alpha) - other.wighted_sum(alpha)

    def display(self) -> None:
        print(self)

    def __repr__(self) -> str:
        return f"State: {self.state} - Depth: {self.depth} - Path cost: {self.path_cost} - Heuristic: {self.heuristic} - Weighted sum: {self.wighted_sum(self.alpha)}"


def insert(node: Node, queue: list[Node], alpha: float = 1) -> list[Node]:
    """Returns a copy of the queue with the node inserted (the fringe).

    The queue must be ordered already (essentially means built by this function)"""
    out = queue.copy()
    for i in range(0, len(queue)):
        if node.compare(out[i], alpha) < 0:
            out.insert(i, node)
            return out
    out.insert(len(queue), node)
    return out


def insert_all(in_list: list[Node], queue: list, alpha: float = 1) -> list[Node]:
    """Inserts all nodes from the input list, into the queue using the insert function defined in this script"""
    for node in in_list:
        queue = insert(node, queue, alpha)

    return queue


def remove_first(queue: list[Node]) -> Node:
    """Removes and returns the first element from the input list"""
    return queue.pop(0)


class StateSpace:
    def __init__(self, state_space: dict = None):
        self.state_space = state_space

    def successor(self, state: str):
        if self.state_space is None:
            raise Exception("No state space set")

        return self.state_space[state]


class Searcher:
    def __init__(self, initial_state, goal_state: tuple | str, state_space: StateSpace = None, heuristics: dict = None):
        self.initial_state = initial_state
        self.goal_state: tuple = goal_state if type(goal_state) == tuple else tuple(goal_state)
        self.state_space = state_space
        self.heuristics = heuristics

    def get_heuristic(self, state: str):
        if self.heuristics is None:
            raise Exception("No heuristics set")
        return self.heuristics[state]

    def expand_node(self, node: Node, alpha: float) -> list[Node]:
        successors = []
        children = self.state_space.successor(node.state)
        for child in children:
            child_state = child[0]
            cost_to_child = child[1]
            s = Node(child_state, node, node.depth + 1, node.path_cost + cost_to_child, self.get_heuristic(child_state),
                     alpha)
            successors = insert(s, successors)

        return successors

    def weighted_A_star(self, weight_alpha: float) -> list[Node]:
        fringe = []
        initial_node = Node(self.initial_state, path_cost=0, heuristic=self.get_heuristic(self.initial_state),
                            alpha=weight_alpha)
        fringe = insert(initial_node, fringe, weight_alpha)
        fringe_count = 0
        while fringe is not None:
            node = remove_first(fringe)
            if node.state in self.goal_state:
                return node.path()
            children = self.expand_node(node, weight_alpha)
            fringe = insert_all(children, fringe, weight_alpha)
            fringe_count += 1
            print(f"Fringe {fringe_count}: {fringe}")

    def A_star(self) -> list[Node]:
        """Search the tree for the goal state
                and return the path from the initial state to the goal state."""
        print("Searching using A-star:")
        return self.weighted_A_star(1)

    def greedy_BFS(self) -> list[Node]:
        print("Searching using Greedy BFS:")
        return self.weighted_A_star(1000)

    def show_path(self, path: list[Node]):
        print("\nSolution path:")
        path.reverse()
        for node in path:
            node.display()
        print("-" * 100 + "\n")


if __name__ == '__main__':
    # Tuple format = ('Node_name', cost to this node)
    input_state_space = {
        'A': [('B', 1), ('C', 2), ('D', 4)],
        'B': [('F', 5), ('E', 4)],
        'C': [('E', 1)],
        'D': [('H', 1), ('I', 4), ('J', 2)],
        'E': [('G', 2), ('H', 3)],
        'F': [('G', 1)],
        'G': [('K', 6)],
        'H': [('K', 6), ('L', 5)],
        'I': [('L', 3)],
        'J': [],
        'K': [],
        'L': [],
    }

    input_heuristics = {
        'A': 6,
        'B': 5,
        'C': 5,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 4,
        'H': 1,
        'I': 2,
        'J': 1,
        'K': 0,
        'L': 0,
    }

    searcher = Searcher('A', ('K', 'L'), state_space=StateSpace(input_state_space), heuristics=input_heuristics)
    searcher.show_path(searcher.A_star())
    searcher.show_path(searcher.greedy_BFS())
    print("Weighted A-star 1.2")
    searcher.show_path(searcher.weighted_A_star(1.2))

    print("Weighted A-star 1.5")
    searcher.show_path(searcher.weighted_A_star(1.5))
    print("Weighted A-star 2.5")
    searcher.show_path(searcher.weighted_A_star(2.5))

    searcher = Searcher('A', ('K'), state_space=StateSpace(input_state_space), heuristics=input_heuristics)
    searcher.show_path(searcher.A_star())
    searcher.show_path(searcher.greedy_BFS())
    print("Weighted A-star 1.2")
    searcher.show_path(searcher.weighted_A_star(1.2))

    print("Weighted A-star 1.5")
    searcher.show_path(searcher.weighted_A_star(1.5))
    print("Weighted A-star 2.5")
    searcher.show_path(searcher.weighted_A_star(2.5))

    # vacuum_space = {
    #     ('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
    #     ('B', 'Dirty', 'Dirty'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
    #     ('B', 'Dirty', 'Clean'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Clean')],
    #     ('A', 'Dirty', 'Clean'): [('B', 'Dirty', 'Clean'), ('A', 'Clean', 'Clean'), ('A', 'Dirty', 'Clean')],
    #     ('A', 'Clean', 'Dirty'): [('B', 'Clean', 'Dirty'), ('A', 'Clean', 'Dirty')],
    #     ('B', 'Clean', 'Dirty'): [('B', 'Clean', 'Dirty'), ('A', 'Clean', 'Dirty'), ('A', 'Clean', 'Clean')],
    #     ('B', 'Clean', 'Clean'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Clean')],
    #     ('A', 'Clean', 'Clean'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Clean')],
    # }
    #
    # print("Vacuum world")
    # searcher = Searcher(initial_state=('A', 'Dirty', 'Dirty'), goal_state=('B', 'Clean', 'Clean'),
    #                     state_space=StateSpace(vacuum_space))
    #
    # print("Breadth-first")
    # searcher.run()
