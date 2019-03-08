
from graphviz import Digraph


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


def init_nerode_class(rho):
    compteur = 0
    cl = [None for i in range(len(rho))]
    for p1 in range(len(rho)):
        if cl[p1] == None:
            cl[p1] = compteur
            compteur += 1
            for p2 in range(p1+1, len(rho)):
                if cl[p2] == None:
                    equivalent = True
                    for x in range(len(rho[0])):
                        if rho[p1][x] != rho[p2][x]:
                            equivalent = False
                    if equivalent:
                        cl[p2] = cl[p1]
    return cl


def next_nerode_class(delta, cl):
    compteur = 0
    new_cl = [None for i in range(len(delta))]
    for p1 in range(len(delta)):
        if new_cl[p1] == None:
            new_cl[p1] = compteur
            compteur += 1
            for p2 in range(p1+1, len(delta)):
                if new_cl[p2] == None and cl[p1] == cl[p2]:
                    equivalent = True
                    for x in range(len(delta[0])):
                        if cl[delta[p1][x]] != cl[delta[p2][x]]:
                            equivalent = False
                    if equivalent:
                        new_cl[p2] = new_cl[p1]
    return new_cl


def fusion(machine, cl):
    delta, rho = machine
    new_delta, new_rho = [], []

    for p in range(len(delta)):
        if p == cl[p]:
            new_delta.append(list(delta[p]))
            new_rho.append(list(rho[p]))

    for p in range(len(new_delta)):
        for x in range(len(new_delta[0])):
            new_delta[p][x] = cl[delta[p][x]]

    return new_delta, new_rho


def minimize(machine):
    delta, rho = machine
    stop = False
    cl = init_nerode_class(rho)
    while not stop:
        new_cl = next_nerode_class(delta, cl)
        if new_cl == cl:
            stop = True
        else:
            cl = new_cl
    return fusion(machine, cl)


def md_reduction(machine):
    prev, current = None, machine
    while prev != current:
        prev, current = current, minimize(current)
        if current == prev:  # automaton is minimal
            prev = dual(prev)
            current = minimize(prev)
    return current


def show(machine):
    in_matrix, out_matrix = machine

    graph = Digraph(comment="Mealy Machine")
    graph.attr(rankdir='LR')

    for i in range(len(in_matrix)):
        graph.node(str(i))

    graph.attr('node', shape='circle')

    for p in range(len(in_matrix)):
        edges = {}
        for x in range(len(in_matrix[0])):
            key = str(in_matrix[p][x])
            if key in edges:
                edges[key] = edges[key] + "\n" + \
                    str(x) + " | " + str(out_matrix[p][x])
            else:
                edges[key] = str(x) + " | " + str(out_matrix[p][x])
        for key in edges:
            graph.edge(str(p), key, label=edges[key])

    graph.view()
