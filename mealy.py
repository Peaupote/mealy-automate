from graphviz import Digraph

class MealyAutomaton:

    def __init__(self, delta, rho, states=None, letters=None):
        self.delta = delta
        self.rho = rho
        self.states = states if states != None else [str(i) for i in range(len(delta))]
        self.letters = letters if letters != None else [str(i) for i in range(len(delta[0]))]
        self.nb_states = len(self.states)
        self.nb_letters = len(self.letters)


    def __eq__(self, other):
        return other and\
            self.delta == other.delta and self.rho == other.rho

    def execute(self, entry, state):
        out = []
        for w in entry:
            out.append(self.rho[state][w])
            state = self.delta[state][w]
        return out


    def dual(self):
        delta = [[None for i in range(self.nb_states)]
                 for j in range(self.nb_letters)]
        rho = [[None for i in range(self.nb_states)]
               for j in range(self.nb_letters)]
        for x in range(self.nb_letters):
            S = [False] * self.nb_states
            for p in range(self.nb_states):
                q, y = self.delta[p][x], self.rho[p][x]
                if S[q]:
                    return False
                delta[x][p] = y
                rho[x][p] = q
                S[q] = True
        return MealyAutomaton(delta, rho, list(self.letters), list(self.states))


    def inverse(self):
        delta = list(self.delta)
        rho = [[None for i in range(self.nb_letters)]
               for j in range(self.nb_states)]
        for p in range(self.nb_states):
            for x in range(self.nb_letters):
                q, y = self.delta[p][x], self.rho[p][x]
                if rho[p][y] != None:
                    return False
                rho[p][y] = x
        states = [p + "**-1" for p in self.states]
        return MealyAutomaton(delta, rho, states, list(self.letters))


    def is_reversible(self):
        for x in range(self.nb_letters):
            out = [False] * self.nb_states
            for p in range(self.nb_states):
                if out[self.delta[p][x]]:
                    return False
                out[self.delta[p][x]] = True
        return True


    def bireversible(self):
        inv = self.inverse()
        if not inv:
            return False
        return self.is_reversible() and inv.is_reversible()


    def __init_nerode_class(self, rho):
        cl = [None for i in range(len(rho))]
        for p1 in range(len(rho)):
            if cl[p1] == None:
                cl[p1] = p1
                for p2 in range(p1+1, len(rho)):
                    if cl[p2] == None:
                        equivalent = True
                        for x in range(len(rho[0])):
                            if rho[p1][x] != rho[p2][x]:
                                equivalent = False
                        if equivalent:
                            cl[p2] = cl[p1]
        return cl


    def __next_nerode_class(self, delta, cl):
        new_cl = [None for i in range(len(delta))]
        for p1 in range(len(delta)):
            if new_cl[p1] == None:
                new_cl[p1] = p1
                for p2 in range(p1+1, len(delta)):
                    if new_cl[p2] == None and cl[p1] == cl[p2]:
                        equivalent = True
                        for x in range(len(delta[0])):
                            if cl[delta[p1][x]] != cl[delta[p2][x]]:
                                equivalent = False
                        if equivalent:
                            new_cl[p2] = new_cl[p1]
        return new_cl


    def __fusion(self, cl):
        new_delta, new_rho = [], []

        for p in range(len(self.delta)):
            if p == cl[p]:
                new_delta.append(list(self.delta[p]))
                new_rho.append(list(self.rho[p]))

        new_id = {}
        states = []
        compteur = 0
        for i in range(self.nb_states):
            if not cl[i] in new_id:
                new_id[cl[i]] = compteur
                states.append(self.states[i])
                compteur += 1
            else:
                states[new_id[cl[i]]] += self.states[i]

        for p in range(len(new_delta)):
            for x in range(len(new_delta[0])):
                new_delta[p][x] = new_id[cl[self.delta[p][x]]]

        return MealyAutomaton(new_delta, new_rho, states, self.letters)


    def minimize(self):
        stop = False
        cl = self.__init_nerode_class(self.rho)
        while not stop:
            new_cl = self.__next_nerode_class(self.delta, cl)
            if new_cl == cl:
                stop = True
            else:
                cl = new_cl
        return self.__fusion(cl)


    def md_reduce(self):
        prev, current = None, self
        while prev != current:
            prev, current = current, current.minimize()
            if current == prev:  # automaton is minimal
                prev = prev.dual()
                current = prev.minimize()
        return current


    def show(self, view=True, destfile=None):
        graph = Digraph(comment="Mealy Machine")
        graph.attr(rankdir='LR')

        for i in range(len(self.delta)):
            graph.node(self.states[i])

        graph.attr('node', shape='circle')

        for p in range(self.nb_states):
            edges = {}
            for x in range(self.nb_letters):
                key = self.states[self.delta[p][x]]
                if key in edges:
                    edges[key] = edges[key] + "\n" + \
                        self.letters[x] + " | " + self.letters[self.rho[p][x]]
                else:
                    edges[key] = self.letters[x] + " | " + self.letters[self.rho[p][x]]
            for key in edges:
                graph.edge(self.states[p], key, label=edges[key])

        if destfile:
            graph.render('outputs/' + destfile, view=view)
            if view:
                graph.view()
        else: graph.view()

def product(m1, m2):
    M = max(m1.nb_states, m2.nb_states)
    nb_states = m1.nb_states * m2.nb_states
    delta = [[None for i in range(m1.nb_letters)]
             for i in range(nb_states)]
    rho = [[None for i in range(m1.nb_letters)]
           for i in range(nb_states)]
    states = [None for i in range(nb_states)]

    for p in range(m1.nb_states):
        for x in range(m1.nb_letters):
            q, y = m1.delta[p][x], m1.rho[p][x]
            for r in range(m2.nb_states):
                delta[p * M + r][x] = q * M + m2.delta[r][y]
                rho[p * M + r][x] = m2.rho[r][y]
                states[p * M + r] = m1.states[p] + m2.states[r]
    return MealyAutomaton(delta, rho, states, list(m1.letters))


def mass(m, n):
    current = m
    size = []
    for i in range(n):
        current = current.minimize()
        size.append(current.nb_states)
        current = product(current, current)
    return size
