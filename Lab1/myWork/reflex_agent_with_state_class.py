from Enums import States, Location, Action

state = {}
last_action = Action.NO_OP
model = {
    Location.A: States.UNKNOWN,
    Location.B: States.UNKNOWN,
    Location.C: States.UNKNOWN,
    Location.D: States.UNKNOWN,
}  # Initially ignorant



# The agent will clean in a clockwise pattern following:
# --
# A B
# C D
# --
# Which makes a clockwise pattern of A B D C (A...)
rules = {
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
# Ex. rule (if location == A && Dirty then rule 1)

Environment = {
    Location.A: States.DIRTY,
    Location.B: States.DIRTY,
    Location.C: States.DIRTY,
    Location.D: States.DIRTY,
    Location.CURRENT: Location.A
}


def match_rule(state: tuple, rules: dict) -> Action:  # Match rule for a given state
    return rules.get(tuple(state))


def update_state(state, action, percept):
    (location, status) = percept
    state = percept
    if model[Location.A] == model[Location.B] == model[Location.C] == model[Location.D] == States.CLEAN:
        state = (Location.A, Location.B, Location.C, Location.D, States.CLEAN)
        # Model consulted only for A and B Clean
    model[location] = status  # Update the model state
    return state


def run_reflex_agent_with_state(percept):
    global state, last_action
    state = update_state(state, last_action, percept)
    return match_rule(state, rules)


def sensors() -> tuple[Location, States]:  # Sense Environment
    location = Environment[Location.CURRENT]
    return location, Environment[location]


def actuators(requested_action: Action) -> None:  # Modify Environment
    location = Environment[Location.CURRENT]

    # Improved strat:
    if requested_action not in location.allowed_moves():
        return

    if requested_action == Action.SUCK:
        Environment[location] = States.CLEAN
    elif requested_action == Action.RIGHT:
        Environment[Location.CURRENT] = Location.B if location == Location.A else Location.D
    elif requested_action == Action.LEFT:
        Environment[Location.CURRENT] = Location.A if location == Location.B else Location.C
    elif requested_action == Action.UP:
        Environment[Location.CURRENT] = Location.B if location == Location.D else Location.A
    elif requested_action == Action.DOWN:
        Environment[Location.CURRENT] = Location.C if location == Location.A else Location.D

def run(n):  # run the agent through n steps
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = sensors()  # Sense Environment before action
        print("{:12s}{:8s}".format(location.name, status.name), end='')
        action = run_reflex_agent_with_state(sensors())
        actuators(action)
        (location, status) = sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action.name, location.name, status.name))



if __name__ == '__main__':
    run(20)
