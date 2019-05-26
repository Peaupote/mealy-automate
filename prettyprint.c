#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

#include "nauty.h"
#include "utils.h"

int fd;
unsigned char nb_states, nb_letters, size;
unsigned long count = 0, trivial_count = 0, finite_not_trivial = 0;
unsigned char *buffer, *delta, *rho;

int main (int argc, char *argv[]) {
    if (argc < 2) {
        printf("usage: %s <file>\n", argv[0]);
        return 1;
    }

    int rc;
    fd = open(argv[1], O_RDONLY, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    rc = read(fd, &nb_states, 1);
    if (rc < 0) {
        perror("read nb_states");
        return 1;
    }

    rc = read(fd, &nb_letters, 1);
    if (rc < 0) {
        perror("read nb_states");
        return 1;
    }

    printf("Dimesion %u, %u\n", nb_states, nb_letters);

    size = nb_states * nb_letters;

    int sl = size + nb_states,
        st = st + nb_letters,
        n = size + nb_letters + nb_states + 3,
        m = ceil(n / WORDSIZE);
    m = SETWORDSNEEDED(n);

    nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);

    unsigned int x, p, index;
    mealy_t *machine, *red;

    /* DYNALLSTAT(graph, g, g_sz); */
    /* DYNALLSTAT(int, lab, lab_sz); */
    /* DYNALLSTAT(int, ptn, ptn_sz); */
    /* DYNALLSTAT(int, orbits, orbits_sz); */
    /* static DEFAULTOPTIONS_GRAPH(options); */
    /* statsblk stats; */

    /* DYNALLOC2(graph, g, g_sz, m, n, "malloc"); */
    /* DYNALLOC1(int, lab, lab_sz, n, "malloc"); */
    /* DYNALLOC1(int, ptn, ptn_sz, n, "malloc"); */
    /* DYNALLOC1(int, orbits, orbits_sz, n, "malloc"); */

    /* options.writeautoms = TRUE; */

    buffer = malloc(size);
    while ((rc = read(fd, buffer, size)) > 0) {
        if (rc < size) {
            fprintf(stderr, "Corrupted file\n");
            return 1;
        }

        delta = malloc(size);
        rho = malloc(size);

        machine = malloc(sizeof(mealy_t));
        machine->nb_states = nb_states;
        machine->nb_letters = nb_letters;
        machine->delta = delta;
        machine->rho = rho;

        printf("Machine %lu\n", ++count);
        printf("delta:\n");
        memcpy(delta, buffer, size);

        for (int p = 0; p < nb_states; p++) {
            for (int x = 0; x < nb_letters; x++) {
                printf("%u ", buffer[p * nb_states + x]);
            }
            printf("\n");
        }

        rc = read(fd, buffer, size);
        if (rc < size) {
            fprintf(stderr, "Corrupted file\n");
            return 1;
        }

        printf("rho:\n");
        memcpy(rho, buffer, size);

        for (int p = 0; p < nb_states; p++) {
            for (int x = 0; x < nb_letters; x++) {
                printf("%u ", buffer[p * nb_states + x]);
            }
            printf("\n");
        }

        //
        /* EMPTYGRAPH(g, m, n); */
        /* ADDONEEDGE(g, sl + 1, sl + 2, m); */

        /* for (x = 0; x < nb_letters; x++) { */
        /*     ADDONEEDGE(g, st + x, sl + 1, m); */
        /* } */

        /* for (p = 0; p < nb_states; p++) { */
        /*     ADDONEEDGE(g, size + p, sl, m); */
        /*     for (x = 0; x < nb_letters; x++) { */
        /*         index = p * nb_letters + x; */
        /*         ADDONEEDGE(g, index, delta[index] * nb_letters + rho[index], m); */
        /*         ADDONEEDGE(g, index, size + p, m); */
        /*         ADDONEEDGE(g, index, st + x, m); */
        /*     } */
        /* } */

        /* ADDONEEDGE(g, index, delta[index] * nb_letters + rho[index], m); */

        /* densenauty(g, lab, ptn, orbits, &options, &stats, m, n, 0); */

        /* printf("Automorphism group size = "); */
        /* writegroupsize(stdout, stats.grpsize1, stats.grpsize2); */
    }

    printf("Total count %lu.\n", count);

    close(fd);
    return 0;
}
