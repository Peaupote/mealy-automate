import math
from mealy import MealyMachine, product
from random import randint

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
