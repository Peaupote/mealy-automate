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

birev33_1 = MealyMachine([[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                         [[0, 2, 1], [1, 2, 0], [1, 2, 0]],
                         ['a', 'b', 'c'], name="birev33_1")


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


def helix_birev(nb_states, nb_letters):
    size = nb_states*nb_letters
    cycles = []
    c = 0
    while c < size:
        s = randint(0, size-c)
        cycles.append([None for _ in range(s)])
        c += s
    check_letters = [[(p, i) for i in range(nb_letters)]
                     for p in range(nb_states)]
    check_states = {i: [p for p in range(nb_states)]
                    for i in range(nb_letters)}
    for C in cycles:
        for i in range(len(C)):
            state = None
            letter = None
            while state is None or letter is None:
                s = randint(0, len(check_letters) - 1)
                state, letter = check_letters[s][randint(
                    0, len(check_letters[s]) - 1)]
                if not check_states[letter] or not state in check_states[letter]:
                    state, letter = None, None
                else:
                    check_letters[s].remove((state, letter))
                    if not check_letters[s]:
                        del check_letters[s]
                    check_states[letter].remove(state)
            C[i] = (state, letter)

    delta = [[None for i in range(nb_letters)]
             for j in range(nb_states)]
    rho = [[None for i in range(nb_letters)]
           for j in range(nb_states)]
    for C in cycles:
        for i in range(0, len(C)):
            prev_state, prev_letter = C[i-1]
            state, letter = C[i]
            delta[prev_state][prev_letter] = state
            rho[prev_state][prev_letter] = letter
    # print(cycles)
    return MealyMachine(delta, rho)


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

for i in range(len(birev33)):
    birev33[i].name = "birev33_" + str(i)
