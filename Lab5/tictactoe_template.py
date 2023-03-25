X = "X"
O = "O"


def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        # print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    action, state = max(successors_of(state), key=lambda a: min_value(a[1]))
    return action


def is_terminal(state) -> bool:
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    unmarked = 0
    for v in state:
        if v != X and v != O:
            unmarked += 1
            break

    if unmarked == 0:
        return True

    # Check diagonals
    if state[0] == state[4] and state[4] == state[8]:
        return True
    if state[2] == state[4] and state[4] == state[6]:
        return True

    # Check vertical
    for j in range(0, 3):  # up to and including 2
        if state[j] == state[j + 3] and state[j + 3] == state[j + 6]:
            return True

    # Check horizontal
    for j in range(0, 7, 3):  # up to and including 6
        if state[j] == state[j + 1] and state[j + 1] == state[j + 2]:
            return True

    return False


def utility_of(state: list[int | str]) -> int:
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    utility = 0

    # Check diagonal
    utility += check_line(state, (0, 4, 8))
    utility += check_line(state, (2, 4, 6))

    # Check vertical
    for j in range(0, 3):  # up to and including 2
        utility += check_line(state, (j, j + 3, j + 6))

    # Check horizontal
    for j in range(0, 7, 3):  # up to and including 6
        utility += check_line(state, (j, j + 1, j + 2))

    # if utility > 0:
    #     return 1
    #
    # if utility < 0:
    #     return -1

    return utility


def check_line(state: list[str | int], numbers: tuple) -> int:
    symbol_count = 0
    x_count = 0
    # o_count = symbol_count - x_count
    symbols = (X, O)
    for i in numbers:
        if state[i] in symbols:
            symbol_count += 1
            x_count += 1 if state[i] == X else 0

    if symbol_count == x_count:
        return 1

    if symbol_count == 0 or x_count > 0:
        return 0

    # We have some O, and x_count is 0, therefore O must have an open line here
    return -1


def successors_of(state) -> list[tuple[int, list]]:
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    out = list()
    x_count = 0
    o_count = 0
    symbols = (X, O)

    for i in state:
        if i in symbols:
            if i == X:
                x_count += 1
            else:
                o_count += 1

    symbol_to_place = X if x_count == o_count else O

    for k, i in enumerate(state):
        if i != X and i != O:
            state_copy = list(state)
            state_copy[k] = symbol_to_place
            out.append((k, state_copy))

    return out


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = X
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = O
    display(board)


if __name__ == '__main__':
    main()
