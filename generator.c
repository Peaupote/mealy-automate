#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <sys/wait.h>
#include <assert.h>

#include "nauty.h"
#include "generator_struct.h"

char *usage =
    "Usage: %s [-s nb_states] [-l nb_letters]"
    "[-o outputfile] [-f nb_forks] [-d] [-n]\n";

char *dreadnaut = "./nauty26r11/dreadnaut";

int fd = -1, nb_states = 2, nb_letters = 2, size,
    sl, st, n, m,
    nb_forks = 0, depth = 0;
u_int32_t sup, count = 0, can_count = 0;
u_int8_t *delta, *rho;
int buffersize, bufferp;
unsigned char *buffer;
char debug = 0, use_nauty = 0;
LinkedList canlist = NULL;

DYNALLSTAT(graph, g, g_sz);
DYNALLSTAT(graph, can, can_sz);
DYNALLSTAT(int, lab, lab_sz);
DYNALLSTAT(int, ptn, ptn_sz);
DYNALLSTAT(int, orbits, orbits_sz);
static DEFAULTOPTIONS_GRAPH(options);
statsblk stats;

void pb(u_int32_t t, int indent) {
    for (int i = 0; i <= indent; i++) printf(" ");
    for (unsigned int i = 0; i < size; i++) {
        printf("%d", (t >> i) & 1);
    }
    printf("\n");
}

void pt(u_int8_t *tab) {
    unsigned int p, x;
    for (p = 0; p < nb_states; p++) {
        for (x = 0; x < nb_letters; x++) {
            printf("%u ", tab[p * nb_letters + x]);
        }
    }
    printf("\n");
}

int valid_rho() {
    unsigned int p, x, index, out;
    for (p = 0; p < nb_states; p++) {
        out = 0;
        for(x = 0; x < nb_letters; x++) {
            index = p * nb_letters + x;
            if (rho[index] == 0xFF) continue;
            if ((1UL << rho[index]) & out) return 0;
            out ^= 1UL << rho[index];
        }
    }

    return 1;
}

int valid_delta() {
    unsigned int p, x, index, out;
    for(x = 0; x < nb_letters; x++) {
        out = 0;
        for(p = 0; p < nb_states; p++) {
            index = p * nb_letters + x;
            if (delta[index] == 0xFF) continue;
            if ((1UL << delta[index]) & out) return 0;
            out ^= 1UL << delta[index];
        }
    }

    return 1;
}

unsigned int pop(u_int32_t *tab, unsigned int i) {
    for (; i < size; i++) {
        if ((((*tab) >> i) & 1) == 0) {
            *tab ^= 1UL << i;
            return i;
        }
    }

    return i;
}

unsigned int iter(u_int32_t *tab, unsigned int i) {
    if (i >= 0) (*tab) ^= 1UL << i++;
    if (i < 0) i = 0;
    while (i < size && ((*tab) >> i) & 1) i++;
    if (i < size) (*tab) ^= 1UL << i;
    return i;
}

int canonical() {
    unsigned int x, p, index, k;

    int rc, st, fds[2], fds2[2];
    rc = pipe(fds);
    if (rc < 0) {
        perror("pipe");
        exit(1);
    }

    rc = pipe(fds2);
    if (rc < 0) {
        perror("pipe");
        exit(1);
    }

    rc = fork();
    if (rc == 0) {
        dup2(fds[0], 0);
        dup2(fds2[1], 1);
        close(fds[0]);
        close(fds[1]);
        close(fds2[0]);
        close(fds2[1]);
        // rc = execlp("/usr/bin/cat", "cat", 0);
        rc = execl(dreadnaut, dreadnaut, 0);
        if (rc < 0) {
            perror("execl");
            exit(1);
        }
        exit(0);
    }

    close(fds2[1]);
    close(fds[0]);
    FILE *din = fdopen(fds[1], "w");
    fprintf(din, "n=%d d ", n);
    fprintf(din, " f=[ 0:%d | %d:%d ] g\n", size - 1,
            size, size + nb_states - 1);

    // LinkedList new = new_node(m, n);
    EMPTYGRAPH(g, m, n);

    for (p = 0; p < nb_states; p++) {
        for (x = 0; x < nb_letters; x++) {
            index = p * nb_letters + x;
            fprintf(din, "%d, %d, %d;\n",
                    delta[index] * nb_letters + rho[index],
                    size + p, size + nb_states + x);
        }
    }

    for (p = 0; p < nb_states + nb_letters; p++)
        fprintf(din, ";");

    fprintf(din, " p c *=13 k=0 99 x b q");
    fflush(din);
    fclose(din);
    close(fds[1]);

    rc = waitpid(rc, &st, 0);
    if (rc < 0) {
        perror("waitpid");
        exit(1);
    }

    char buff[5000];
    int len;
    while((rc = read(fds2[0], buff + len, 5000 - len)) > 0)
        len += rc;

    close(fds2[0]);

    if (rc < 0) {
        perror("read");
        exit(1);
    }

    char *ptr = memmem(buff, len, ".\n", 2);
    assert(ptr != 0);

    ptr += 2 * (1 + size);

    //write(1, ptr, len - (ptr - buff));
    char *end = memchr(ptr, '\n', len - (ptr - buff));
    assert(end != 0);
    *end = 0;

    int h;
    for (p = 0; p < nb_states + nb_letters; p++, ptr = 0) {
        char *tmp = strtok(ptr, " ");
        h = atoi(tmp);
        //printf("%s=%d, ", tmp, h);
        if (h != p + size) return 0;
    }

    //printf("\n--\n");

    return 1;
}

