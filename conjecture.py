#!/usr/bin/python

import mealy
import factor
import generator
import sys
import time
import os

import matplotlib.pyplot as plt


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
                                     mealy.mass(a, exp)[-1])

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
        # if mdc:
        #     countmdc += 1
        # if mdc and not md:
        #     t.add(m)
        # if not mdc and not md:
        #     countelse += 1

    i += 1
    print("Total count {}.".format(i))
    print("Done analyzing.")
    print("Results:")
    print("Md-trivial       {:>10} / {:>10}".format(countmd, i))
    print("Mdc-trivial      {:>10} / {:>10}".format(countmdc, i))
    print("Mdc but not md   {:>10} / {:>10}".format(len(t), i))
    print("Not trivial      {:>10} / {:>10}".format(countelse, i))

n = 4
size = 1500

def conjecture_mass(fname):
    #if len(sys.argv) < 2:
    #    print("usage: {} fname".format(sys.argv[0]), file=sys.stderr)
    #    sys.exit(1)

    x = list(range(1, n+1))
    out = open(fname + ".out", "wb")

    for i, m in enumerate(read_canonics(fname)):
        if i % 100 == 0:
            print("Machine", i)

        info = 1 if m.is_md_trivial() else 0
        out.write(y.to_bytes(1, byteorder='little'))

        for y in mealy.mass(m, n):
            out.write(y.to_bytes(4, byteorder='little'))

    out.close()


def split_file(fname, nb):
    f = open(fname, "rb")
    frags = []

    nb_states = int.from_bytes(f.read(1), byteorder='little')
    nb_letters = int.from_bytes(f.read(1), byteorder='little')
    print("states", nb_states)
    print("letters", nb_letters)

    while True:
        machines = f.read(nb_states * nb_letters * 2 * nb)
        if not machines:
            f.close()
            return frags

        frag_name = "/tmp/mealy_fragment" + str(time.time())
        frag = open(frag_name, "wb")
        frag.write(bytes([nb_states, nb_letters]))
        frag.write(machines)
        frag.close()

        frags.append(frag_name)

def main():
    print("n", n)
    print("frag size", size)

    frags = split_file(sys.argv[1], size)
    print(len(frags))

    max_fork = 4
    fork_count = 0
    outs = []

    for fname in frags:
        if fork_count >= max_fork:
            os.wait()

        if os.fork() == 0:
            conjecture_mass(fname)
            os.remove(fname)
            sys.exit(0)
        else:
            fork_count += 1

    for i in range(max_fork):
        os.wait()

    print("All done")
    print("Reassemble files")

    out = open(sys.argv[1] + ".out", "wb")
    out.write(n.to_bytes(1, byteorder='little'))

    for fname in frags:
        fragout = open(fname + ".out", "rb")
        while True:
            buf = fragout.read(4 * n + 1)
            if not buf:
                fragout.close()
                break

            out.write(buf)

        os.remove(fname + ".out")
    out.close()

if __name__ == "__main__":
    #conjecture()
    # main()

    i = 0
    for _ in read_canonics(sys.argv[1]):
        i += 1

    print(i)
