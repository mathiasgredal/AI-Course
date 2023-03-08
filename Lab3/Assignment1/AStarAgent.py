from Enums import StateTypes, Location, Action
from Lab3.Assignment1.SearchState import EnvironmentState, SearchState

test_environment = {
    Location.A: StateTypes.DIRTY,
    Location.B: StateTypes.DIRTY,
    Location.C: StateTypes.DIRTY,
    Location.D: StateTypes.DIRTY,
}


def insert_all(in_list: list[SearchState], queue: list, alpha: float = 1) -> list[SearchState]:
    """Inserts all nodes from the input list, into the queue using the insert function defined in this script"""
    for state in in_list:
        queue = state.insert(queue, alpha)

    return queue


def remove_first(queue: list[SearchState]) -> SearchState:
    """Removes and returns the first element from the input list"""
    return queue.pop(0)


class AStarAgent:
    def __init__(self, start_position: Location, start_state_space: dict[Location: StateTypes]):
        self.current_position = start_position

        self.last_action = Action.NO_OP

        self.goal_state = EnvironmentState({
            Location.A: StateTypes.CLEAN,
            Location.B: StateTypes.CLEAN,
            Location.C: StateTypes.CLEAN,
            Location.D: StateTypes.CLEAN,
        })

        self.state = EnvironmentState(start_state_space)

    def weighted_A_star(self, weight_alpha: float = 1) -> list[Action]:
        fringe = []

        initial_state = SearchState(self.state, self.current_position)
        fringe = initial_state.insert(fringe, weight_alpha)

        fringe_count = 0

        while fringe is not None:
            node = remove_first(fringe)
            if node.get_environment_state() == self.goal_state:
                return node.path
            children = self.expand_node(node, weight_alpha)
            fringe = insert_all(children, fringe, weight_alpha)
            fringe_count += 1
            print(f"Fringe {fringe_count}: {fringe}")

        return []

    def expand_node(self, node: SearchState, alpha: float) -> list[SearchState]:
        # Check the legal moves on the current position of the agent
        allowed_moves = list(node.position.allowed_moves())
        # Perform an additional check to see if we are allowed to suck
        if node.get_environment_state().environment[node.position] == StateTypes.DIRTY:
            allowed_moves.append(Action.SUCK)

        # For the list of legal moves, perform them and put the resulting search state into the output array
        out = []
        for action in allowed_moves:
            if action == Action.NO_OP:
                continue
            new_location = node.position.perform_move(action)
            if new_location == Location.UNKNOWN:
                raise Exception("Tried to explore an illegal move")
                continue
            environment = node.environment.copy()
            if action == Action.SUCK:
                environment.clean(node.position)
            path = node.path.copy()
            path.append(action)
            new_state = SearchState(environment=environment, position=new_location, path=path, cost=node.cost+1)
            out.append(new_state)

        return out


def run(n):  # run the agent through n steps
    print('    Current                        New')
    print('location    status  action  location    status')
    environment = test_environment.copy()
    agent = AStarAgent(Location.A, environment)
    solution = agent.weighted_A_star()
    print(solution)



if __name__ == '__main__':
    run(20)
