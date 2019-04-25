#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "utils.h"

mealy_t *mealy(uint nb_states, uint nb_letters) {
    mealy_t *machine = malloc(sizeof(mealy_t*));
    if (machine) {
        machine->nb_states = nb_states;
        machine->nb_letters = nb_letters;
        machine->delta = calloc(nb_states * nb_letters, 1);
        if (!machine->delta) {
            free(machine);
            return 0;
        }

        machine->rho = calloc(nb_states * nb_letters, 1);
        if (!machine->rho) {
            free(machine->delta);
            free(machine);
            return 0;
        }
    }

    return machine;
}

char mealy_eq(mealy_t *m1, mealy_t *m2) {
    if (!m1 || !m2) return 0;
    if (m1->nb_letters != m2->nb_letters || m1->nb_states != m2->nb_states)
        return 0;

    unsigned int size = m1->nb_states * m1->nb_letters;
    return memcmp(m1->delta, m2->delta, size) == 0
        && memcmp(m1->rho, m2->rho, size) == 0;
}

void free_mealy(mealy_t *m) {
    free(m->delta);
    free(m->rho);
    free(m);
}

mealy_t *dual(mealy_t *m) {
    unsigned int x, p, i1, i2;
    mealy_t *d = mealy(m->nb_letters, m->nb_states);
    if (!d) return 0;

    for (p = 0; p < m->nb_states; p++) {
        for (x = 0; x < m->nb_letters; x++) {
            i1 = p * m->nb_letters + x;
            i2 = x * m->nb_states + p;
            d->delta[i2] = m->rho[i1];
            d->rho[i2] = m->delta[i1];
        }
    }

    return d;
}

mealy_t *min(mealy_t *m) {
    u_int8_t i, j, k, count;
    u_int8_t *part = malloc(m->nb_states),
        *part2 = malloc(m->nb_states);

    if (!part || !part2) return 0;

    for (i = 0; i < m->nb_states; i++) {
        for (j = 0; j < i; j++) {
            for (k = 0; k < m->nb_letters; k++) {
                if (m->rho[j * m->nb_letters + k] != m->rho[i * m->nb_letters + k])
                    break;
            }

            if (k == m->nb_letters)
                break;
        }

        part[i] = j;
    }

    while (1) {
        count = 0;

        for (i = 0; i < m->nb_states; i++) {
            for (j = 0; j < i; j++) {
                for (k = 0; part[i] == part[j] && k < m->nb_letters; k++) {
                    if (m->delta[i * m->nb_letters + k] != m->delta[j * m->nb_letters + k])
                        break;
                }

                if (k == m->nb_letters)
                    break;
            }

            if (j == i)
                count++;

            part2[i] = j;
        }

        if (memcmp(part2, part, m->nb_states) == 0)
            break;

        memcpy(part, part2, m->nb_states);
        memset(part2, 0, m->nb_states); //useless
    }

    mealy_t *min = mealy(count, m->nb_letters);
    if (!min) return 0;

    for (i = 0; i < count; i++) {
        for (j = 0; j < m->nb_states; j++)
            if (part[j] == i) break;

        for (k = 0; k < m->nb_letters; k++) {
            min->delta[i * m->nb_letters + k] = part[m->delta[j] * m->nb_letters + k];
            min->rho[i * m->nb_letters + k] = m->rho[j * m->nb_letters + k];
        }
    }

    free(part);
    free(part2);

    return min;
}

// can be improved
mealy_t *md_reduce(mealy_t *a) {
    mealy_t *b = 0, *c;

    while (!mealy_eq(a, b)) {
        b = a;
        a = min(a);
        if (mealy_eq(a, b)) {
            c = b;
            b = dual(b);
            free_mealy(c);
            c = a;
            a = min(b);
            free_mealy(a);
        }
    }

    return a;
}

mealy_t *product(mealy_t *m1, mealy_t *m2) {
    unsigned int nbl = m1->nb_letters,
        nbs = m1->nb_letters * m2->nb_states,
        p, x, r, q, y, i;

    mealy_t *prod = mealy(nbs, nbl);
    if (!p) return 0;

    for (p = 0; p < m1->nb_states; p++) {
        for (x = 0; x < m2->nb_letters; x++) {
            i = p * m1->nb_letters + x;
            q = m1->delta[i];
            y = m1->rho[i];
            for (r = 0; r < m2->nb_states; r++) {
                i = p * m2->nb_states + r;
                prod->delta[i * prod->nb_letters + x] = q * m2->nb_states
                    + m2->delta[r * m2->nb_letters + y];
                prod->rho[i * prod->nb_letters + x] = m2->rho[r * m2->nb_states + y];
            }
        }
    }

    return prod;
}

unsigned int mexp(mealy_t *m, unsigned int bound) {
    unsigned int i;
    mealy_t *tmp, *prev;

    tmp = m;
    m = min(m);
    free_mealy(m);

    for (i = 0; i < bound && !mealy_eq(prev, m); i++) {
        prev = m;
        tmp = product(m, m);
        m = min(tmp);
        free_mealy(tmp);
    }

    return i;
}
