import random
import mealy

basilica = ([[1, 2], [0, 2], [2, 2], [4, 2], [2, 3], [6, 2], [2, 5]],
            [[0, 1], [1, 0], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0]])

grigorchuk = ([[4, 4], [0, 2], [0, 3], [4, 1], [4, 4]],
              [[1, 0], [0, 1], [0, 1], [0, 1], [0, 1]])

# md reduce to trivial pair
sample1 = ([[1, 0, 1, 0], [0, 1, 0, 1]],
           [[1, 0, 3, 2], [3, 0, 1, 2]])

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
    return in_ret, out_ret


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
    return in_ret, out_ret


def random_birev(nb_states, nb_letters):
    # compteur = 0
    while True:
        # print(compteur)
        # compteur += 1
        m = random_inv(nb_states, nb_letters)
        if mealy.bireversible(m):
            return m
