from __future__ import annotations

from copy import deepcopy

from Enums import StateTypes, Location, Action


class EnvironmentState:
    def __init__(self, environment: dict[Location: StateTypes]):
        self.environment = environment

    def count_dirty_states(self) -> int:
        out = 0
        for k, v in self.environment.items():
            if v == StateTypes.DIRTY:
                out += 1
        return out

    def __eq__(self, other):
        if type(other) != EnvironmentState or len(other.environment) != len(self.environment):
            return False

        for k, v in self.environment.items():
            if other.environment[k] != v:
                return False

        return True  # The other thing is an EnvironmentState,
        # it has the same number of elements as this, and all values match, They must be equal

    def copy(self) -> EnvironmentState:
        """Returns a deepcopy of this state, that can then be modified at will"""
        out_state = deepcopy(self.environment)
        return EnvironmentState(out_state)

    def clean(self, location: Location) -> None:
        self.environment[location] = StateTypes.CLEAN

    def __repr__(self):
        return str(self.environment)


class SearchState:
    def __init__(self, environment: EnvironmentState, position: Location, path: list[Action] = None, cost: int = 0):
        """
        The environment should contain the state of the environment after the last action in the path have been performed.
        Position should contain the position of the vacuum robot.
        cost is a running (true) cost of all actions taken on the path.
        """
        self.environment = environment
        self.position = position
        self.path = path if path is not None else []
        self.cost = cost

    def get_heuristic_a(self):
        return self.environment.count_dirty_states()

    def get_heuristic(self):
        extra = 1 if self.environment.environment[self.position] == StateTypes.DIRTY else 0
        return self.environment.count_dirty_states() + extra

    def insert(self, queue: list[SearchState], alpha: float = 1) -> list[SearchState]:
        """Returns a copy of the queue with the node inserted (the fringe).

        The queue must be ordered already (essentially means built by this function)"""
        out = queue.copy()
        for i in range(0, len(queue)):
            if self.compare(out[i], alpha) < 0:
                out.insert(i, self)
                return out
        out.insert(len(queue), self)
        return out

    def compare(self, other: SearchState, alpha: float) -> float:
        """Returns r < 0  if other is larger, 0 if equal and r > 0 if self is larger.

        Alpha is a weight that is applied to the heuristic. It can be used to change the behaviour of A-star (if infinite A-star effectively becomes greedy best first)"""

        return self.weighted_sum(alpha) - other.weighted_sum(alpha)

    def weighted_sum(self, alpha: float) -> float:
        return self.cost + self.get_heuristic() * alpha

    def get_environment_state(self):
        return self.environment

    def __repr__(self):
        return f"SearchState ( env: {self.environment} - pos{self.position} - path:{self.path} - cost: {self.cost})"