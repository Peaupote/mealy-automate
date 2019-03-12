import random
from mealy import *

basilica = MealyAutomaton( \
    [[1, 2], [0, 2], [2, 2], [4, 2], [2, 3], [6, 2], [2, 5]],
    [[0, 1], [1, 0], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0]])

grigorchuk = MealyAutomaton( \
    [[4, 4], [0, 2], [0, 3], [4, 1], [4, 4]],
    [[1, 0], [0, 1], [0, 1], [0, 1], [0, 1]])

# md reduce to trivial pair
sample1 = MealyAutomaton( \
    [[1, 0, 1, 0], [0, 1, 0, 1]],
    [[1, 0, 3, 2], [3, 0, 1, 2]])

# generate group of order 1 494 186 269 970 473 680 896
sample2 = ([[0, 0, 0], [0, 2, 1], [1, 1, 1]],
           [[2, 1, 0], [2, 1, 0], [1, 2, 0]])

fantastique1 = ([[0, 1, 2], [1, 0, 3], [3, 2, 0], [2, 3, 1]],
                [[2, 0, 1], [2, 1, 0], [1, 2, 0], [0, 2, 1]])

fantastique2 = ([[1, 2, 3], [0, 3, 2], [3, 1, 0], [2, 0, 1]],
                [[1, 0, 2], [2, 0, 1], [1, 2, 0], [2, 1, 0]])

fantastique3 = ([[0, 1, 2], [1, 0, 3], [3, 2, 0], [2, 3, 1]],
                [[0, 2, 1], [1, 2, 0], [2, 0, 1], [2, 1, 0]])


def random_machine(nb_states, nb_letters):
    in_ret = [[random.randint(0, nb_states - 1)
               for i in range(nb_letters)] for j in range(nb_states)]
    out_ret = [[random.randint(0, nb_letters - 1)
                for i in range(nb_letters)] for j in range(nb_states)]
    return MealyAutomaton(in_ret, out_ret)


def random_permutation(n):
    lst = list(range(n))
    for i in range(n):
        j = random.randint(i, n - 1)
        lst[i], lst[j] = lst[j], lst[i]
    return lst


def random_inv(nb_states, nb_letters):
    in_ret = [[random.randint(0, nb_states - 1)
               for i in range(nb_letters)] for j in range(nb_states)]
    out_ret = [[None for i in range(nb_letters)] for j in range(nb_states)]
    for p in range(nb_states):
        rho = random_permutation(nb_letters)
        for x in range(nb_letters):
            out_ret[p][x] = rho[x]
    return MealyAutomaton(in_ret, out_ret)


def random_birev(nb_states, nb_letters):
    # compteur = 0
    while True:
        # print(compteur)
        # compteur += 1
        m = random_inv(nb_states, nb_letters)
        if mealy.bireversible(m):
            return m


import math
def dumb_factorization(m):
    for i in range(1, int(math.sqrt(m.nb_states))):
        if m.nb_states % i == 0:
            for j in range(100):
                a = random_machine(i, m.nb_letters)
                b = random_machine(m.nb_states // i, m.nb_letters)
                if product(a, b) == m: return a, b
    return None
