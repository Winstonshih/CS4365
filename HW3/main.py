# Skyler Lee (HXL220052)
# Winston Shih (WXS190012)
# CS4365.004 HW3

import sys

# parse line (ex: ~p q) to ordered list of strings
def parse_clause(line):
    tokens = [t for t in line.strip().split(' ') if t != '']
    # remove duplicates, but preserve order
    seen = set()
    literals = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            literals.append(t)
    return literals

# given a literal, return the negated version
def negate_literal(literal):
    if literal.startswith('~'):
       return literal[1:]
    else:
        return '~' + literal

# check if clause is tautology
def is_tautology(clause):
    givenSet = set(clause)
    for literal in list(givenSet):
        if negate_literal(literal) in givenSet:
            return True
    return False

# just for formatting clauses, if it is a constradiction or not
def format_clause(clause):
    if clause is None:
        return "Contradiction"
    if not clause:
        return ""
    return ' '.join(clause)

# add clause to KB, return true if added, false if not
# knowledgebase is a list of dicts defined in main
# parents is a tuple that led to this clause (can be None)
def add_clause(knowledgebase, clause_signatures, clause_literals, parents=None):
    # remove duplicate literals, keep the original order
    unique_literals = []
    for literal in clause_literals:
        if literal not in unique_literals:
            unique_literals.append(literal)

    # ignore tautologies (ex L and ~L)
    if is_tautology(unique_literals):
        return False

    # make signature to detect duplicates
    signature = tuple(sorted(unique_literals))

    if signature in clause_signatures:
        # clause already exists in knowledgebase
        return False

    # put new clause in the knowledgebase
    clause_signatures.add(signature)
    knowledgebase.append({
        "clause": unique_literals,
        "parents": parents
    })
    return True

def resolvents(ci, cj):
    result = []
    # for each literal in ci
    for li in ci:
        opposite = negate_literal(li)
        # if opposite of the literal in cj
        if opposite in cj:
            # build new clause (ci without literal) + (cj without ~literal)
            # skip duplicates for each of those
            new_clause = []

            # add from ci, skip li, duplicates
            for lit in ci:
                if lit != li and lit not in new_clause:
                    new_clause.append(lit)

            # add from cj, skip opposite, duplicates
            for lit in cj:
                if lit != opposite and lit not in new_clause:
                    new_clause.append(lit)

            # skip tautologies (p, ~p, etc)
            if not is_tautology(new_clause):
                result.append(new_clause)

    return result


# print all the clauses in order
# print contradiction if necessary then valid or fail at the end
def print_kb_and_result(knowledge_base, is_valid):
    for line_number, item in enumerate(knowledge_base, start=1):
        clause_literals = item["clause"]
        parent_indices = item["parents"] # this is a tuple or None

        if clause_literals is None:
            # empty clause so this is a contradiction
            print(f"{line_number}. Contradiction {{{parent_indices[0]},{parent_indices[1]}}}")
            continue

        clause_text = format_clause(clause_literals)

        if parent_indices is None:
            parents_text = "{}"
        else:
            parents_text = f"{{{parent_indices[0]},{parent_indices[1]}}}"

        print(f"{line_number}. {clause_text} {parents_text}")

    if is_valid:
        print("Valid")
    else:
        print("Fail")


def main():
    input_file = sys.argv[1]

    # read lines from file
    lines = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip() # strip spacings
            if s: # if valid line, add it
                lines.append(s)
    if not lines:
        print("Failed to read")
        return

    # split kb and other lines
    original_query_line = lines[-1]
    initial_kb_lines = lines[:-1]

    # KB and the other signature
    knowledge_base = []
    clause_signatures = set()

    # add all the given KB clauses
    for kb_line in initial_kb_lines:
        add_clause(knowledge_base, clause_signatures, parse_clause(kb_line), parents=None)

    # add the negated clause
    for lit in parse_clause(original_query_line):
        add_clause(knowledge_base, clause_signatures, [negate_literal(lit)], parents=None)

    # compute
    i = 0
    while i < len(knowledge_base):
        ci = knowledge_base[i]["clause"]
        j = 0
        while j < i:
            cj = knowledge_base[j]["clause"]
            for new_clause in resolvents(ci, cj):
                if not new_clause: # empty clause means contradiction
                    knowledge_base.append({"clause": None, "parents": (i+1, j+1)})
                    print_kb_and_result(knowledge_base, is_valid=True)
                    return
                add_clause(knowledge_base, clause_signatures, new_clause, parents=(i+1, j+1))
            j += 1
        i += 1

    # no contradiction
    print_kb_and_result(knowledge_base, is_valid=False)

if __name__ == "__main__":
    main()
