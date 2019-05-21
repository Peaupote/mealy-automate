import itertools
from generator import helix
from mealy import product, MealyMachine

COMPTEUR = 0


def find1(r, lpr, lqr, y):
    # print("delta", r.delta)
    # print("rho", r.rho)
    # print("lpr", lpr, "lqr", lqr, "y", y)
    for i in range(r.nb_letters):
        # print(r.delta[lpr][i], " = ", lqr, " - ", r.rho[lpr][i], " = ", y)
        if r.delta[lpr][i] == lqr and r.rho[lpr][i] == y:
            return i
    return None


def rec(m, r, delta, rho, label, vertices):
    global COMPTEUR
    COMPTEUR += 1
    # print(COMPTEUR)
    if not vertices:
        return delta, rho

    p, x = vertices.pop()
    q, y = m.delta[p][x], m.rho[p][x]
    lpl, lpr = label[p]
    lql, lqr = label[q]

    index = find1(r, lpr, lqr, y)
    if index == None:
        print("PREMIER")
        return False

    if delta[lpl][x] != None and delta[lpl][x] != lql and rho[lpl][x] != index:
        print("DEUXIEME")
        return False

    delta[lpl][x] = lql
    rho[lpl][x] = index
    return rec(m, r, delta, rho, label, vertices)


def divide_right(m, r):
    couples = [(x, y)
               for x in range(m.nb_states // r.nb_states)
               for y in range(r.nb_states)]
    div = set()
    nb_permut = 0
    for p in itertools.permutations(list(range(m.nb_states))):
        nb_permut += 1
        print("Permutation", nb_permut)
        label = [couples[p[i]] for i in range(m.nb_states)]
        delta = [[None for _ in range(m.nb_letters)]
                 for _ in range(m.nb_states // r.nb_states)]
        rho = [[None for _ in range(m.nb_letters)]
               for _ in range(m.nb_states // r.nb_states)]
        vertices = [(x, y) for x in range(m.nb_states)
                    for y in range(m.nb_letters)]
        res = rec(m, r, delta, rho, label, vertices)
        if res:
            div.add(MealyMachine(res[0], res[1]))

    return div


def test_divide(nb_states, nb_letters):
    while True:
        m1 = helix(nb_states, nb_letters)
        m2 = helix(nb_states, nb_letters)
        m = product(m1, m2)
        if m.bireversible():
            break

    find = False
    res = divide_right(m, m2)
    for ma in res:
        print(ma)
        if ma == m1:
            print("C'EST LE BON")
            find = True
        prod = product(ma, m2)
        if not prod.bireversible():
            print("PAS BIREV")
        if prod != m:
            print("PUTAINS")
    print(len(res))
    return find


def test_divide_n(nb_states, nb_letters, n):
    compteur = 0
    for _ in range(n):
        if test_divide(nb_states, nb_letters):
            compteur += 1
    print(compteur, "/", n)
