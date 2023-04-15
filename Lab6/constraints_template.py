from random import shuffle

from Lab6.MyWork.Colors import Color
from Lab6.MyWork.States import States


class CSP:
    def __init__(self, variables: list[States], domains: dict[States, list[Color]],
                 neighbours: dict[States, list[States]], constraints: dict[States, callable]):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        pass

    def select_unassigned_variable(self, assignment) -> States:
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment) -> bool:
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable: States, assignment) -> list[Color]:
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable: States, value: Color, assignment) -> bool:
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_australia_csp() -> CSP:
    variables = [States.WA, States.Q, States.T, States.V, States.SA, States.NT, States.NSW]
    values = [Color.Red, Color.Blue, Color.Green]
    domains = {
        States.WA: values[:],
        States.Q: values[:],
        States.T: values[:],
        States.V: values[:],
        States.SA: values[:],
        States.NT: values[:],
        States.NSW: values[:],
    }
    neighbours = {
        States.WA: [States.SA, States.NT],
        States.Q: [States.SA, States.NT, States.NSW],
        States.T: [],
        States.V: [States.SA, States.NSW],
        States.SA: [States.WA, States.NT, States.Q, States.NSW, States.V],
        States.NT: [States.SA, States.WA, States.Q],
        States.NSW: [States.SA, States.Q, States.V],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        States.WA: constraint_function,
        States.Q: constraint_function,
        States.T: constraint_function,
        States.V: constraint_function,
        States.SA: constraint_function,
        States.NT: constraint_function,
        States.NSW: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_australia_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
