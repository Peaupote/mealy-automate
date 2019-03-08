def execute(entry, state, machine):
    in_matrix, out_matrix = machine
    out = []
    for w in entry:
        out.append(out_matrix[state][w])
        state = in_matrix[state][w]
    return out


def dual(machine):
    in_matrix, out_matrix = machine
    delta = [[None for i in range(len(in_matrix))]
             for j in range(len(in_matrix[0]))]
    rho = [[None for i in range(len(in_matrix))]
           for j in range(len(in_matrix[0]))]
    for p in range(len(in_matrix)):
        for x in range(len(in_matrix[0])):
            q, y = in_matrix[p][x], out_matrix[p][x]
            if delta[x][p] != None:
                return False
            delta[x][p] = out_matrix[p][x]
            rho[x][p] = in_matrix[p][x]
    return delta, rho


def inverse(machine):
    in_matrix, out_matrix = machine
    delta = list(in_matrix)
    rho = [[None for i in range(len(in_matrix[0]))]
           for j in range(len(in_matrix))]
    for p in range(len(in_matrix)):
        for x in range(len(in_matrix[0])):
            q, y = in_matrix[p][x], out_matrix[p][x]
            if rho[p][y] != None:
                return False
            rho[p][y] = x
    return delta, rho


def bireversible(machine):
    inv = inverse(machine)
    return inv and dual(inv)


def minimize(machine):
    in_matrix, out_matrix = machine
    delta = list(in_matrix)
    rho = list(out_matrix)
    stop = False
    replace = []
    keep = [i for i in range(len(delta))]
    while not stop:
        stop = True
        # On cherche les pairs de sommets à fusionner
        for p1 in range(len(delta)):
            for p2 in range(p1+1, len(delta)):
                fusion = True
                for x in range(len(delta[0])):
                    if (delta[p1][x] != delta[p2][x] or
                            rho[p1][x] != rho[p2][x]):
                        fusion = False
                        break
                # Si toutes les liaisons sont identiques, on fusionnent
                if fusion:
                    stop = False
                    replace.append((p1, p2))

        # On les fusionnent effectivement
        for p1, p2 in replace:
            keep.remove(p2)
            # On remplace les arcs arrivant sur p2 par des arcs arrivant sur p1
            for p in range(len(delta)):
                for x in range(len(delta[0])):
                    if delta[p][x] == p2:
                        delta[p][x] = p1

        # On réindice
        new_delta = []
        new_rho = []
        for p in keep:
            new_delta.append(delta[p])
            new_rho.append(rho[p])
        delta = new_delta
        rho = new_rho

        for i in range(len(keep)):
            if i != keep[i]:
                for p in range(len(delta)):
                    for x in range(len(delta[0])):
                        if delta[p][x] == keep[i]:
                            delta[p][x] = i

        # On réinitilise keep et replace
        keep = [i for i in range(len(delta))]
        replace = []

    return delta, rho


def md_reduction(machine):
    prev, current = None, machine
    while prev != current:
        prev, current = current, minimize(current)
        if current == prev:  # automaton is minimal
            prev = dual(prev)
            current = minimize(prev)
    return current
