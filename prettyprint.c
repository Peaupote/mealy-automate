#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <wait.h>

#include "nauty.h"
#include "utils.h"
#include "frags.h"

#define POWER 7
#define MAX_FORK 2

int fd;
u_int8_t nb_states, nb_letters, size;
unsigned long count = 0, trivial_count = 0;
unsigned char *buffer, *delta, *rho;
mealy_t *machine, *red;

typedef struct index_list {
    unsigned long index;
    struct index_list *next;
} list_t;

list_t *not_md_trivial_lst = 0;

unsigned int max_md_trivial () {
    int rc;
    unsigned int mass, trivial_mass_max = 0;

    while ((rc = read(fd, buffer, size)) > 0) {
        if (rc < size) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        machine = mealy(nb_states, nb_letters);

        printf("Machine %lu\n", ++count);
        //printf("delta:\n");
        unsigned int c;
        for(unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->delta+i, &c, sizeof(unsigned int));
        }

        rc = read(fd, buffer, size);
        if (rc < size) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        //printf("rho:\n");
        for(unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->rho+i, &c, sizeof(unsigned int));
        }

        if(is_md_trivial(machine)) {
            trivial_count++;
            mass = mexp(machine, POWER, -1);
            printf("mass upper bound %u\n", mass);

            if (mass > trivial_mass_max) {
                trivial_mass_max = mass;
            }
        } else {
            list_t *node = malloc(sizeof(list_t));
            if (!node) {
                perror("malloc");
                exit(42);
            }

            node->index = count;
            node->next = not_md_trivial_lst;
            not_md_trivial_lst = node;
        }

        free_mealy(machine);
    }

    return trivial_mass_max;
}


mealy_t *check_not_trivial (unsigned int trivial_mass_max) {
    int rc;
    unsigned int mass;
    list_t *node;

    while (not_md_trivial_lst) {
        node = not_md_trivial_lst;
        not_md_trivial_lst = not_md_trivial_lst->next;
        printf("Machine %lu\n", node->index);

        rc = lseek(fd, 2 + size * 2 * (node->index - 1), SEEK_SET);
        if (rc < 0) {
            perror("lseek");
            exit(42);
        }

        free(node);

        if (read(fd, buffer, size) < size) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        machine = mealy(nb_states, nb_letters);

        //printf("delta:\n");
        unsigned int c;
        for(unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->delta+i, &c, sizeof(unsigned int));
        }

        rc = read(fd, buffer, size);
        if (rc < size) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        //printf("rho:\n");
        for(unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->rho+i, &c, sizeof(unsigned int));
        }

        mass = mexp(machine, POWER * 10, trivial_mass_max);

        if (mass < trivial_mass_max) {
            printf("problem here %u < %u\n", mass, trivial_mass_max);
            return machine;
        }

        printf("mass %u > %u\n", mass, trivial_mass_max);


        free_mealy(machine);
    }

    return 0;
}


int work() {
    unsigned int trivial_mass_max = max_md_trivial();

    printf("md trivial %lu.\n", trivial_count);
    printf("Total count %lu.\n", count);
    printf("Max mass upper bound found: %u\n", trivial_mass_max);
    printf("Look for non-md-trivial.\n");

    mealy_t *res = check_not_trivial(trivial_mass_max);
    if (!res) {
        printf("Seems to work !\n");
    } else {
        printf("This one seems to be a counter example.\n");
    }

    free_mealy(res);
    return 0;
}

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
    buffer = malloc(size);

    int nb, forkcount = 0;
    frag_t *p, *frags = fragment_file(fd, &nb);
    close(fd);

    printf("Number of fragments %d\n", nb);

    for (p = frags; p; p = p->next) {
        if (forkcount >= MAX_FORK) wait(0);

        if (fork() == 0) {
            printf("start file %s\n", p->fragname);
            fd = open(p->fragname, O_RDONLY);
            if (fd < 0) {
                perror("open");
                exit(42);
            }

            work();

            printf("remove file %s\n", p->fragname);
            rc = remove(p->fragname);
            if (rc < 0) {
                perror("remove");
                exit(42);
            }

            exit(0);
        } else {
            forkcount++;
        }
    }

    while (forkcount > 0) {
        wait(0);
        forkcount--;
    }

    return 0;
}
