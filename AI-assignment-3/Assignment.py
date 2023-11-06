# CSP Assignment
# Original code by Håkon Måløy
# Updated by Xavier Sánchez Díaz

import copy
from itertools import product as prod


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains is a dictionary of domains (lists)
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.backtrack_counter = 0
        self.failure_counter = 0

    def add_variable(self, name: str, domain: list):
        """Add a new variable to the CSP.

        Parameters
        ----------
        name : str
            The name of the variable to add
        domain : list
            A list of the legal values for the variable
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a: list, b: list) -> list[tuple]:
        """Get a list of all possible pairs (as tuples) of the values in
        lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.

        Parameters
        ----------
        a : list
            First list of values
        b : list
            Second list of values

        Returns
        -------
        list[tuple]
            List of tuples in the form (a, b)
        """
        return prod(a, b)

    def get_all_arcs(self) -> list[tuple]:
        """Get a list of all arcs/constraints that have been defined in
        the CSP.

        Returns
        -------
        list[tuple]
            A list of tuples in the form (i, j), which represent a
            constraint between variable `i` and `j`
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var: str) -> list[tuple]:
        """Get a list of all arcs/constraints going to/from variable 'var'.

        Parameters
        ----------
        var : str
            Name of the variable

        Returns
        -------
        list[tuple]
            A list of all arcs/constraints in which `var` is involved
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i: str, j: str,
                               filter_function: callable):
        """Add a new constraint between variables 'i' and 'j'. Legal
        values are specified by supplying a function 'filter_function',
        that should return True for legal value pairs, and False for
        illegal value pairs.

        NB! This method only adds the constraint one way, from i -> j.
        You must ensure to call the function the other way around, in
        order to add the constraint the from j -> i, as all constraints
        are supposed to be two-way connections!

        Parameters
        ----------
        i : str
            Name of the first variable
        j : str
            Name of the second variable
        filter_function : callable
            A callable (function name) that needs to return a boolean.
            This will filter value pairs which pass the condition and
            keep away those that don't pass your filter.
        """
        if j not in self.constraints[i]:
            # First, get a list of all possible pairs of values
            # between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(
                self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = list(filter(lambda
                                                 value_pair:
                                             filter_function(*value_pair),
                                             self.constraints[i][j]))

    def add_all_different_constraint(self, var_list: list):
        """Add an Alldiff constraint between all the variables in the list provided.

        Parameters
        ----------
        var_list : list
            A list of variable names
        """
        for (i, j) in self.get_all_possible_pairs(var_list, var_list):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self) -> dict[str, list] | bool:
        """This functions starts the CSP solver and returns the found solution."""

        # Initialize counters
        self.backtrack_counter = 0
        self.failure_counter = 0

        # Copy domains of CSP variables
        assignment = copy.deepcopy(self.domains)

        # Reduce domain by inference
        self.inference(assignment, self.get_all_arcs())

        # Recursive backtrack search
        return self.backtrack(assignment)

    def backtrack(self, assignment: dict[str, list]) -> dict[str, list] | bool:
        """Recursive backtracking

        Parameters
        ----------
        assignment : dict[str, list]
            A set of variable-domain key-value pairs for the assignment to complete
        """
        if all([len(x) == 1 for x in assignment.values()]):  # if assignment is complete (all domains have size=1)
            return assignment

        self.backtrack_counter += 1  # increment counter

        var = self.select_unassigned_variable(assignment)  # select variable
        for val in self.order_variable_domain(assignment, var):  # Try every possible value of domain
            new_assignment = copy.deepcopy(assignment)  # copy the assignment, so we don't ruin it for when we backtrack

            if self.__is_consistent(var, val):  # If val is legal
                # If value is legal, assign value to variable {var = val}
                new_assignment[var] = [val]

                # Reduce domain of other variables (if possible)
                if self.inference(new_assignment, self.get_all_arcs()):

                    # If reduction is possible, assign next variable
                    result = self.backtrack(new_assignment)

                    # If assignment is complete
                    if result:
                        return result

                # If we get an empty domain, the value does not give a solution (in this branch)
                assignment[var] = self.domains[var]  # reset the variable (remove {var = val})

        # No valid value for the variable was found, so we go back
        self.failure_counter += 1
        return False

    def __is_consistent(self, var: str, val: str) -> bool:
        """
        Checks if a value in variable is consistent
        :param var: the variable
        :param val: the value
        :return: True if value is consistent, False if not
        """
        # Check all arcs
        for arcs in list(self.constraints[var].values()):
            # Check if any valid value exists in the arc, if not, value is not consistent
            if not any([val == arc[0] for arc in arcs]):
                return False
        return True

    def select_unassigned_variable(self, assignment: dict[str, list]) -> str:
        """
        Implementation of Minimum-remaining-values. Selects the variable with the minimal remaining number of values
        that is also not assigned (number of values of 1)
        :param assignment: the assignment to choose the variable from
        :return: The selected variable
        """
        # Filter all assigned values
        unassigned_variables = filter(lambda var: len(assignment[var]) > 1, assignment.keys())

        # Return the unassigned value with the smallest domain
        return min(unassigned_variables, key=lambda var: len(assignment[var]))

    def order_variable_domain(self, assignment: dict[str, list], var: str) -> list[str]:
        """Implementation of least-constraining-value. Sorts values after minimum number of collisions it has with
        neighbor variables, meaning how much a domain would be reduces if the variable was assigned.
        :return: LCV-sorted list of values
        """
        values = assignment[var]

        # Sort by minimal conflicts with neighbor variables
        return sorted(values, key=lambda val: self.get_num_conflicting_constraints(var, val))[::-1]

    def get_num_conflicting_constraints(self, var: str, val: str):
        """Calculates number of a collisions of a variable and its neighbors, given a value."""
        conflicts = 0
        for nb in self.get_all_neighboring_arcs(var):
            for arc in self.constraints[var][nb[0]]:
                if arc[0] == val:  # if value has a legal value pair
                    conflicts += 1  # we get a conflict (it is a lost value for the neighbor)
        return conflicts

    def inference(self, assignment, queue: list[tuple[str, str]]) -> bool:
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while len(queue) > 0:
            i, j = queue.pop()
            if self.revise(assignment, i, j):
                var = assignment[i]
                # if we get an empty domain
                if len(var) == 0:
                    return False
                # else, add all neighbors of i (must be checked also=
                for nb in self.get_all_neighboring_arcs(i):
                    if nb[0] != j:  # except from j
                        queue.append(nb)
        return True

    def revise(self, assignment: dict[str, list], i: str, j: str) -> bool:
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        revised = False

        # For values in x
        for x in assignment[i]:
            consistent = False
            # Try every value in y, to find a legal value pair
            for y in assignment[j]:
                # Check if x and y have legal values together
                if any([(x, y) == tuple(arc) for arc in self.constraints[i][j]]):
                    consistent = True  # if so, x is consistent
                    break
            # if no legal value for x and y was found
            if not consistent:
                # Remove x from assignment (counts as revision)
                assignment[i].remove(x)
                revised = True
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
             'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp


def create_sudoku_csp(filename: str) -> CSP:
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.

    Parameters
    ----------
    filename : str
        Filename of the Sudoku board to solve

    Returns
    -------
    CSP
        A CSP instance
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str,
                                                                range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col)
                                          for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col)
                                          for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" "),
            if col == 2 or col == 5:
                print('|', end=" "),
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


if __name__ == "__main__":
    import time


    def solve(name):
        print("=" * 25)
        print(name)

        if name == "map":
            csp = create_map_coloring_csp()
        else:
            csp = create_sudoku_csp(f"{name}.txt")
        t0 = time.time()
        solution = csp.backtracking_search()
        t1 = time.time()

        if solution:
            if name == "map":
                print(solution)
            else:
                print_sudoku_solution(solution)
        else:
            print("No solution")
        print(f"Num backtracks: {csp.backtrack_counter}")
        print(f"Num failures: {csp.failure_counter}")
        print(f"Calculation took {t1 - t0:.2f} seconds")
        print()


    solve("easy")
    solve("medium")
    solve("hard")
    solve("veryhard")
    solve("map")
