from Enums import States, Location, Action

# Ex. rule (if location == A && Dirty then rule 1)

test_environment = {
    Location.A: States.DIRTY,
    Location.B: States.DIRTY,
    Location.C: States.DIRTY,
    Location.D: States.DIRTY,
    Location.CURRENT: Location.A
}


class StatefulReflexAgent:
    def __init__(self):
        self.rules = {
            (Location.A, States.DIRTY): Action.SUCK,
            (Location.B, States.DIRTY): Action.SUCK,
            (Location.C, States.DIRTY): Action.SUCK,
            (Location.D, States.DIRTY): Action.SUCK,
            (Location.A, States.CLEAN): Action.RIGHT,
            (Location.B, States.CLEAN): Action.DOWN,
            (Location.D, States.CLEAN): Action.LEFT,
            (Location.C, States.CLEAN): Action.UP,
            (Location.A, Location.B, Location.C, Location.D, States.CLEAN): Action.NO_OP
        }

        self.model = {
            Location.A: States.UNKNOWN,
            Location.B: States.UNKNOWN,
            Location.C: States.UNKNOWN,
            Location.D: States.UNKNOWN,
        }  # Initially ignorant

        self.state = {}
        self.last_action = Action.NO_OP

    def match_rule(self, percept: tuple[Location, States]) -> Action:  # Match rule for a given state
        return self.rules[percept]

    def update_state(self, percept: tuple[Location, States]) -> tuple[Location, States]:
        (location, status) = percept
        output_state = percept
        if self.model[Location.A] == self.model[Location.B] == self.model[Location.C] \
                == self.model[Location.D] == States.CLEAN:
            output_state = (Location.A, Location.B, Location.C, Location.D, States.CLEAN)
            # Output modified only for all elements clean
            # The model is used for checking if this is the case
        self.model[location] = status  # Update the model state
        return output_state

    def sensors(self, environment: dict[Location]) -> tuple[Location, States]:  # Sense Environment
        location = environment[Location.CURRENT]
        return location, environment[location]

    def actuators(self, requested_action: Action, environment: dict[Location]) -> None:  # Modify Environment
        location = environment[Location.CURRENT]

        # Improved strat:
        if requested_action not in location.allowed_moves():
            return

        if requested_action == Action.SUCK:
            environment[location] = States.CLEAN
        elif requested_action == Action.RIGHT:
            environment[Location.CURRENT] = Location.B if location == Location.A else Location.D
        elif requested_action == Action.LEFT:
            environment[Location.CURRENT] = Location.A if location == Location.B else Location.C
        elif requested_action == Action.UP:
            environment[Location.CURRENT] = Location.B if location == Location.D else Location.A
        elif requested_action == Action.DOWN:
            environment[Location.CURRENT] = Location.C if location == Location.A else Location.D

    def act(self, environment: dict[Location]) -> Action:
        percept = self.sensors(environment)
        self.state = self.update_state(percept)
        action = self.match_rule(self.state)
        self.actuators(action, environment)
        return action


def run(n):  # run the agent through n steps
    print('    Current                        New')
    print('location    status  action  location    status')
    environment = test_environment.copy()
    agent = StatefulReflexAgent()
    for i in range(1, n):
        (location, status) = agent.sensors(environment)  # Sense Environment before action
        print("{:12s}{:8s}".format(location.name, status.name), end='')
        action = agent.act(environment)
        (location, status) = agent.sensors(environment)  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action.name, location.name, status.name))


if __name__ == '__main__':
    run(20)
