from Lab6.Assignment2_part2.Colors import Color
from Lab6.Assignment2_part2.SAStates import SAStates


class CSP:
    def __init__(self, variables: list[SAStates], domains: dict[SAStates, list[Color]],
                 neighbours: dict[SAStates, list[SAStates]], constraints: dict[SAStates, callable]):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self) -> dict[SAStates, Color] | None:
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment: dict[SAStates, Color]) -> dict[SAStates, Color] | None:
        if self.is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result_out = self.recursive_backtracking(assignment)
                if result_out is not None:
                    return result_out

                # Remove variable from assignment if it resulted in a failure down the line
                assignment.pop(variable)

        return None

    def select_unassigned_variable(self, assignment: dict[SAStates, Color]) -> SAStates:
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment) -> bool:
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable: SAStates, assignment: dict[SAStates, Color]) -> list[Color]:
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable: SAStates, value: Color, assignment: dict[SAStates, Color]) -> bool:
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


def create_south_america_csp() -> CSP:
    variables = [v for v in SAStates]

    # We write the colors individually, since it allows us greater control, to choose exactly the colors we want to use
    values = [Color.Red, Color.Blue, Color.Green, Color.Yellow]

    domains = {
    }
    # All variables have the same domain, when starting
    for variable in variables:
        domains[variable] = values[:]

    neighbours = {
        SAStates.CostaRica: [SAStates.Panama],
        SAStates.Panama: [SAStates.CostaRica, SAStates.Colombia],
        SAStates.Colombia: [SAStates.Panama, SAStates.Venezuela, SAStates.Ecuador, SAStates.Peru, SAStates.Brasil],
        SAStates.Venezuela: [SAStates.Colombia, SAStates.Brasil, SAStates.Guyana],
        SAStates.Guyana: [SAStates.Venezuela, SAStates.Brasil, SAStates.Suriname],
        SAStates.Suriname: [SAStates.Guyana, SAStates.Brasil, SAStates.GuyaneFR],
        SAStates.GuyaneFR: [SAStates.Suriname, SAStates.Brasil],
        SAStates.Ecuador: [SAStates.Colombia, SAStates.Peru],
        SAStates.Peru: [SAStates.Ecuador, SAStates.Colombia, SAStates.Brasil, SAStates.Bolivia, SAStates.Chile],
        SAStates.Brasil: [SAStates.Colombia, SAStates.Venezuela, SAStates.Guyana, SAStates.Suriname, SAStates.GuyaneFR,
                          SAStates.Uruguay, SAStates.Argentina, SAStates.Paraguay, SAStates.Bolivia, SAStates.Peru],
        SAStates.Bolivia: [SAStates.Peru, SAStates.Brasil, SAStates.Paraguay, SAStates.Argentina, SAStates.Chile],
        SAStates.Paraguay: [SAStates.Bolivia, SAStates.Brasil, SAStates.Argentina],
        SAStates.Chile: [SAStates.Peru, SAStates.Bolivia, SAStates.Argentina],
        SAStates.Argentina: [SAStates.Bolivia, SAStates.Paraguay, SAStates.Brasil, SAStates.Uruguay, SAStates.Chile],
        SAStates.Uruguay: [SAStates.Brasil, SAStates.Argentina],
    }

    def constraint_function(first_variable: SAStates, first_value: Color, second_variable: SAStates,
                            second_value: Color):
        return first_value != second_value or first_variable == second_variable

    constraints = {
    }
    # Fill the constraint into all variables
    for v in variables:
        constraints[v] = constraint_function

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_south_america_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))
        # The below line makes it easier to check if any neighbours have been put into the solution wrongly
        # And whether any color assignments violate constraints
        print(f"\tNeighbours: {[(n.name, result[n].name) for n in australia.neighbours[area]]}")

    # Check at https://mapchart.net/australia.html
