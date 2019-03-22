
import math
from mealy import MealyMachine, product
from random import randint, sample
from copy import deepcopy

basilica = MealyMachine(
    [[1, 2], [0, 2], [2, 2], [4, 2], [2, 3], [6, 2], [2, 5]],
    [[0, 1], [1, 0], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0]])

grigorchuk = MealyMachine(
    [[4, 4], [0, 2], [0, 3], [4, 1], [4, 4]],
    [[1, 0], [0, 1], [0, 1], [0, 1], [0, 1]])

# md reduce to trivial pair
sample1 = MealyMachine(
    [[1, 0, 1, 0], [0, 1, 0, 1]],
    [[1, 0, 3, 2], [3, 0, 1, 2]],
    ['a', 'b'])

# generate group of order 1 494 186 269 970 473 680 896
sample2 = MealyMachine([[0, 0, 0], [0, 2, 1], [1, 1, 1]],
                       [[2, 1, 0], [2, 1, 0], [1, 2, 0]])

fantastique1 = MealyMachine([[0, 1, 2], [1, 0, 3], [3, 2, 0], [2, 3, 1]],
                            [[2, 0, 1], [2, 1, 0], [1, 2, 0], [0, 2, 1]],
                            ['a', 'b', 'c', 'd'], name="fantastique1")

fantastique2 = MealyMachine([[1, 2, 3], [0, 3, 2], [3, 1, 0], [2, 0, 1]],
                            [[1, 0, 2], [2, 0, 1], [1, 2, 0], [2, 1, 0]],
                            ['a', 'b', 'c', 'd'], name="fantastique2")

fantastique3 = MealyMachine([[0, 1, 2], [1, 0, 3], [3, 2, 0], [2, 3, 1]],
                            [[0, 2, 1], [1, 2, 0], [2, 0, 1], [2, 1, 0]],
                            ['a', 'b', 'c', 'd'], name="fantastique3")


def random_machine(nb_states, nb_letters):
    in_ret = [[randint(0, nb_states - 1)
               for i in range(nb_letters)] for j in range(nb_states)]
    out_ret = [[randint(0, nb_letters - 1)
                for i in range(nb_letters)] for j in range(nb_states)]
    return MealyMachine(in_ret, out_ret)


def random_permutation(n):
    lst = list(range(n))
    for i in range(n):
        j = randint(i, n - 1)
        lst[i], lst[j] = lst[j], lst[i]
    return lst


def random_inv(nb_states, nb_letters):
    in_ret = [[randint(0, nb_states - 1)
               for i in range(nb_letters)] for j in range(nb_states)]
    out_ret = [[None for i in range(nb_letters)] for j in range(nb_states)]
    for p in range(nb_states):
        rho = random_permutation(nb_letters)
        for x in range(nb_letters):
            out_ret[p][x] = rho[x]
    return MealyMachine(in_ret, out_ret)


def random_birev(nb_states, nb_letters):
    compteur = 0
    while True:
        compteur += 1
        if compteur % 1000 == 0:
            print(compteur)
        m = random_inv(nb_states, nb_letters)
        if m.bireversible():
            return m


