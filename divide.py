import itertools

def divide_right(m, r):
    couples = [(x, y)
               for x in range(m.nb_states // r.nb_states)
               for y in range(r.nb_states)]
    for p in itertools.permutation(m.nb_states):
        label = [couples[p[i]] for i in range(m.nb_states)]