void rec(u_int8_t start_p, u_int8_t start_x,
         u_int8_t prev_p, u_int8_t prev_x,
         u_int32_t sources, u_int32_t targets, int ident) {
    if (debug) {
        printf("====\n");
        pb(sources, ident);
        pb(targets, ident);
    }

    if (sup - 1 == sources && sup - 1 == targets) {
        count++;
        if (count % 100000 == 0) {
            printf("%u\n", count);
        }

        if (!use_nauty || (use_nauty && canonical())) {
            if (debug) {
                pt(delta);
                pt(rho);
                printf("find one %u\n", count);
            }

            can_count++;
            if (fd > 0) {
                memcpy(buffer + bufferp, delta, size);
                memcpy(buffer + bufferp + size, rho, size);
                bufferp += size * 2;

                if (bufferp == buffersize) {
                    write(fd, buffer, bufferp);
                    bufferp = 0;
                }
            }
        }
        return;
    }

    unsigned char add = 0;
    unsigned int index, i = -1;
    u_int8_t next_p, next_x;

    if (prev_x == 0xFF) {
        add = 1;
        index = pop(&sources, 0);
        start_p = index / nb_letters;
        start_x = index % nb_letters;
        prev_p = start_p;
        prev_x = start_x;
        if (debug)
            printf("%*s new start %u, %u\n", ident, "", start_p, start_x);
    }

    while((i = iter(&targets, i)) < size) {
        next_p = i / nb_letters;
        next_x = i % nb_letters;
        if (debug) {
            printf("%*s in while %u\n", ident, "", i);
            pb(sources, ident);
            pb(targets, ident);
            printf("%*s next %u, %u\n", ident, "", next_p, next_x);
        }

        index = prev_p * nb_letters + prev_x;
        delta[index] = next_p;
        rho[index] = next_x;

        if (next_p != start_p || next_x != start_x) {
            if (valid_delta(delta) && valid_rho(rho)) {
                index = 1UL << (next_p * nb_letters + next_x);
                sources ^= index;
                if (depth < nb_forks) {
                    if (fork() == 0) {
                        depth++;
                        rec(start_p, start_x, next_p, next_x,
                            sources, targets, ident + 4);
                        return;
                    }
                } else {
                    rec(start_p, start_x, next_p, next_x,
                        sources, targets, ident + 4);
                }
                sources ^= index;
            }
        } else {
            if (valid_delta(delta) && valid_rho(rho)) {
                if (depth < nb_forks) {
                    if (fork() == 0) {
                        depth++;
                        rec(0xFF, 0xFF, 0xFF, 0xFF, sources, targets, ident + 4);
                        return;
                    }
                } else {
                    rec(0xFF, 0xFF, 0xFF, 0xFF, sources, targets, ident + 4);
                }

            }
        }

        index = prev_p * nb_letters + prev_x;
        delta[index] = 0xFF;
        rho[index] = 0xFF;
    }

    if (add) {
        sources ^= 1 << (start_p * nb_letters + start_x);
    }

    if (debug)
        printf("%*s end\n", ident, "");
}

int main (int argc, char *argv[]) {
    int opt;

    while((opt = getopt(argc, argv, "s:l:f:o:dn")) != -1) {
        switch(opt) {
        case 's':
            nb_states = atoi(optarg);
            break;
        case 'l':
            nb_letters = atoi(optarg);
            break;
        case 'f':
            nb_forks = atoi(optarg);
            break;
        case 'o':
            fd = open(optarg, O_WRONLY|O_CREAT, 0644);
            if (fd < 0) {
                perror("open");
                return 1;
            }
            break;
        case 'd':
            debug = 1;
            break;
        case 'n':
            use_nauty = 1;
            break;
        default:
            fprintf(stderr, usage, argv[0]);
            return 1;
        }
    }

    unsigned char nbl = nb_letters,
        nbs = nb_states;

    write(fd, &nbs, 1);
    write(fd, &nbl, 1);

    size = nb_letters * nb_states;
    sup = (1UL << size);


    delta = malloc(size);
    if (!delta) return -1;
    rho = malloc(size);
    if (!rho) return -1;

    for(unsigned int p = 0; p < nb_states; p++) {
        for(unsigned int x = 0; x < nb_letters; x++) {
            delta[p * nb_letters + x] = 0xFF;
            rho[p * nb_letters + x] = 0xFF;
        }
    }

    buffersize = size * 2 * 10000000;
    buffer = malloc(buffersize);
    bufferp = 0;

    if (use_nauty) {
        options.getcanon = TRUE;
        //options.defaultptn = FALSE;

        n = size + nb_letters + nb_states;
        m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);

        DYNALLOC2(graph, g, g_sz, n, m, "malloc");
        DYNALLOC2(graph, can, can_sz, n, m, "malloc");

        DYNALLOC1(int, lab, lab_sz, n, "malloc");
        DYNALLOC1(int, ptn, ptn_sz, n, "malloc");
        DYNALLOC1(int, orbits, orbits_sz, n, "malloc");

        printf("Size = %d\n", size);
        printf("Nb_states = %d\n", nb_states);
        printf("Nb_letters = %d\n", nb_letters);
        printf("N = %d\n", n);
        //m = ceil(n / WORDSIZE);

        // options.writeautoms = TRUE;
    }

    printf("alloc done.\n");

    rec(0xFF, 0xFF, 0xFF, 0xFF, 0, 0, 0);

    if (fd > 0 && bufferp > 0) {
        write(fd, buffer, bufferp);
    }

    printf("Total count %u.\n", count);

    if (use_nauty) {
        printf("Canonical count %u.\n", can_count);
        // printf("Canlist size %d\n", size_of_list(canlist));
    }

    close(fd);
    while (depth < nb_forks && wait(0) > 0);
    return 0;
}
