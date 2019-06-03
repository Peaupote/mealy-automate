#include "nauty.h"

int canonical() {
    unsigned int x, p, index, k;

    EMPTYGRAPH(g, m, n);
    ADDONEEDGE(g, sl + 1, sl + 2, m);

    for (x = 0; x < nb_letters; x++) {
        ADDONEEDGE(g, st + x, sl + 1, m);
    }

    for (p = 0; p < nb_states; p++) {
        ADDONEEDGE(g, size + p, sl, m);
        for (x = 0; x < nb_letters; x++) {
            index = p * nb_letters + x;
            ADDONEEDGE(g, index, delta[index] * nb_letters + rho[index], m);
            ADDONEEDGE(g, index, size + p, m);
            ADDONEEDGE(g, index, st + x, m);
        }
    }

    densenauty(g, lab, ptn, orbits, &options, &stats, m, n, can);

    for (k = 0; k < m*(size_t)n; k++) {
        if (g[k] != can[k]) return 0;
    }

    return 1;
}