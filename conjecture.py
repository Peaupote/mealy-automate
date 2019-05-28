#!/usr/bin/python

import mealy
import factor
import generator
import sys


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


def conjecturebis(file1, file2):
    if len(sys.argv) < 3:
        print("usage: {} file1 file2".format(sys.argv[0]))
        sys.exit(1)

    tot = 0
    res = set()
    for a in read_canonics(file1):
        for b in read_canonics(file2):
            tot += 1
            print("Machine", tot, end='\r')
            if (not mealy.product(a, b).is_md_trivial()
                and mealy.product(b, a).is_md_trivial()):
                res.add(mealy.product(a, b))

    print("Total factorisable count {}.".format(tot))
    print("AB not md-trivial and BA md-trivial {}".format(len(res)))
    return res


def conjecture(fname):
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


if __name__ == "__main__":
    res = conjecturebis(sys.argv[1], sys.argv[2])
