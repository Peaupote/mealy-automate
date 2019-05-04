from mealy import *

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
    sources = [(i, j) for i in range(nb_states) for j in range(nb_letters)]
    targets = [(i, j) for i in range(nb_states) for j in range(nb_letters)]
    delta = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    rho = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    return delta, rho, sources, targets


def factor(m):
    for i in range(1, m.nb_states // 2):
        if m.nb_states % i == 0:
            print("Choose size", i)
            factor_step1(m, i)

def find(tab, i, state, letter):
    for j in range(i, len(tab)):
        if state != None and tab[j][0] == state:
            return j
        if letter != None and tab[j][1] == letter:
            return j
        if state == None and letter == None:
            return j
    return None


def factor_step1(m, i):
    vertices = [(i, j) for i in range(m.nb_states) for j in range(m.nb_letters)]
    labels = [(None, None)] * m.nb_states
    deltaA, rhoA, sourcesA, targetsA = __init(i, m.nb_letters)
    deltaB, rhoB, sourcesB, targetsB = __init(m.nb_states // i, m.nb_letters)
    p, x = vertices.pop()
    factor_step2(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x)

def factor_step2(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x):
    q, y = m.delta[p][x], m.rho[p][x]
    i = 0
    while True:
        i = find(targetsB, i, labels[q][1], y)
        if i != None:
            res = factor_step3(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i)
            if res: return res
        if i == None:
            return False
        i += 1

def factor_step3(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2):
    i = 0
    while True:
        i = find(sourcesB, i, labels[p][1], None)
        if i != None:
            res = factor_step4(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i)
            if res: return res
        if i == None:
            return False
        i += 1

def factor_step4(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3):
    i = 0
    while True:
        i = find(targetsA, i, labels[q][0], sourcesB[i3][1])
        if i != None:
            if labels[q] == (None, None):
                tmp = (targetsA[i][0], targetsB[i2][0])
                if tmp in labels:
                    break
                labels[q] = tmp
                res = factor_step5(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, i)
                if res: return res
                labels[q] = (None, None)
            else:
                res = factor_step5(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, i)
                if res: return res
        if i == None:
            return False
        i += 1

def factor_step5(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, i4):
    i = 0
    while True:
        i = find(sourcesA, i, labels[p][0], x)
        if i != None:
            if labels[p] == (None, None):
                tmp = (sourcesA[i][0], targetsB[i3][0])
                if tmp in labels:
                    break
                labels[p] = tmp
                deltaA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][0]
                rhoA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][1]

                deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][0]
                rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][1]
                print(deltaA, rhoA)
                print(deltaB, rhoB)

                if __valid_rho(rhoA) and __valid_delta(deltaA) and __valid_rho(rhoB) and __valid_delta(deltaB):
                    if not vertices:
                        mA = MealyMachine(deltaA, rhoA)
                        mB = MealyMachine(deltaB, rhoB)
                        if product(mA, mB) == m:
                            return True
                        else:
                            i += 1
                            deltaA[sourcesA[i][0]][sourcesA[i][1]] = None
                            rhoA[sourcesA[i][0]][sourcesA[i][1]] = None

                            deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = None
                            rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = None
                            continue
                    p, x = vertices.pop()
                    res = factor_step2(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x)
                    if res: return res
                    vertices.append((p, x))
                labels[p] = (None, None)
            else:
                deltaA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][0]
                rhoA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][1]

                deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][0]
                rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][1]
                print("A :", deltaA, rhoA)
                print("B :", deltaB, rhoB)

                if __valid_rho(rhoA) and __valid_delta(deltaA) and __valid_rho(rhoB) and __valid_delta(deltaB):
                    if not vertices:
                        mA = MealyMachine(deltaA, rhoA)
                        mB = MealyMachine(deltaB, rhoB)
                        if product(mA, mB) == m:
                            return True
                        else:
                            i += 1
                            deltaA[sourcesA[i][0]][sourcesA[i][1]] = None
                            rhoA[sourcesA[i][0]][sourcesA[i][1]] = None

                            deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = None
                            rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = None
                            continue
                    p, x = vertices.pop()
                    res = factor_step2(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x)
                    if res: return res
                    vertices.append((p, x))
            deltaA[sourcesA[i][0]][sourcesA[i][1]] = None
            rhoA[sourcesA[i][0]][sourcesA[i][1]] = None

            deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = None
            rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = None
        if i == None:
            return False
        i += 1


import generator
M1 = generator.helix(2, 2)
M2 = generator.helix(2, 2)
print(factor(product(M1, M2)))
