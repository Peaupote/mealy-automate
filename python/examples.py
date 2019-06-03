from mealy import MealyMachine
from generator import helix_gen
from random import randint, sample

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


def random_inv(nb_states, nb_letters):
    in_ret = [[randint(0, nb_states - 1)
               for i in range(nb_letters)] for j in range(nb_states)]
    out_ret = [[None for i in range(nb_letters)] for j in range(nb_states)]
    for p in range(nb_states):
        rho = sample(range(nb_letters), nb_letters)
        for x in range(nb_letters):
            out_ret[p][x] = rho[x]
    return MealyMachine(in_ret, out_ret)


def reduce_gen(nb_states, nb_letters):
    enum = helix_gen(nb_states, nb_letters)
    reduce_set = []
    for m in enum:
        mini = m.minimize()
        if mini not in reduce_set:
            # print("ok")
            reduce_set.append(mini)
    return list(reduce_set)
