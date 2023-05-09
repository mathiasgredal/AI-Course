A = 'A'
B = 'B'
C = 'C'
D = 'D'
state = {}
last_action = None
model = {A: None, B: None, C: None, D: None}  # Initially ignorant

RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'Up',
    5: 'Down',
    10: 'NoOp'
}

# The agent will clean in a clockwise pattern following:
# --
# A B
# C D
# --
# Which makes a clockwise pattern of A B D C (A...)
rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 5,
    (D, 'Clean'): 3,
    (C, 'Clean'): 4,
    (A, B, C, D, 'Clean'): 10
}
# Ex. rule (if location == A && Dirty then rule 1)

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def match_rule(state, rules):  # Match rule for a given state
    rule = rules.get(tuple(state))
    return rule


def update_state(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == 'Clean':
        state = (A, B, C, D, 'Clean')
        # Model consulted only for A and B Clean
    model[location] = status  # Update the model state
    return state


def run_reflex_agent_with_state(percept):
    global state, last_action
    state = update_state(state, action, percept)
    rule = match_rule(state, rules)
    action = RULE_ACTION[rule]
    return action


def sensors():  # Sense Environment
    location = Environment['Current']
    return (location, Environment[location])


def actuators(action: str) -> None:  # Modify Environment
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Down' and location == A:
        Environment['Current'] = D
    elif action == 'Left' and location == B:
        Environment['Current'] = A
    elif action == 'Down' and location == B:
        Environment['Current'] = D
    elif action == 'Right' and location == C:
        Environment['Current'] = D
    elif action == 'Up' and location == C:
        Environment['Current'] = A
    elif action == 'Left' and location == D:
        Environment['Current'] = C
    elif action == 'Up' and location == D:
        Environment['Current'] = B


def run(n):  # run the agent through n steps
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = sensors()  # Sense Environment before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = run_reflex_agent_with_state(sensors())
        actuators(action)
        (location, status) = sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20)
