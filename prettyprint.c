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
u_int8_t nb_states, nb_letters, size;
unsigned long count = 0, trivial_count = 0;
unsigned char *buffer, *delta, *rho;
mealy_t *machine, *red;

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

    while ((rc = read(fd, buffer, size)) > 0) {
        if (rc < size) {
            fprintf(stderr, "Corrupted file\n");
            return 1;
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
            return 1;
        }

        //printf("rho:\n");
        for(unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->rho+i, &c, sizeof(unsigned int));
        }

        if(is_md_trivial(machine)) {
            trivial_count++;
            printf("%u\n", mexp(machine, 7));
        }

        free_mealy(machine);
        // if (count >= 1000) return 0;

    }

    printf("md trivial %lu.\n", trivial_count);
    printf("Total count %lu.\n", count);

    close(fd);
    return 0;
}
