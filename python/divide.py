import itertools
import sys
from generator import helix
from mealy import product, MealyMachine


def find1(r, lpr, lqr, y):
    for i in range(r.nb_letters):
        if r.delta[lpr][i] == lqr and r.rho[lpr][i] == y:
            return i
    return None


def rec_div(m, r, delta, rho, label, vertices):
    if not vertices:
        return MealyMachine(delta, rho)

    p, x = vertices.pop()
    q, y = m.delta[p][x], m.rho[p][x]
    lpl, lpr = label[p]
    lql, lqr = label[q]

    index = find1(r, lpr, lqr, y)
    if index is None:
        return None

    if (delta[lpl][x] is not None
        and (delta[lpl][x] != lql or rho[lpl][x] != index)):
        return None

    delta[lpl][x] = lql
    rho[lpl][x] = index
    return rec_div(m, r, delta, rho, label, vertices)


def divide_right(m, r):
    couples = [(x, y)
               for x in range(m.nb_states // r.nb_states)
               for y in range(r.nb_states)]
    label = [(i // r.nb_states, i % r.nb_states) for i in range(m.nb_states)]
    delta = [[None for _ in range(m.nb_letters)]
                 for _ in range(m.nb_states // r.nb_states)]
    rho = [[None for _ in range(m.nb_letters)]
               for _ in range(m.nb_states // r.nb_states)]
    vertices = [(x, y) for x in range(m.nb_states)
                    for y in range(m.nb_letters)]

    return rec_div(m, r, delta, rho, label, vertices)


def test_divide(nb_states, nb_letters):
    while True:
        m1 = helix(nb_states, nb_letters)
        m2 = helix(nb_states, nb_letters)
        m = product(m1, m2)
        if m.bireversible():
            break

    ma = divide_right(m, m2)

    print(ma)
    if ma == m1:
        print("C'EST LE BON")
        prod = product(ma, m2)
        return True
#    if prod == m:
#        return True

    return False


def test_divide_n(nb_states, nb_letters, n):
    compteur = 0
    for _ in range(n):
        if test_divide(nb_states, nb_letters):
            compteur += 1
    print(compteur, "/", n)
