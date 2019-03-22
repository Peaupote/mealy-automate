from mealy import MealyMachine
from random import sample, shuffle
from copy import deepcopy


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


def __init(nb_states, nb_letters):
    vertices = []
    for p in range(nb_states):
        for x in range(nb_letters):
            vertices.append((p, x))
    shuffle(vertices)
    delta = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    rho = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    return vertices, delta, rho


def helix(nb_states, nb_letters):
    vertices, delta, rho = __init(nb_states, nb_letters)
    targets = sample(vertices, len(vertices))
    res = rec(list(vertices), list(targets),
              list(delta), list(rho))
    return MealyMachine(*res)


def rec(sources, targets, delta, rho):
    if not sources and not targets:
        return delta, rho

    for _ in range(len(sources)):
        (p, x) = sources.pop(0)
        for _ in range(len(targets)):
            (q, y) = targets.pop(0)
            delta[p][x] = q
            rho[p][x] = y
            if __valid_delta(delta) and __valid_rho(rho):
                res = rec(list(sources), list(targets),
                          deepcopy(delta), deepcopy(rho))
                if res:
                    return res
            delta[p][x] = None
            rho[p][x] = None
            targets.append((q, y))
        sources.append((p, x))
    return False
