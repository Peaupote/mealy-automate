import generator
from mealy import *

def is_full(tab):
    for x in tab:
        for y in x:
            if y is None:
                return False
    return True

depth = 0
def rec_factor(m, deltal, rhol, deltar, rhor, vertices):
    global depth
    depth += 1
    if not vertices:
        depth -= 1
        if ((not is_full(deltal)) or (not is_full(deltar))
            or (not is_full(rhol)) or (not is_full(rhor))):
            return None
        m1 = MealyMachine(deltal, rhol)
        m2 = MealyMachine(deltar, rhor)
        if product(m1, m2) == m:
            return m1, m2
        return None

    vertex = vertices.pop()
    p, x = vertex
    q, y = m.delta[p][x], m.rho[p][x]
    print("  " * depth, "p {}, q {}, x {}, y {}".format(p, q, x, y))

    lpl, lpr = p // len(deltar), p % len(deltar)
    lql, lqr = q // len(deltar), p % len(deltar)
    print("  " * depth, "lpl {}, lpr {}".format(lpl, lpr))
    print("  " * depth, "lql {}, lqr {}".format(lql, lqr))

    for z in range(m.nb_letters): # TODO: do something smart
        print("  " * depth, "test", z)

        # letter x has a value and its not z. contradiction
        if rhol[lpl][x] is not None and rhol[lpl][x] != z:
            continue

        # letter z has a value and its not y. contradiction
        if rhor[lpr][z] is not None and rhol[lpr][z] != y:
            continue

        deltal[lpl][x] = lql
        rhol[lpl][x] = z

        deltar[lpr][z] = lqr
        rhor[lpr][z] = y

        print("  " * depth, deltal, rhol)
        print("  " * depth, deltar, rhor)
        print("  " * depth, "-" * 10)

        res = rec_factor(m, deltal, rhol, deltar, rhor, vertices)
        if res is not None:
            depth -= 1
            return res

        deltal[lpl][x] = None
        rhol[lpl][x] = None

        deltar[lpr][z] = None
        rhor[lpr][z] = None

    print("  " * depth, "Impasse")
    depth -= 1
    # append and pop is not necessary and inefficient
    # a simple integer should do the job
    vertices.append(vertex)
    return None


def factor(m):
    for i in range(2, m.nb_states):
        if m.nb_states % i != 0:
            continue

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

        return rec_factor(m, deltal, rhol, deltar, rhor, vertices)


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
