#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

#include "nauty.h"
#include "utils.h"

#define POWER 7

int fd;
u_int8_t nb_states, nb_letters, size;
unsigned long count = 0, trivial_count = 0;
unsigned char *buffer, *delta, *rho;
mealy_t *machine, *red;

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
        }

        free_mealy(machine);
    }

    return trivial_mass_max;
}


mealy_t *check_not_trivial (unsigned int trivial_mass_max) {
    int rc;
    unsigned int mass;

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

        if(!is_md_trivial(machine)) {
            mass = mexp(machine, POWER, trivial_mass_max);

            if (mass < trivial_mass_max) {
                printf("problem here %u < %u\n", mass, trivial_mass_max);
                return machine;
            }

            printf("mass %u > %u\n", mass, trivial_mass_max);
        }

        free_mealy(machine);
    }

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

    unsigned int trivial_mass_max = max_md_trivial();

    printf("md trivial %lu.\n", trivial_count);
    printf("Total count %lu.\n", count);
    printf("Max mass upper bound found: %u\n", trivial_mass_max);
    printf("Look for non-md-trivial.\n");

    // back to beginning of file
    lseek(fd, 2, SEEK_SET);

    mealy_t *res = check_not_trivial(trivial_mass_max);
    if (!res) {
        printf("Seems to work !\n");
    } else {
        printf("This one seems to be a counter example.\n");
    }

    free_mealy(res);
    close(fd);
    return 0;
}
