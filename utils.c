#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "utils.h"

mealy_t *mealy(unsigned int nb_states, unsigned int nb_letters) {
    mealy_t *machine = malloc(sizeof(mealy_t));
    if (machine) {
        machine->nb_states = nb_states;
        machine->nb_letters = nb_letters;
        machine->delta = malloc(nb_states * nb_letters * sizeof(unsigned int));
        if (!machine->delta) {
            free(machine);
            return 0;
        }

        machine->rho = malloc(nb_states * nb_letters * sizeof(unsigned int));
        if (!machine->rho) {
            free(machine->delta);
            free(machine);
            return 0;
        }
    }

    return machine;
}

char mealy_eq(const mealy_t *m1, const mealy_t *m2) {
    if (!m1 || !m2) return 0;
    if (m1->nb_letters != m2->nb_letters || m1->nb_states != m2->nb_states)
        return 0;

    unsigned int size = m1->nb_states * m1->nb_letters * sizeof(unsigned int);
    return memcmp(m1->delta, m2->delta, size) == 0
        && memcmp(m1->rho, m2->rho, size) == 0;
}

void free_mealy(mealy_t *m) {
    if (!m) return;
    free(m->delta);
    free(m->rho);
    free(m);
}

mealy_t *dual(const mealy_t *m) {
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

mealy_t *min(const mealy_t *m) {
    unsigned int i, j, k, count;
    unsigned int
        *part = calloc(m->nb_states, sizeof(unsigned int)),
        *part2 = calloc(m->nb_states, sizeof(unsigned int));

    if (!part || !part2)
        return 0;

    count = 0;
    for (i = 0; i < m->nb_states; i++) {
        for (j = 0; j < i; j++) {
            for (k = 0; k < m->nb_letters; k++) {
                if (m->rho[j * m->nb_letters + k] != m->rho[i * m->nb_letters + k])
                    break;
            }

            if (k == m->nb_letters)
                break;
        }

        j = ((j == i) ? count++ : part[j]);
        part[i] = j;
    }

    while (1) {
        count = 0;

        for (i = 0; i < m->nb_states; i++) {
            for (j = 0; j < i; j++) {
                for (k = 0; part[i] == part[j] && k < m->nb_letters; k++) {
                    if (part[m->delta[i * m->nb_letters + k]]
                        != part[m->delta[j * m->nb_letters + k]])
                        break;
                }

                if (k == m->nb_letters)
                    break;
            }

            j = ((j == i) ? count++ : part2[j]);

            part2[i] = j;
        }

        if (memcmp(part2, part, m->nb_states * sizeof(unsigned int)) == 0) {
            memcpy(part, part2, m->nb_states * sizeof(unsigned int));
            break;
        }

        memcpy(part, part2, m->nb_states * sizeof(unsigned int));
        memset(part2, 0, m->nb_states * sizeof(unsigned int)); //useless
    }

    mealy_t *mm = mealy(count, m->nb_letters);
    if (!mm) return 0;

    for (i = 0; i < count; i++) {
        for (j = 0; j < m->nb_states; j++)
            if (part[j] == i) break;

        for (k = 0; k < m->nb_letters; k++) {
            mm->delta[i * m->nb_letters + k] = part[m->delta[j * m->nb_letters + k]];
            mm->rho[i * m->nb_letters + k] = m->rho[j * m->nb_letters + k];
        }
    }

    free(part);
    free(part2);

    return mm;
}


mealy_t *md_reduce(const mealy_t *machine) {
    mealy_t *a, *b, *c;

    a = min(machine);
    b = 0;

    while (!mealy_eq(a, b)) {
        if (b) {
            free_mealy(b);
        }

        b = a;
        a = min(a);
        if (mealy_eq(a, b)) {
            c = b;
            b = dual(b);
            free_mealy(c);
            c = a;
            a = min(b);
            free_mealy(c);
        }
    }

    free_mealy(b);

    return a;
}

char is_trivial (const mealy_t *m) {
    if (m == 0 || m->nb_states != 1) return 0;
    for (unsigned int i = 0; i < m->nb_letters; i++)
        if (m->rho[i] != i) return 0;
    return 1;
}

char is_md_trivial (const mealy_t *m) {
    mealy_t *red, *d;
    char ret = 0;

    red = md_reduce(m);
    if (is_trivial(red)) {
        ret = 1;
    } else {
        d = dual(red);
        if (is_trivial(d)) {
            ret = 1;
        }

        free_mealy(d);
    }

    free_mealy(red);

    return ret;
}


mealy_t *product(const mealy_t *m1, const mealy_t *m2) {
    unsigned int nbl = m1->nb_letters,
        nbs = m1->nb_states * m2->nb_states,
        p, x, r, q, y, i;

    mealy_t *prod = mealy(nbs, nbl);
    if (!prod) return 0;

    for (p = 0; p < m1->nb_states; p++) {
        for (x = 0; x < m2->nb_letters; x++) {
            i = p * m1->nb_letters + x;
            q = m1->delta[i];
            y = m1->rho[i];
            for (r = 0; r < m2->nb_states; r++) {
                i = (p * m2->nb_states + r) * prod->nb_letters + x;
                prod->delta[i] = q * m2->nb_states
                    + m2->delta[r * m2->nb_letters + y];
                prod->rho[i] = m2->rho[r * m2->nb_letters + y];
            }
        }
    }

    return prod;
}


unsigned int
mexp(const mealy_t *machine, unsigned int bound, unsigned int upbound) {
    unsigned int i, max;
    mealy_t *m, *tmp, *prev;

    if (!machine) return -1;

    prev = NULL;
    m = min(machine);

    for (i = 0; i < bound
             && (prev == NULL || prev->nb_states != m->nb_states)
             && m->nb_states < upbound; i++) {
        free_mealy(prev);
        prev = m;
        tmp = product(m, machine);
        m = min(tmp);
        free_mealy(tmp);
        printf("mass %u\n", m->nb_states);
    }

    max = m->nb_states;
    free_mealy(prev);
    free_mealy(m);

    return max;
}
