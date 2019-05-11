import generator
from mealy import *

NB_PRODUCT = 0

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


def is_there_none(tab_of_tab):
    for i in range(len(tab_of_tab)):
        for j in range(len(tab_of_tab[i])):
            if tab_of_tab[i][j] is None:
                return True
    return False


def __init(nb_states, nb_letters):
    sources = [(i, j) for i in range(nb_states) for j in range(nb_letters)]
    targets = [(i, j) for i in range(nb_states) for j in range(nb_letters)]
    delta = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    rho = [[None for _ in range(nb_letters)] for _ in range(nb_states)]
    return delta, rho, sources, targets


couples = []

def factor(m):
    for i in range(2, m.nb_states // 2 + 1):
        if m.nb_states % i == 0:
            print("Choose size", i)
            if factor_step1(m, i):
                print("NB_PRODUCT =", NB_PRODUCT)
                return True
    print("NB_PRODUCT =", NB_PRODUCT)
    return False


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
    vertices = [(i, j) for i in range(m.nb_states)
                for j in range(m.nb_letters)]
    labels = [(None, None)] * m.nb_states
    deltaA, rhoA, sourcesA, targetsA = __init(i, m.nb_letters)
    deltaB, rhoB, sourcesB, targetsB = __init(m.nb_states // i, m.nb_letters)
    p, x = vertices.pop()
    if factor_step2(m, vertices, deltaA, rhoA, sourcesA, targetsA,
                    deltaB, rhoB, sourcesB, targetsB, labels, p, x, 0):
        return True


def factor_step2(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, indent):
    print(indent, indent*" ", "factor_step2")
    q, y = m.delta[p][x], m.rho[p][x]
    i = 0
    while True:
        i = find(targetsB, i, labels[q][1], y)
        if i != None:
            res = factor_step3(m, vertices, deltaA, rhoA, sourcesA, targetsA,
                               deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i, indent)
            if res:
                return res
        if i == None:
            return False
        i += 1


def factor_step3(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, indent):
    print(indent, indent*" ", "factor_step3")
    i = 0
    while True:
        i = find(sourcesB, i, labels[p][1], None)
        if i != None:
            res = factor_step4(m, vertices, deltaA, rhoA, sourcesA, targetsA,
                               deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i, indent)
            if res:
                return res
        if i == None:
            return False
        i += 1


def factor_step4(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, indent):
    print(indent, indent*" ", "factor_step4")
    i = 0
    while True:
        i = find(targetsA, i, labels[q][0], sourcesB[i3][1])
        if i != None:
            if labels[q] == (None, None):
                tmp = (targetsA[i][0], targetsB[i2][0])
                if tmp in labels:
                    break
                labels[q] = tmp
                res = factor_step5(m, vertices, deltaA, rhoA, sourcesA, targetsA,
                                   deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, i, indent)
                if res:
                    return res
                labels[q] = (None, None)
            else:
                res = factor_step5(m, vertices, deltaA, rhoA, sourcesA, targetsA,
                                   deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, i, indent)
                if res:
                    return res
        if i == None:
            return False
        i += 1


def factor_step5(m, vertices, deltaA, rhoA, sourcesA, targetsA, deltaB, rhoB, sourcesB, targetsB, labels, p, x, q, y, i2, i3, i4, indent):
    print(indent, indent*" ", "factor_step5")
    global NB_PRODUCT
    print(indent, indent*"  ", "p", p, "x", x, "q", q, "y", y)
    print(indent, indent*"  ", "Reste :", len(vertices))
    print(indent, indent*"  ", "Label :", labels)
    print(indent, indent*" ", "({},{}) --> ({},{})  <~> ({},{} --> ({},{}))".format(labels[p][0], x, labels[q][0], targetsA[i3][1], labels[p][1], sourcesB[i3][1], labels[q][1], y))
    i = 0
    while True:
        i = find(sourcesA, i, labels[p][0], x)
        print(indent, indent*"  ", "new i", i)
        print(indent, indent*"  ", "sourcesA", sourcesA, "targetsA", targetsA)
        print(indent, indent*"  ", "sourcesB", sourcesB, "targetsB", targetsB)
        if i != None:
            dA = deltaA[sourcesA[i][0]][sourcesA[i][1]]
            rA = rhoA[sourcesA[i][0]][sourcesA[i][1]]

            dB = deltaB[sourcesB[i3][0]][sourcesB[i3][1]]
            rB = rhoB[sourcesB[i3][0]][sourcesB[i3][1]]
            if labels[p] == (None, None):
                tmp = (sourcesA[i][0], sourcesB[i3][0])
                if tmp in labels:
                    print("break label")
                    print(p, tmp)
                    i+=1
                    continue
                labels[p] = tmp
                deltaA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][0]
                rhoA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][1]

                deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][0]
                rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][1]
                print(indent, indent*"  ", "A1", deltaA, rhoA)
                print(indent, indent*"  ", "B1", deltaB, rhoB)

                if __valid_rho(rhoA) and __valid_delta(deltaA) and __valid_rho(rhoB) and __valid_delta(deltaB):
                    print(indent, indent*"  ", "Valide 1")
                    if len(sourcesA) == 1 and len(sourcesB) == 1:
                        mA = MealyMachine(deltaA, rhoA)
                        mB = MealyMachine(deltaB, rhoB)
                        NB_PRODUCT += 1
                        prod = product(mA, mB)
                        print(indent, indent*"  ", "produit",
                              prod.delta, prod.rho)
                        print(indent, indent*"  ", "m      ", m.delta, m.rho)
                        if prod == m:
                            return True
                        else:
                            deltaA[sourcesA[i][0]][sourcesA[i][1]] = dA
                            rhoA[sourcesA[i][0]][sourcesA[i][1]] = rA

                            deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = dB
                            rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = rB
                            i += 1
                            continue

                    newp, newx = vertices.pop()
                    sA = sourcesA.pop(i)
                    tA = targetsA.pop(i4)
                    sB = sourcesB.pop(i3)
                    tB = targetsB.pop(i2)
                    res = factor_step2(m, vertices, deltaA, rhoA, sourcesA,
                                       targetsA, deltaB, rhoB, sourcesB, targetsB, labels, newp, newx, indent+1)
                    if res:
                        return res
                    vertices.append((newp, newx))
                    sourcesA.insert(i, sA)
                    targetsA.insert(i4, tA)

                    sourcesB.insert(i3, sB)
                    targetsB.insert(i2, tB)
                labels[p] = (None, None)
            else:
                # print(indent, "sourcesA[i][0]", sourcesA[i][0], "sourcesA[i][1]", sourcesA[i][1], "targetsA[i4][0]", targetsA[i4][0])

                # print(indent, indent*"  ", "i", i, "i4", i4)
                print(indent, indent*"  ", "A avant :", deltaA, rhoA)
                print(indent, indent*"  ", "B avant :", deltaB, rhoB)

                deltaA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][0]
                rhoA[sourcesA[i][0]][sourcesA[i][1]] = targetsA[i4][1]

                deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][0]
                rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = targetsB[i2][1]

                print(indent, indent*"  ", "A après :", deltaA, rhoA)
                print(indent, indent*"  ", "B après :", deltaB, rhoB)

                if __valid_rho(rhoA) and __valid_delta(deltaA) and __valid_rho(rhoB) and __valid_delta(deltaB):
                    print(indent, indent*"  ", "Valide 2")
                    if len(sourcesA) == 1 and len(sourcesB) == 1:
                        mA = MealyMachine(deltaA, rhoA)
                        mB = MealyMachine(deltaB, rhoB)
                        NB_PRODUCT += 1                        prod = product(mA, mB)
                        print(indent, indent*"  ", "produit",
                              prod.delta, prod.rho)
                        print(indent, indent*"  ", "m      ", m.delta, m.rho)
                        if prod == m:
                            return True
                        else:
                            deltaA[sourcesA[i][0]][sourcesA[i][1]] = dA
                            rhoA[sourcesA[i][0]][sourcesA[i][1]] = rA

                            deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = dB
                            rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = rB
                            i += 1
                            continue
                    newp, newx = vertices.pop()
                    sA = sourcesA.pop(i)
                    tA = targetsA.pop(i4)
                    sB = sourcesB.pop(i3)
                    tB = targetsB.pop(i2)
                    res = factor_step2(m, vertices, deltaA, rhoA, sourcesA,
                                       targetsA, deltaB, rhoB, sourcesB, targetsB, labels, newp, newx, indent+1)
                    if res:
                        return res
                    vertices.append((newp, newx))
                    sourcesA.insert(i, sA)
                    targetsA.insert(i4, tA)

                    sourcesB.insert(i3, sB)
                    targetsB.insert(i2, tB)
                else:
                    print(indent, indent*"  ", "Non Valide 2")
            deltaA[sourcesA[i][0]][sourcesA[i][1]] = dA
            rhoA[sourcesA[i][0]][sourcesA[i][1]] = rA

            deltaB[sourcesB[i3][0]][sourcesB[i3][1]] = dB
            rhoB[sourcesB[i3][0]][sourcesB[i3][1]] = rB
        else: #None
            return False
        i += 1


M1 = generator.helix(2, 2)
M2 = generator.helix(2, 2)
prod = product(M1, M2)
while not prod.bireversible():
    M1 = generator.helix(2, 2)
    M2 = generator.helix(2, 2)
    prod = product(M1, M2)
print(factor(prod))
