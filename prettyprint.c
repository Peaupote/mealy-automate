#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int fd;
unsigned char nb_states, nb_letters, size;
unsigned long count = 0;
unsigned char *buffer;

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

        printf("Machine %lu\ndelta:\n", ++count);

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

        for (int p = 0; p < nb_states; p++) {
            for (int x = 0; x < nb_letters; x++) {
                printf("%u ", buffer[p * nb_states + x]);
            }
            printf("\n");
        }

        printf("\n");
    }

    close(fd);
    return 0;
}
