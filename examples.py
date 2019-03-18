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


def random_cycles(size):
    cycles = []
    c = 0
    while c < size:
        s = randint(0, size-c)
        # s = size
        cycles.append([None for _ in range(s)])
        c += s
    return [[None for _ in range(size)]]


def helix_birev(nb_states, nb_letters):
    cycles = random_cycles(nb_states*nb_letters)
    check_curr_letters = [random_permutation(nb_letters)
                          for p in range(nb_states)]
    check_next_letters = [random_permutation(nb_letters)
                          for p in range(nb_states)]
    check_states = [random_permutation(nb_states)
                    for p in range(nb_letters)]
    available_states = list(range(nb_states))

    for C in cycles:
        for i in range(len(C)):
            state = None
            letter = None
            previous_letter = None
            previous_state = None
            while state is None or letter is None:
                if previous_letter is not None:
                    state = check_states[previous_letter][0]
                    letter = check_next_letters[previous_state][0]
                    check_curr_letters[state].remove(state)
                    check_next_letters[previous_state].remove(letter)
                    if not check_next_letters[previous_state]:
                        available_states.remove(previous_state)
                    if not check_curr_letters[state]:
                        available_states.remove(state)
                    check_states[previous_letter].remove(state)
                else:
                    state = available_states[randint(
                        0, len(available_states) - 1)]
                    letter = check_curr_letters[state][0]
                    check_curr_letters[state].remove(letter)
                    if not check_curr_letters[state]:
                        available_states.remove(state)
                previous_state = state
                previous_letter = letter
            C[i] = (state, letter)

    # print(cycles)

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
