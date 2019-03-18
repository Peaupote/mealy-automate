"""Mealy Machine : md-réduction, dualisation, inversion, produit, factorisation..."""

import igraph
from graphviz import Digraph


class MealyMachine:
    """Machine de Mealy : dualisation, inversion, minimisation, md-réduction,
    test d'inversibilité, test de réversibilité"""

    def __init__(self, delta, rho, states=None, letters=None, name=None):
        self.delta = delta
        self.rho = rho
        self.states = states if states is not None else [
            str(i) for i in range(len(delta))]
        self.letters = letters if letters is not None else [
            str(i) for i in range(len(delta[0]))]
        self.name = name if name is not None else None
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
        """Renvoie l'automate dual si l'automate est dualisable, renvoie Faux sinon"""
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
        name_dual = self.name + "_dual" if self.name is not None else None
        return MealyMachine(delta, rho, list(self.letters), list(self.states), name_dual)

    def inverse(self):
        """Renvoie l'automate inverse si l'automate est inversible, renvoie Faux sinon"""
        new_delta = [[None for i in range(self.nb_letters)]
                     for j in range(self.nb_states)]
        new_rho = [[None for i in range(self.nb_letters)]
                   for j in range(self.nb_states)]
        for p in range(self.nb_states):
            for x in range(self.nb_letters):
                e, y = self.delta[p][x], self.rho[p][x]
                if new_rho[p][y] is not None:
                    return False
                new_delta[p][y] = e
                new_rho[p][y] = x
        new_states = [p + "*" for p in self.states]
        name_inverse = self.name + "_inverse" if self.name is not None else None
        return MealyMachine(new_delta, new_rho, new_states, list(self.letters), name_inverse)

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

    def __init_nerode_class(self):
        cl = [None for i in range(self.nb_states)]
        for p1 in range(self.nb_states):
            if cl[p1] is None:
                cl[p1] = p1
                for p2 in range(p1+1, self.nb_states):
                    if cl[p2] is None:
                        equivalent = True
                        for x in range(self.nb_letters):
                            if self.rho[p1][x] != self.rho[p2][x]:
                                equivalent = False
                        if equivalent:
                            cl[p2] = cl[p1]
        return cl

    def __next_nerode_class(self, cl):
        new_cl = [None for i in range(self.nb_states)]
        for p1 in range(self.nb_states):
            if new_cl[p1] is None:
                new_cl[p1] = p1
                for p2 in range(p1+1, self.nb_states):
                    if new_cl[p2] is None and cl[p1] == cl[p2]:
                        equivalent = True
                        for x in range(self.nb_letters):
                            if cl[self.delta[p1][x]] != cl[self.delta[p2][x]]:
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

        return MealyMachine(new_delta, new_rho, states, self.letters)

    def minimize(self):
        stop = False
        cl = self.__init_nerode_class()
        while not stop:
            new_cl = self.__next_nerode_class(cl)
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
        """Affiche l'automate"""
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
                    edges[key] = self.letters[x] + " | " + \
                        self.letters[self.rho[p][x]]
            for key in edges:
                graph.edge(self.states[p], key, label=edges[key])

        if destfile:
            graph.render('outputs/' + destfile, view=view)
        elif self.name is not None:
            graph.render('outputs/' + self.name, view=view)
        else:
            graph.render('outputs/default', view=view)

    def helix_graph(self):
        adj = {}
        for p in range(self.nb_states):
            for x in range(self.nb_letters):
                adj[p, x] = self.delta[p][x], self.rho[p][x]
        return adj

    def show_helix_graph(self, view=True, destfile=None):
        graph = Digraph(comment="Helix Graph")
        graph.attr(rankdir='LR')
        graph.attr('node', shape='circle')

        H = self.helix_graph()

        for i in H:
            p, x = i
            q, y = H[i]
            graph.node(self.states[p] + ", " + self.letters[x])
            graph.edge(self.states[p] + ", " + self.letters[x],
                       self.states[q] + ", " + self.letters[y])

        if destfile:
            graph.render('outputs/' + destfile, view=view)
        elif self.name is not None:
            graph.render('outputs/' + self.name + "_helix", view=view)
        else:
            graph.render('outputs/default', view=view)

    def automorphisms(self):
        # construction of helix graph using igraph
        H = igraph.Graph(directed=True)
        M = max(self.nb_states, self.nb_letters)
        S = self.nb_states * self.nb_letters
        ST = S + self.nb_states
        SL = ST + self.nb_letters
        H.add_vertices(SL + 3)

        labels = [None] * (SL + 3)
        labels[SL + 2] = "Idle"
        labels[SL + 1] = "Sigma"
        labels[SL] = "Q"

        H.add_edge(SL + 1, SL + 2)
        for x in range(self.nb_letters):
            H.add_edge(ST + x, SL + 1)
            labels[ST + x] = self.letters[x]
        for p in range(self.nb_states):
            H.add_edge(S + p, SL)
            labels[S + p] = self.states[p]
            for x in range(self.nb_letters):
                st = p * M + x
                labels[st] = self.states[p] + ", " + self.letters[x]
                H.add_edge(st, self.delta[p][x] * M + self.rho[p][x])
                H.add_edge(st, S + p)
                H.add_edge(st, ST + x)
        H.vs["label"] = labels

        Aut = H.get_automorphisms_vf2()
        # TODO: transform into nice output format
        # sympy PermutationGroup ?
        return Aut


def product(m1, m2):
    """Renvoie le produit des automates m1 et m2"""
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
    return MealyMachine(delta, rho, states, list(m1.letters))


def mass(m, n):
    current = m
    size = []
    for _ in range(n):
        current = current.minimize()
        size.append(current.nb_states)
        current = product(current, current)
    return size
