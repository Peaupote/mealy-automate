import generator
from mealy import *
import itertools

depth = -1
def rec_factor(m, label, deltal, rhol, deltar, rhor, vertices):
    global depth
    depth += 1
    if depth >= len(vertices):
        depth -= 1
        m1 = MealyMachine(deltal, rhol)
        m2 = MealyMachine(deltar, rhor)
        if product(m1, m2) == m:
            return m1, m2
        return None

    vertex = vertices[depth]
    p, x = vertex
    q, y = m.delta[p][x], m.rho[p][x]
    print("  " * depth, "p {}, q {}, x {}, y {}".format(p, q, x, y))

    lpl, lpr = label[p]
    lql, lqr = label[q]
    print("  " * depth, "lpl {}, lpr {}".format(lpl, lpr))
    print("  " * depth, "lql {}, lqr {}".format(lql, lqr))

    for z in range(m.nb_letters): # TODO: do something smart
        print("  " * depth, "test", z)

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

        print("  " * depth, deltal, rhol)
        print("  " * depth, deltar, rhor)
        print("  " * depth, "-" * 10)

        res = rec_factor(m, label, deltal, rhol, deltar, rhor, vertices)
        if res is not None:
            depth -= 1
            return res

        deltal[lpl][x] = prev_deltal
        rhol[lpl][x] = prev_rhol

        deltar[lpr][z] = prev_deltar
        rhor[lpr][z] = prev_rhor

    print("  " * depth, "Impasse")
    depth -= 1
    return None


def factor(m):
    global depth
    for i in range(2, m.nb_states):
        if m.nb_states % i != 0:
            continue

        depth = -1
        deltal = [[None for _ in range(m.nb_letters)]
                  for _ in range(i)]
        rhol = [[None for _ in range(m.nb_letters)]
                for _ in range(i)]

        deltar = [[None for _ in range(m.nb_letters)]
                  for _ in range(m.nb_states // i)]
        rhor = [[None for _ in range(m.nb_letters)]
                  for _ in range(m.nb_states // i)]

        vertices = [(x, y)
                    for x in range(m.nb_states)
                    for y in range(m.nb_letters)]

        couples = [(x, y) for x in range(i) for y in range(m.nb_states // i)]
        for p in itertools.permutations(range(m.nb_states)):
            label = [couples[p[i]] for i in range(m.nb_states)]
            res = rec_factor(m, label, deltal, rhol, deltar, rhor, vertices)
            if res:
                return res


def test_facto():
    while True:
        m1 = generator.helix(2, 2)
        m2 = generator.helix(2, 2)
        m = product(m1, m2)
        if m.bireversible():
            break

    print(m)
    return factor(m) is not None

def test_facto_n(n):
    c = 0
    for _ in range(n):
        if test_facto():
            c += 1
    print(c, "/", n)
