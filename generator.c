#include <stdio.h>
#include <stdlib.h>

int nb_states, nb_letters, size;
u_int32_t sup, count;
u_int8_t *delta, *rho;

void pb(u_int32_t t) {
    for (unsigned int i = 0; i < size; i++) {
        printf("%d", (t >> i) & 1);
    }
    printf("\n");
}

int valid_rho() {
    unsigned int p, x, index, out;
    for (p = 0; p < nb_states; p++) {
        out = 1UL << nb_letters;
        for(x = 0; x < nb_letters; x++) {
            index = p * nb_letters + x;
            if (rho[index] == 0xFF) continue;
            if (((1 << rho[index]) & out) != 0) return 0;
            out ^= 1 << rho[index];
        }
    }

    return 1;
}

int valid_delta() {
    unsigned int p, x, index, out;
    for(x = 0; x < nb_letters; x++) {
        out = 1UL << nb_states;
        for(p = 0; p < nb_states; p++) {
            index = p * nb_letters + x;
            if (delta[index] == 0xFF) continue;
            if (((1 << delta[index]) & out) != 0) return 0;
            out ^= 1 << delta[index];
        }
    }

    return 1;
}

unsigned int pop(u_int32_t *tab, unsigned int i) {
    //printf("pop %u\n", i);
    //pb(*tab);
    for (; i < size; i++) {
        if (((*tab) & (1UL << i)) == 0) {
            *tab ^= 1UL << i;
            return i;
        }
    }

    return i;
}

unsigned int iter(u_int32_t *tab, unsigned int i) {
    //printf("iter %u\n", i);
    //pb(*tab);
    if (i) (*tab) ^= 1UL << i++;
    while (i < size && ((*tab) >> i) & 1) i++;
    if (i < size) (*tab) ^= 1UL << i;
    return i;
}

unsigned int len(u_int32_t tab) {
    unsigned int i, c = 0;
    for (i = 0; i < size; i++) {
        if ((tab & (1UL << i)) == 0) c++;
    }
    return c;
}

void rec(u_int8_t start_p, u_int8_t start_x,
         u_int8_t prev_p, u_int8_t prev_x,
         u_int32_t sources, u_int32_t targets) {
    //printf("====\n");
    //pb(sources);
    //pb(targets);
    if (sup - 1 == sources && sup - 1 == targets) {
        count++;
        printf("find one %u\n", count);
        return;
    }

    unsigned char add = 0;
    unsigned int index, i = 0;
    u_int8_t next_p, next_x;

    if (prev_x == 0xFF) {
        add = 1;
        index = pop(&sources, 0);
        start_p = index / nb_letters;
        start_x = index % nb_letters;
        //printf("new start %u, %u\n", start_p, start_x);
    }

    //u_int32_t tmp = targets;
    while((i = iter(&targets, i)) < size) {
        next_p = i / nb_letters;
        next_x = i % nb_letters;
        //printf("in while %u\n", i);
        //pb(tmp);
        //pb(targets);
        //printf("next %u, %u\n", next_p, next_x);

        index = prev_p * nb_letters + prev_x;
        delta[index] = next_p;
        rho[index] = next_x;

        if (next_p != start_p || next_x != start_x) {
            //printf("not loop\n");
            if (valid_delta(delta) && valid_rho(rho)) {
                index = 1UL << (next_p * nb_letters + next_x);
                sources ^= index;
                rec(start_p, start_x, next_p, next_x, sources, targets);
                sources ^= index;
            }
        } else {
            //printf("loop\n");
            if (valid_delta(delta) && valid_rho(rho)) {
                rec(0xFF, 0xFF, 0xFF, 0xFF, sources, targets);
            }
        }

        index = prev_p * nb_letters + prev_x;
        delta[index] = 0xFF;
        rho[index] = 0xFF;
    }

    if (add) {
        sources ^= 1 << (start_p * nb_letters + start_x);
    }

    //printf("end\n\n");
}

int main (int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s nb_states nb_letters\n", argv[0]);
        return 1;
    }

    nb_states = atoi(argv[1]);
    nb_letters = atoi(argv[2]);

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


    printf("alloc done.\n");

    rec(0xFF, 0xFF, 0xFF, 0xFF, 0, 0);

    printf("%u\n", count);
}
