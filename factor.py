import divide
import generator
import itertools
from mealy import *


def rec_factor(m, label, deltal, rhol, deltar, rhor, vertices, factors, depth):
    depth += 1

    if depth >= len(vertices):
        depth -= 1
        m1 = MealyMachine(deltal, rhol)
        m2 = MealyMachine(deltar, rhor)

        factors.add((m1, m2))
        return

    vertex = vertices[depth]
    p, x = vertex
    q, y = m.delta[p][x], m.rho[p][x]
    # print("  " * depth, "p {}, q {}, x {}, y {}".format(p, q, x, y))

    lpl, lpr = label[p]
    lql, lqr = label[q]
    # print("  " * depth, "lpl {}, lpr {}".format(lpl, lpr))
    # print("  " * depth, "lql {}, lqr {}".format(lql, lqr))

    for z in range(m.nb_letters):  # TODO: do something smart
        # print("  " * depth, "test", z)

        # letter x has a value and its not z. contradiction
        if rhol[lpl][x] is not None and rhol[lpl][x] != z:
            continue

        # letter z has a value and its not y. contradiction
        if rhor[lpr][z] is not None and rhor[lpr][z] != y:
            continue

        prev_deltal = deltal[lpl][x]
        prev_rhol = rhol[lpl][x]

        prev_deltar = deltar[lpr][z]
        prev_rhor = rhor[lpr][z]

        deltal[lpl][x] = lql
        rhol[lpl][x] = z

        deltar[lpr][z] = lqr
        rhor[lpr][z] = y

        # print("  " * depth, deltal, rhol)
        # print("  " * depth, deltar, rhor)
        # print("  " * depth, "-" * 10)

        rec_factor(m, label, deltal, rhol, deltar,
                   rhor, vertices, factors, depth)

        depth -= 1

        deltal[lpl][x] = prev_deltal
        rhol[lpl][x] = prev_rhol

        deltar[lpr][z] = prev_deltar
        rhor[lpr][z] = prev_rhor

    # print("  " * depth, "Impasse")
    depth -= 1


def factor(m):
    factors = set()
    for i in range(2, m.nb_states // 2 + 1):
        if m.nb_states % i != 0:
            continue

        depth = -1
        deltal = [[None for _ in range(m.nb_letters)]
                  for _ in range(i)]
        rhol = [[None for _ in range(m.nb_letters)]
                for _ in range(i)]

        nb_state_r = m.nb_states // i
        deltar = [[None for _ in range(m.nb_letters)]
                  for _ in range(nb_state_r)]
        rhor = [[None for _ in range(m.nb_letters)]
                for _ in range(nb_state_r)]

        vertices = [(x, y)
                    for x in range(m.nb_states)
                    for y in range(m.nb_letters)]

        label = [(j // (nb_state_r), j % (nb_state_r))
                 for j in range(m.nb_states)]

        rec_factor(m, label, deltal, rhol, deltar,
                   rhor, vertices, factors, depth)
        return factors


def test_facto(nb_states_1, nb_letters_1, nb_states_2, nb_letters_2):
    while True:
        m1 = generator.helix(nb_states_1, nb_letters_1)
        m2 = generator.helix(nb_states_2, nb_letters_2)
        m = product(m1, m2)
        if m.bireversible():
            break

    # print(m)
    return len(factor(m)) != 0


def test_facto_n(nb_states_1, nb_letters_1, nb_states_2, nb_letters_2, n):
    c = 0
    for _ in range(n):
        if test_facto(nb_states_1, nb_letters_1, nb_states_2, nb_letters_2):
            c += 1
    print(c, "/", n)


def factor_inv(m):
    factors = set()
    for i in range(2, m.nb_states // 2 + 1):
        if m.nb_states % i == 0:
            tot_class = generator.helix_gen(i, m.nb_letters)
            # iso_class = isomorphism_class(i, m.nb_letters)
            for r in tot_class:
                l = divide.divide_right(m, r)
                if l:
                    factors.add((l, r))
    return factors


def test_factor_inv(nb_states_1, nb_letters_1, nb_states_2, nb_letters_2):
    while True:
        m1 = generator.helix(nb_states_1, nb_letters_1)
        m2 = generator.helix(nb_states_2, nb_letters_2)
        m = product(m1, m2)
        if m.bireversible():
            break

    print(m)
    return factor_inv(m) is not None


def test_facto_inv_n(nb_states_1, nb_letters_1, nb_states_2, nb_letters_2, n):
    c = 0
    for _ in range(n):
        if test_factor_inv(nb_states_1, nb_letters_1, nb_states_2, nb_letters_2):
            c += 1
    print(c, "/", n)


def factor_naive(m):
    factors = set()
    for i in range(2, m.nb_states // 2 + 1):
        if m.nb_states % i != 0:
            continue
        tot_class = generator.helix_gen(i, m.nb_letters)
        for l in tot_class:
            for r in tot_class:
                if product(l, r) == m:
                    factors.add((l, r))
    return factors


def test_all_factors(m):
    factors_naive = factor_naive(m)
    factors_inv = factor_inv(m)
    factors_smart = factor(m)

    inv = False
    smart = False

    if factors_naive == factors_inv:
        inv = True
        print("INV WORKS")
    if factors_naive == factors_smart:
        smart = True
        print("SMART WORKS")

    return inv, smart


def test_all_factors_n(n):
    c_inv = 0
    c_smart = 0
    for _ in range(n):
        inv, smart = test_all_factors(generator.helix(4, 2))
        if inv:
            c_inv += 1
        if smart:
            c_smart += 1
    print("inv", c_inv, "/", n)
    print("smart", c_smart, "/", n)


def test_all_factors_iso(m):
    factors_naive = factor_naive(m)
    factors_smart = factor(m)

    for nl, nr in factors_naive:
        find = False
        for sl, sr in factors_smart:
            if nl.isomorphic(sl) and nr.isomorphic(sr):
                find = True
        if not find:
            return False
    return True


def test_all_factors_iso_n(n):
    c_smart = 0
    for _ in range(n):
        smart = test_all_factors_iso(generator.helix(4, 2))
        if smart:
            c_smart += 1
    print("smart", c_smart, "/", n)
