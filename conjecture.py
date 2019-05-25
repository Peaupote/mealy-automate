import mealy
import factor
import generator

# this probqbly dont work
def mdc_reduce(machine):
    stack = [machine]

    while stack:
        m = stack.pop()
        if m.is_trivial():
            return True

        m = m.md_reduce()
#        print(m.nb_states, m.nb_letters)

        fs = factor.factor(m)
        if not fs:
            m = m.dual()
#            print("dual", m.nb_states, m.nb_letters)
            if m.is_trivial():
                return True
            fs = factor.factor(m)
            if not fs:
                continue

#        print("facto nb", len(fs))
        for a, b in fs:
            c = mealy.product(b, a)
            d = c.md_reduce()
            if d.is_trivial():
                return True
            if d != c and d.dual() != c:
                stack.append(d)
    return False

def read_canonics(fname):
    f = open(fname, "rb")
    nb_states = int.from_bytes(f.read(1), byteorder='little')
    nb_letters = int.from_bytes(f.read(1), byteorder='little')
    size = nb_states * nb_letters
    can = []

    delta = [[None for _ in range(nb_letters)]
             for _ in range(nb_states)]

    rho = [[None for _ in range(nb_letters)]
           for _ in range(nb_states)]

    count = 0
    while True:
        d = list(f.read(size))
        if not d:
            f.close()
            return can
        r = list(f.read(size))

        for p in range(nb_states):
            for x in range(nb_letters):
                delta[p][x] = d[p * nb_letters + x]
                rho[p][x] = r[p * nb_letters + x]

        can.append(mealy.MealyMachine(delta, rho))
        count += 1
        print("count", count)

if __name__ == "__main__":
    cans = read_canonics("file")

    t = set()
    countmd = 0
    countmdc = 0
    for i, m in enumerate(cans):
        print("{:10}".format(i), "/", len(cans))
        md = m.is_md_trivial()
        mdc = mdc_reduce(m)
        if md:
            countmd += 1
        if mdc:
            countmdc += 1
        if mdc and not md:
            t.add(m)

    print("Md-trivial", countmd, "/", len(cans))
    print("Mdc-trivial", countmdc, "/", len(cans))
    print("Result", len(t), "/", len(cans))
