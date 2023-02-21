A = 'A'
B = 'B'
C = 'C'
D = 'D'

# I believe that the world is laid out like:
# --
# A B
# C D
# --
# Which makes a clockwise pattern of A B D C (A)

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def run_reflex_vacuum_agent(percept: tuple):  # Determine action
    if percept[1] == 'Dirty':
        return 'Suck'
    # The square is clean, so we begin on a clockwise cleaning pattern
    if percept[0] == A:
        return 'Right'
    if percept[0] == B:
        return 'Down'
    if percept[0] == C:
        return 'Up'
    if percept[0] == D:
        return 'Left'


def sensors() -> tuple:  # Sense Environment
    location = Environment['Current']
    return location, Environment[location]


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
        action = run_reflex_vacuum_agent(sensors())
        actuators(action)
        (location, status) = sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20)
