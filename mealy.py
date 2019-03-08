def execute(entry, state, machine):
    in_matrix, out_matrix = machine
    out = []
    for w in entry:
        out.append(out_matrix[state][w])
        state = in_matrix[state][w]
    return out

def dual(machine):
    in_matrix, out_matrix = machine
    delta = [[None for i in range(len(in_matrix))] for j in range(len(in_matrix[0]))]
    rho = [[None for i in range(len(in_matrix))] for j in range(len(in_matrix[0]))]
    for p in range(len(in_matrix)):
        for x in range(len(in_matrix[0])):
            q, y = in_matrix[p][x], out_matrix[p][x]
            if delta[x][p] != None: return False
            delta[x][p] = out_matrix[p][x]
            rho[x][p] = in_matrix[p][x]
    return delta, rho

def inverse(machine):
    in_matrix, out_matrix = machine
    delta = in_matrix[:]
    rho = [[None for i in range(len(in_matrix[0]))] for j in range(len(in_matrix))]
    for p in range(len(in_matrix)):
        for x in range(len(in_matrix[0])):
            q, y = in_matrix[p][x], out_matrix[p][x]
            if rho[p][y] != None: return False
            rho[p][y] = x
    return delta, rho

def bireversible(machine):
    inv = inverse(machine)
    return inv and dual(inv)

def minimize(machine):
    # TODO
    return machine

def md_reduction(machine):
    prev, current = None, machine
    while prev != current:
        prev, current = current, minimize(current)
        if current == prev: # automaton is minimal
            prev = dual(prev)
            current = minimize(prev)
    return current