def dumb_factorization(m):
    for i in range(1, int(math.sqrt(m.nb_states))):
        if m.nb_states % i == 0:
            for _ in range(100):
                a = random_machine(i, m.nb_letters)
                b = random_machine(m.nb_states // i, m.nb_letters)
                if product(a, b) == m:
                    return a, b
    return None


def __valid_delta(delta):
    for x in range(len(delta[0])):
        out = [False] * len(delta)
        for p in range(len(delta)):
            if delta[p][x] is None:
                continue
            elif out[delta[p][x]]:
                return False
            out[delta[p][x]] = True
    return True


def __valid_rho(rho):
    for p in range(len(rho)):
        out = [False] * len(rho[p])
        for x in range(len(rho[p])):
            if rho[p][x] is None:
                continue
            elif out[rho[p][x]]:
                return False
            out[rho[p][x]] = True
    return True


def __valid_vertex(v, start, prev, delta, rho):
    p, x = v
    for i in range(len(delta)):
        if delta[i][x] == p:
            return False
    for i in range(len(delta[0])):
        if rho[p][i] == x:
            return False

    if start:
        print("COMPLEXE")
        p_prev, x_prev = prev
        p_start, x_start = start
        new_delta = deepcopy(delta)
        new_rho = deepcopy(rho)
        new_delta[p_prev][x_prev] = p
        new_rho[p_prev][x_prev] = x
        for i in range(len(delta)):
            if new_delta[p_start][x_start] == p_start:
                return False
        for i in range(len(delta[0])):
            if new_rho[p_start][i] == x_start:
                return False
    return True


def __populate_cycles(cycles, suites,  start, prev, vertices, delta, rho):
    print("---------")
    # if not vertices:
    #     p, x = prev
    #     delta[p][x] = start[0]
    #     rho[p][x] = start[1]
    #     return delta, rho

    options = list(filter(lambda v: __valid_vertex(
        v, start if cycles[0] == 1 else None, prev, delta, rho), vertices))
    if cycles[0] == 0:
        print("CYCLES FIN")
        p, x = prev
        delta[p][x] = start[0]
        rho[p][x] = start[1]
        print("populate ", cycles)
        print("suites", suites)
        print("delta", delta)
        print("rho", rho)
        print("start", start)
        print("prev", prev)
        print("vertices", vertices)
        print("options", options)
        cycles.pop(0)
        if not __valid_delta(delta) or not __valid_rho(rho):
            print("INVALIDE")
            return False
        elif not cycles:
            return delta, rho
        else:
            print("NOUVEAU CYCLES")
            new_start = vertices.pop()
            prev = new_start
            start = new_start
            suites.append(new_start)
            cycles[0] -= 1

            new_delta, new_rho = deepcopy(delta), deepcopy(rho)
            res = __populate_cycles(list(cycles), list(suites), new_start, new_start,
                                    list(vertices), new_delta, new_rho)
            if res:
                return res
            suites.pop()
            cycles[0] += 1
            return False

    # print(options)
    if not options:
        print("Pas d'options")
        return False

    for q, y in options:
        # print("boucles", q, y)
        new_delta, new_rho = deepcopy(delta), deepcopy(rho)
        p, x = prev
        new_delta[p][x] = q
        new_rho[p][x] = y
        print("populate ", cycles)
        print("suites", suites)
        print("delta", delta)
        print("rho", rho)
        print("start", start)
        print("prev", prev)
        print("vertices", vertices)
        print("options", options)
        suites.append((q, y))
        cycles[0] -= 1
        res = __populate_cycles(list(cycles), list(suites), start, (q, y),
                                list(filter(lambda v: v != (q, y), vertices)),
                                new_delta, new_rho)
        if res:
            return res
        suites.pop()
        cycles[0] += 1
    return False


def helix_birev(nb_states, nb_letters):
    cycles = []
    c, size = 0, nb_states * nb_letters
    while c < size:
        s = randint(1, size - c)
        cycles.append(s)
        c += s
    # cycles = [4]

    print("CYCLES :", cycles)
    vertices = []
    suites = []
    for p in range(nb_states):
        for x in range(nb_letters):
            vertices.append((p, x))
    delta = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    rho = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    sample(vertices, len(vertices))
    print("vertices", vertices)
    for _ in range(len(vertices)):
        start = vertices.pop(0)
        suites.append(start)
        cycles[0] -= 1
        # print(start)
        res = __populate_cycles(
            list(cycles), list(suites), start, start, list(vertices), deepcopy(delta), deepcopy(rho))
        if res:
            return MealyMachine(*res)
        vertices.append(start)
    return False


def cycles_to_mealy_machines(cycles, nb_states, nb_letters):
    delta = [[None for i in range(nb_letters)]
             for j in range(nb_states)]
    rho = [[None for i in range(nb_letters)]
           for j in range(nb_states)]
    for C in cycles:
        for i in range(0, len(C)):
            prev_state, prev_letter = C[i-1]
            state, letter = C[i]
            # print(prev_state, prev_letter)
            delta[prev_state][prev_letter] = state
            rho[prev_state][prev_letter] = letter
    return MealyMachine(delta, rho)


H = helix_birev(2, 2)


def random_helix_birev(nb_states, nb_letters):
    compteur = 0
    while True:
        compteur += 1
        if compteur % 1000 == 0:
            print(compteur)
        m = helix_birev(nb_states, nb_letters)
        if m.bireversible():
            return m


birev33 = [MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                        [[0, 2, 1], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                        [[0, 2, 1], [1, 2, 0], [2, 1, 0]]),
           MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                        [[0, 2, 1], [2, 1, 0], [2, 1, 0]]),
           MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                        [[1, 0, 2], [0, 2, 1], [0, 2, 1]]),
           MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                        [[1, 0, 2], [0, 2, 1], [2, 0, 1]]),
           MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                        [[1, 0, 2], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 0, 0], [1, 2, 2], [2, 1, 1]],
                        [[0, 2, 1], [1, 0, 2], [1, 0, 2]]),
           MealyMachine([[0, 0, 0], [1, 2, 2], [2, 1, 1]],
                        [[0, 2, 1], [1, 0, 2], [1, 2, 0]]),
           MealyMachine([[0, 0, 0], [1, 2, 2], [2, 1, 1]],
                        [[0, 2, 1], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 0, 0], [1, 2, 2], [2, 1, 1]],
                        [[1, 0, 2], [2, 0, 1], [2, 0, 1]]),
           MealyMachine([[0, 0, 0], [1, 2, 2], [2, 1, 1]],
                        [[1, 0, 2], [2, 0, 1], [2, 1, 0]]),
           MealyMachine([[0, 0, 0], [1, 2, 2], [2, 1, 1]],
                        [[1, 0, 2], [2, 1, 0], [2, 1, 0]]),
           MealyMachine([[0, 0, 0], [2, 2, 2], [1, 1, 1]],
                        [[0, 2, 1], [1, 0, 2], [1, 2, 0]]),
           MealyMachine([[0, 0, 0], [2, 2, 2], [1, 1, 1]],
                        [[0, 2, 1], [1, 0, 2], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [1, 2, 0], [2, 1, 2]],
                        [[0, 2, 1], [2, 0, 1], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [1, 2, 0], [2, 1, 2]],
                        [[2, 0, 1], [2, 0, 1], [1, 0, 2]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[0, 2, 1], [2, 0, 1], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[0, 2, 1], [2, 1, 0], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[1, 2, 0], [1, 0, 2], [1, 2, 0]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[1, 2, 0], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[2, 0, 1], [2, 0, 1], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[2, 0, 1], [2, 1, 0], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[2, 1, 0], [1, 0, 2], [1, 2, 0]]),
           MealyMachine([[0, 0, 1], [1, 2, 2], [2, 1, 0]],
                        [[2, 1, 0], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[0, 2, 1], [1, 0, 2], [0, 2, 1]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[0, 2, 1], [1, 0, 2], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[0, 2, 1], [2, 1, 0], [0, 2, 1]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[0, 2, 1], [2, 1, 0], [2, 0, 1]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[1, 2, 0], [0, 2, 1], [1, 2, 0]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[1, 2, 0], [0, 2, 1], [2, 1, 0]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[1, 2, 0], [1, 0, 2], [1, 2, 0]]),
           MealyMachine([[0, 0, 1], [2, 2, 2], [1, 1, 0]],
                        [[1, 2, 0], [1, 0, 2], [2, 1, 0]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[1, 0, 2], [0, 2, 1], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[1, 0, 2], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[1, 2, 0], [0, 2, 1], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[1, 2, 0], [1, 2, 0], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[2, 0, 1], [1, 0, 2], [2, 0, 1]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[2, 0, 1], [2, 0, 1], [2, 0, 1]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[2, 1, 0], [1, 0, 2], [2, 0, 1]]),
           MealyMachine([[0, 1, 1], [2, 0, 2], [1, 2, 0]],
                        [[2, 1, 0], [2, 0, 1], [2, 0, 1]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 0, 2], [0, 2, 1], [1, 0, 2]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 0, 2], [0, 2, 1], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 0, 2], [2, 1, 0], [1, 0, 2]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 0, 2], [2, 1, 0], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 2, 0], [0, 2, 1], [1, 0, 2]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 2, 0], [0, 2, 1], [1, 2, 0]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 2, 0], [2, 1, 0], [1, 0, 2]]),
           MealyMachine([[0, 1, 1], [2, 2, 2], [1, 0, 0]],
                        [[1, 2, 0], [2, 1, 0], [1, 2, 0]]),
           MealyMachine([[0, 1, 2], [1, 2, 0], [2, 0, 1]],
                        [[0, 1, 2], [2, 0, 1], [1, 2, 0]]),
           MealyMachine([[0, 1, 2], [1, 2, 0], [2, 0, 1]],
                        [[0, 2, 1], [1, 0, 2], [2, 1, 0]]),
           MealyMachine([[0, 1, 2], [2, 0, 1], [1, 2, 0]],
                        [[0, 1, 2], [1, 2, 0], [2, 0, 1]]),
           MealyMachine([[0, 1, 2], [2, 0, 1], [1, 2, 0]],
                        [[0, 2, 1], [2, 1, 0], [1, 0, 2]]),
           MealyMachine([[0, 1, 2], [2, 2, 0], [1, 0, 1]],
                        [[1, 2, 0], [1, 2, 0], [0, 2, 1]]),
           MealyMachine([[0, 1, 2], [2, 2, 0], [1, 0, 1]],
                        [[1, 2, 0], [2, 1, 0], [1, 2, 0]]),
           MealyMachine([[1, 1, 1], [2, 2, 2], [0, 0, 0]],
                        [[0, 2, 1], [1, 0, 2], [1, 2, 0]]),
           MealyMachine([[1, 1, 1], [2, 2, 2], [0, 0, 0]],
                        [[0, 2, 1], [1, 0, 2], [2, 0, 1]])]

for indice, machine in enumerate(birev33):
    machine.name = "birev33_" + str(indice)


def count_cycle_size(H):
    cycles = {}
    done = set()
    for i in H:
        if i in done:
            continue
        done.add(i)
        j = H[i]
        length = 1
        while j != i:
            done.add(j)
            j = H[j]
            length += 1
        if length not in cycles:
            cycles[length] = 0
        cycles[length] += 1
    return cycles


def count_cycle_size_in_inverse():
    for i in range(len(birev33)):
        h1 = birev33[i].helix_graph()
        h2 = birev33[i].inverse().helix_graph()
        c1 = count_cycle_size(h1)
        c2 = count_cycle_size(h2)
        print(i, c1, c2)


def count_cycle_size_in_product():
    for i in range(len(birev33)):
        b1 = birev33[i]
        for j in range(i, len(birev33)):
            b2 = birev33[j]
            h1 = b1.helix_graph()
            h2 = b2.helix_graph()
            h3 = product(b1, b2).helix_graph()
            c1 = count_cycle_size(h1)
            c2 = count_cycle_size(h2)
            c3 = count_cycle_size(h3)
            print(i, c1, c2, c3)
