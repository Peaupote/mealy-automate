from mealy import MealyMachine
from examples import count_cycle_size
from random import randint, sample, shuffle
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
    res = rec(None, None, list(vertices), list(targets),
              deepcopy(delta), deepcopy(rho))
    return MealyMachine(*res)


def rec(start, prev, sources, targets, delta, rho):
    if not sources and not targets:
        return delta, rho

    if not prev:
        start = sources.pop()
        prev = start

    p_start, x_start = start
    p_prev, x_prev = prev

    for _ in range(len(targets)):
        p_next, x_next = targets.pop(0)
        delta[p_prev][x_prev] = p_next
        rho[p_prev][x_prev] = x_next
        if not p_next == p_start or not x_next == x_start:
            sources.remove((p_next, x_next))
            if __valid_delta(delta) and __valid_rho(rho):
                res = rec(start, (p_next, x_next), list(sources),
                          list(targets), deepcopy(delta), deepcopy(rho))
                if res:
                    return res
            sources.append((p_next, x_next))
        else:
            if __valid_delta(delta) and __valid_rho(rho):
                res = rec(None, None, list(sources),
                          list(targets), deepcopy(delta), deepcopy(rho))
                if res:
                    return res
        delta[p_prev][x_prev] = None
        rho[p_prev][x_prev] = None
        targets.append((p_next, x_next))

    return False


def __random_cycles(size):
    cycles = []
    c = 0
    while c < size:
        s = randint(1, size - c)
        cycles.append(s)
        c += s
    return cycles


def helix_cycles(nb_states, nb_letters):
    vertices, delta, rho = __init(nb_states, nb_letters)
    size = nb_states*nb_letters
    while True:
        cycles = __random_cycles(size)
        shuffle(vertices)
        res = rec_cycles(None, None, list(cycles), list(vertices),
                         deepcopy(delta), deepcopy(rho))
        if res:
            return MealyMachine(*res)
    return False


def rec_cycles(start, prev, cycles, vertices, delta, rho):
    if cycles[0] == 0:
        p_prev, x_prev = prev
        p_start, x_start = start
        delta[p_prev][x_prev] = p_start
        rho[p_prev][x_prev] = x_start
        if not __valid_delta(delta) or not __valid_rho(rho):
            return False
        cycles.pop(0)
        start = None
        prev = None
        if not cycles:
            return delta, rho
    size = len(vertices)

    for _ in range(size):
        v = vertices.pop(0)
        p, x = v
        if prev:
            p_prev, x_prev = prev
            delta[p_prev][x_prev] = p
            rho[p_prev][x_prev] = x
        cycles[0] -= 1
        if __valid_delta(delta) and __valid_rho(rho):
            res = rec_cycles(v if start is None else start, v, list(cycles), list(vertices), deepcopy(
                delta), deepcopy(rho))
            if res:
                return res
        cycles[0] += 1
        vertices.append(v)
        if prev:
            p_prev, x_prev = prev
            delta[p_prev][x_prev] = None
            rho[p_prev][x_prev] = None
    return False


def helix_gen(nb_states, nb_letters):
    vertices, delta, rho = __init(nb_states, nb_letters)
    targets = sample(vertices, len(vertices))
    enum = []
    rec_gen(None, None, list(vertices), list(targets),
            deepcopy(delta), deepcopy(rho), enum)
    return enum


REC = 0


def rec_gen(start, prev, sources, targets, delta, rho, enum):
    global REC

    if not sources and not targets:
        REC += 1
        print(REC)
        enum.append(MealyMachine(delta, rho))
        return

    if not prev:
        start = sources.pop()
        prev = start

    p_start, x_start = start
    p_prev, x_prev = prev

    for _ in range(len(targets)):
        p_next, x_next = targets.pop(0)
        delta[p_prev][x_prev] = p_next
        rho[p_prev][x_prev] = x_next
        if not p_next == p_start or not x_next == x_start:
            sources.remove((p_next, x_next))
            if __valid_delta(delta) and __valid_rho(rho):
                rec_gen(start, (p_next, x_next), list(sources),
                        list(targets), deepcopy(delta), deepcopy(rho), enum)
            sources.append((p_next, x_next))
        else:
            if __valid_delta(delta) and __valid_rho(rho):
                rec_gen(None, None, list(sources),
                        list(targets), deepcopy(delta), deepcopy(rho), enum)
        delta[p_prev][x_prev] = None
        rho[p_prev][x_prev] = None
        targets.append((p_next, x_next))
