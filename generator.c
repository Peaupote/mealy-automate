#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int fd = -1, nb_states, nb_letters, size;
u_int32_t sup, count;
u_int8_t *delta, *rho;
int buffersize, bufferp;
unsigned char *buffer;
char debug = 0;

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
    if (i>=0) (*tab) ^= 1UL << i++;
    if (i<0) i = 0;
    while (i < size && ((*tab) >> i) & 1) i++;
    if (i < size) (*tab) ^= 1UL << i;
    return i;
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

        if (debug) {
            pt(delta);
            pt(rho);
            printf("find one %u\n", count);
        }

        if (fd) {
            if (bufferp < buffersize) {
                memcpy(buffer + bufferp, delta, size);
                memcpy(buffer + bufferp + size, rho, size);
                bufferp += size * 2;
            } else {
                write(fd, buffer, bufferp);
                bufferp = 0;
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
                rec(start_p, start_x, next_p, next_x, sources, targets, ident + 4);
                sources ^= index;
            }
        } else {
            if (valid_delta(delta) && valid_rho(rho)) {
                rec(0xFF, 0xFF, 0xFF, 0xFF, sources, targets, ident + 4);
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
    if (argc < 3) {
        fprintf(stderr, "usage: %s <nb_states> <nb_letters>\n", argv[0]);
        return 1;
    }

    nb_states = atoi(argv[1]);
    nb_letters = atoi(argv[2]);

    if (argc > 3) {
        fd = open(argv[3], O_WRONLY|O_CREAT, 0644);
        if (fd < 0) {
            perror("open");
            return 1;
        }
    }

    unsigned char nbl = nb_letters,
        nbs = nb_states;

    write(fd, &nbs, 1);
    write(fd, &nbl, 1);

    debug = (argc == 5);

    size = nb_letters * nb_states;
    sup = (1UL << size);

    delta = malloc(size);
    if (*delta) return -1;
    rho = malloc(size);
    if (*rho) return -1;

    for(unsigned int p = 0; p < nb_states; p++) {
        for(unsigned int x = 0; x < nb_letters; x++) {
            delta[p * nb_letters + x] = 0xFF;
            rho[p * nb_letters + x] = 0xFF;
        }
    }

    buffersize = nb_letters * nb_states * 2 * 10000000;
    buffer = malloc(buffersize);
    bufferp = 0;

    printf("alloc done.\n");

    rec(0xFF, 0xFF, 0xFF, 0xFF, 0, 0, 0);

    if (fd > 0 && bufferp > 0) {
        write(fd, buffer, bufferp);
    }

    printf("%u\n", count);
    close(fd);
    return 0;
}
