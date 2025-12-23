# Skyler Lee
# Winston Shih (WXS190012)
import sys


class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.value = None


class Constraint:
    def __init__(self, var1, op, var2):
        self.var1 = var1
        self.op = op
        self.var2 = var2


def read_variables(var_file):
    variables = {}
    with open(var_file, 'r') as f:
        for line in f:
            name, values = line.strip().split(': ')
            domain = list(map(int, values.split()))
            variables[name] = Variable(name, domain)
    return variables


def read_constraints(con_file):
    constraints = []
    with open(con_file, 'r') as f:
        for line in f:
            var1, op, var2 = line.strip().split()
            constraints.append(Constraint(var1, op, var2))
    return constraints


def forward_check(variables, constraints, var_name, value):
    removed = {}
    for constraint in constraints:
        # Check constraints where var_name is involved
        if constraint.var1 == var_name:
            other_var = variables[constraint.var2]
            if other_var.value is None:
                to_remove = []
                for val in other_var.domain:
                    if not check_constraint(value, constraint.op, val):
                        to_remove.append(val)
                if to_remove:
                    if other_var.name not in removed:
                        removed[other_var.name] = []
                    for val in to_remove:
                        other_var.domain.remove(val)
                        removed[other_var.name].append(val)
                    if len(other_var.domain) == 0:
                        return False, removed
        elif constraint.var2 == var_name:
            other_var = variables[constraint.var1]
            if other_var.value is None:
                to_remove = []
                for val in other_var.domain:
                    if not check_constraint(val, constraint.op, value):
                        to_remove.append(val)
                if to_remove:
                    if other_var.name not in removed:
                        removed[other_var.name] = []
                    for val in to_remove:
                        other_var.domain.remove(val)
                        removed[other_var.name].append(val)
                    if len(other_var.domain) == 0:
                        return False, removed
    return True, removed


def restore_domains(variables, removed):
    for var_name, values in removed.items():
        variables[var_name].domain.extend(values)


def check_constraint(var1, op, var2):
    if op == '>':
        return var1 > var2
    elif op == '<':
        return var1 < var2
    elif op == '=':
        return var1 == var2
    elif op == '!':
        return var1 != var2


def apply_constraints(variables, constraints):
    for constraint in constraints:
        var1 = variables[constraint.var1].value
        var2 = variables[constraint.var2].value
        if var1 is not None and var2 is not None:
            if not check_constraint(var1, constraint.op, var2):
                return False
    return True


def select_unassigned_variable(variables):
    min_domain = float('inf')
    most_constrained_var = None
    for var in variables.values():
        if var.value is None:
            if len(var.domain) < min_domain:
                min_domain = len(var.domain)
                most_constrained_var = var
    return most_constrained_var


def select_value(var):
    return min(var.domain)


def get_current_assignment(variables):
    assignment = []
    for var in sorted(variables.values(), key=lambda v: v.name):
        if var.value is not None:
            assignment.append(f"{var.name}={var.value}")
    return ", ".join(assignment)


def backtracking_search(variables, constraints, consistency_enforcing):
    branches_visited = []
    result = backtrack(variables, constraints, consistency_enforcing, branches_visited, 0)
    return result, branches_visited


def backtrack(variables, constraints, consistency_enforcing, branches_visited, depth):
    if all(var.value is not None for var in variables.values()):
        return True

    var = select_unassigned_variable(variables)
    for value in sorted(var.domain):
        var.value = value

        can_continue = True
        removed = {}
        if consistency_enforcing == 'fc':
            can_continue, removed = forward_check(variables, constraints, var.name, value)

        if can_continue and apply_constraints(variables, constraints):
            result = backtrack(variables, constraints, consistency_enforcing, branches_visited, depth + 1)
            if result:
                return True

        # Record the branch failure
        assignment = get_current_assignment(variables)
        if not can_continue or not apply_constraints(variables, constraints):
            branches_visited.append(f"{len(branches_visited) + 1}. {assignment} failure")

        # Backtrack
        var.value = None
        if consistency_enforcing == 'fc':
            restore_domains(variables, removed)

    return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py var_file con_file consistency_enforcing")
        sys.exit(1)

    var_file = sys.argv[1]
    con_file = sys.argv[2]
    consistency_enforcing = sys.argv[3]

    variables = read_variables(var_file)
    constraints = read_constraints(con_file)

    result, branches_visited = backtracking_search(variables, constraints, consistency_enforcing)
    for branch in branches_visited:
        print(branch)

    if result:
        print(f"{len(branches_visited) + 1}. {get_current_assignment(variables)} solution")