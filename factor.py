import divide
import generator
from mealy import *
import sys, time, random as rand
import matplotlib.pyplot as plt

def rec_factor(m, label, deltal, rhol, deltar, rhor, vertices, factors, depth):
    depth += 1

    if depth >= len(vertices):
        depth -= 1
        m1 = MealyMachine(deltal, rhol)
        m2 = MealyMachine(deltar, rhor)

        if product(m1, m2) != m:
            return
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

        deltal[lpl][x] = prev_deltal
        rhol[lpl][x] = prev_rhol

        deltar[lpr][z] = prev_deltar
        rhor[lpr][z] = prev_rhor

    # print("  " * depth, "Impasse")
    depth -= 1


def factor(m):
    factors = set()
    for i in range(2, m.nb_states):
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


def test_facto():
    while True:
        m1 = generator.helix(3, 5)
        m2 = generator.helix(3, 5)
        m = product(m1, m2)
        if m.bireversible():
            break

    print(m)
    return len(factor(m)) != 0


def test_facto_n(n):
    c = 0
    for _ in range(n):
        if test_facto():
            c += 1
    print(c, "/", n)

def factor_inv(m, debug=False):
    factors = set()
    for i in range(2, m.nb_states // 2 + 1):
        if m.nb_states % i == 0:
            if not (i, m.nb_letters) in helix_cache:
                print("noo", i, m.nb_letters)
                helix_cache[(i, m.nb_letters)] = generator.helix_gen(i, m.nb_letters)
            # iso_class = isomorphism_class(i, m.nb_letters)
            for mb in helix_cache[(i, m.nb_letters)]:
                ma = divide.divide_right(m, mb)
                if ma:
                    factors.add((ma, mb))
    return factors


def test_factor_inv():
    while True:
        m1 = generator.helix(3, 3)
        m2 = generator.helix(3, 3)
        m = product(m1, m2)
        if m.bireversible():
            break

    print(m)
    return factor_inv(m) is not None


def test_facto_inv_n(n):
    c = 0
    for _ in range(n):
        if test_factor_inv():
            c += 1
    print(c, "/", n)

def perf_facto(fname, f, test_size, test_set, x):
    bar = [0] * test_size
    count = [0] * test_size

    for m in test_set:
        tstart = time.time()
        f(m)
        tend = time.time()
        index = m.nb_states * m.nb_letters - 1
        bar[index] += tend - tstart
        count[index] += 1

    for i in range(test_size):
        if count[i] != 0:
            bar[i] /= count[i]

    return bar

def perf_func(test_size, funcs):
    test_set = []
    for i in range(1, test_size):
        for j in range(test_size):
            if i * j <= test_size:
                for _ in range(2):
                    test_set.append(generator.helix(i, j))
                    print("Generated", len(test_set))
    print("Test set generated")
    bars = []
    for f in funcs:
        bars.append(perf_facto(f[0], f[1], len(test_set) // 2, test_set, x))

    plt.figure(1)
    ind = list(range(len(test_set) // 2))
    for i in range(len(bars)):
        plt.subplot(1, 2, i + 1)
        plt.bar(ind, bars[i], 1)
        plt.title(funcs[i][0])

    plt.show()

if __name__ == "__main__":
    print("Fill cache")
    helix_cache = dict()
    for x in range(1, 4):
        for y in range(1, 3):
            helix_cache[(x, y)] = generator.helix_gen(x, y)

    print("Perf func")
    perf_func(25, [("factor", factor), ("inv", factor_inv)])
