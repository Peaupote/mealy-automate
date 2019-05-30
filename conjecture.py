#!/usr/bin/python

import mealy
import factor
import generator
import sys, time, threading

import matplotlib.pyplot as plt

class SomeThread(threading.Thread):

    def __init__(self, i, f):
        threading.Thread.__init__(self)
        self.i = i
        self.count = 0
        self.action = f

    def run(self):
        while True:
            self.count += 1
            print(self.i, "Start", self.count)

            a = read_canonics(sys.argv[0])
            if not a:
                return

            self.action(a)


def mdc_reduce(machine):
    stack = [machine]

    while stack:
        m = stack.pop()
        if m.is_trivial():
            return True

        m = m.md_reduce()

        fs = factor.factor(m)
        if not fs:
            m = m.dual()
            if m.is_trivial():
                return True
            fs = factor.factor(m)
            if not fs:
                continue

        for a, b in fs:
            c = mealy.product(b, a)
            d = c.md_reduce()
            if d.is_trivial() or d.dual().is_trivial():
                return True
            if d != c and d.dual() != c:
                stack.append(d)
    return False


def read_canonics(fname):
    f = open(fname, "rb")
    nb_states = int.from_bytes(f.read(1), byteorder='little')
    nb_letters = int.from_bytes(f.read(1), byteorder='little')
    # print("Nb states", nb_states)
    # print("Nb letters", nb_letters)

    size = nb_states * nb_letters
    delta = [[None for _ in range(nb_letters)]
             for _ in range(nb_states)]
    rho = [[None for _ in range(nb_letters)]
           for _ in range(nb_states)]

    count = 0
    while True:
        buf = list(f.read(size * 2))
        if not buf:
            f.close()
            return

        for p in range(nb_states):
            for x in range(nb_letters):
                delta[p][x] = buf[p * nb_letters + x]
                rho[p][x] = buf[p * nb_letters + x + size]

        yield mealy.MealyMachine(delta, rho)

def in_iso(a, res):
    for b in res:
        if a.isomorphic(b):
            return True
    return False

def conjecturebis():
    if len(sys.argv) < 4:
        print("usage: {} fileA fileB fileAB".format(sys.argv[0]))
        sys.exit(1)

    max_nb_states_mass = 0
    exp = 5
    tot = 0
    res = set()
    for a in read_canonics(sys.argv[1]):
        for b in read_canonics(sys.argv[2]):
            tot += 1
            print("Machine", tot, end='\r')
            if (not mealy.product(a, b).is_md_trivial()
                and mealy.product(b, a).is_md_trivial()):
                m = mealy.product(a, b)
                max_nb_states_mass = max(max_nb_states_mass,
                                         mealy.mass(m, exp)[-1])
                res.add(m)

    print("Total factorisable count {}.".format(tot))
    print("AB not md-trivial and BA md-trivial {}".format(len(res)))

    for i, a in enumerate(read_canonics(sys.argv[3])):
        print("Machine", i, end='\r')
        if a.is_md_trivial():
            max_nb_states_mass = max(max_nb_states_mass,
                                     mealy.mass(a, exp)[-1] )

    count_not_finite = 0
    for i, a in enumerate(read_canonics(sys.argv[3])):
        print("Machine", i, end='\r')
        if (not a.is_md_trivial()
            and not in_iso(a, res)
            and mealy.mass_decide(a, max_nb_states_mass)):
            count_not_finite += 1

    print("Not md-trivial neither mdc-trivial {}.".format(count_not_finite))
    return res


def conjecture():
    if len(sys.argv) < 2:
        print("usage: {} file".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    t = set()

    countmd = 0
    countmdc = 0
    countelse = 0
    for i, m in enumerate(read_canonics(sys.argv[1])):
        print("Machine", i, end='\r')

        md = m.is_md_trivial()
        mdc = mdc_reduce(m)
        if md:
            countmd += 1
        if mdc:
            countmdc += 1
        if mdc and not md:
            t.add(m)
        if not mdc and not md:
            countelse += 1

    i += 1
    print("Total count {}.".format(i))
    print("Done analyzing.")
    print("Results:")
    print("Md-trivial       {:>10} / {:>10}".format(countmd, i))
    print("Mdc-trivial      {:>10} / {:>10}".format(countmdc, i))
    print("Mdc but not md   {:>10} / {:>10}".format(len(t), i))
    print("Not trivial      {:>10} / {:>10}".format(countelse, i))


def conjecture_mass():
    if len(sys.argv) < 2:
        print("usage: {} fname".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    n = 4
    x = list(range(1, n+1))

    plt.figure(1)

    for i, m in enumerate(read_canonics(sys.argv[1])):
        print("Machine", i, end='\r')
        y = mealy.mass(m, n)
        if m.is_md_trivial():
            plt.subplot(1, 2, 1)
        else:
            plt.subplot(1, 2, 2)
        plt.plot(x, y, '-o')

    print("done.")
    plt.subplot(1, 2, 1)
    plt.title("Mass md-trivials")

    plt.subplot(1, 2, 2)
    plt.title("Mass md-not-trivials")

    plt.show()

def truc(m):
    print(m)

if __name__ == "__main__":
    for i in range(4):
        SomeThread(i, truc).start()
