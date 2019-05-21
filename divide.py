import itertools

def find1(r, lpr, lqr, y):
    for i in range(r.nb_letters):
        if r.delta[lpr][i] == lqr and r.rho[lpr][i] == y:
            return i
    return False

def rec(m, r, delta, rho, label, vertices):
    if not vertices:
        return delta, rho

    p, x = vertices.pop()
    q, y = m.delta[p][x], m.rho[p][x]
    lpl, lpr = label[p]
    lql, lqr = label[q]

    index = find1(r, lpr, lqr, y)
    if index == False:
        return False

    if delta[lpl][x] != None and delta[lpl][x] != lql and rho[lpl][x] != index:
        return False

    delta[lpl][x] = lql
    rho[lpl][x] = index
    return rec(m, r, delta, rho, label, vertices)


def divide_right(m, r):
    couples = [(x, y)
               for x in range(m.nb_states // r.nb_states)
               for y in range(r.nb_states)]
    div = set()
    for p in itertools.permutation(m.nb_states):
        label = [couples[p[i]] for i in range(m.nb_states)]
        delta = [[None for _ in range(m.nb_letters)]
                 for _ in range(m.nb_states // r.nb_states)]
        rho = [[None for _ in range(m.nb_letters)]
               for _ in range(m.nb_states // r.nb_states)]
        verticles = [(x, y) for x in range(m.nb_states)
                     for y in range(m.nb_letters)]
        res = rec(m, r, delta, rho, label, vertices)
        if res: div.add(res)

    return div
