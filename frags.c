#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>


#include "frags.h"

#define FRAG_COUNT 1000

extern u_int8_t size, nb_states, nb_letters;

frag_t *fragment_file(int fd, int *nb) {
    int rc, ffd, nonce = rand();
    unsigned int sz = size * 2 * FRAG_COUNT;
    char *buffer = malloc(sz);
    frag_t *ret = 0;
    *nb = 0;

    while ((rc = read(fd, buffer, sz)) > 0) {
        if (rc < 0 || rc % 2 * size != 0) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        (*nb)++;
        frag_t *frag = malloc(sizeof(frag_t));
        if (!frag) exit(42);

        snprintf(frag->fragname, 255, "/tmp/mealyfrag%d_%d", nonce, *nb);
        frag->next = ret;
        ret = frag;

        ffd = open(frag->fragname, O_CREAT|O_WRONLY, 0644);
        if (ffd < 0) {
            perror("open");
            exit(42);
        }

        printf("fragment of size %d - %d\n", rc, rc/(2*size));
        rc = write(ffd, buffer, rc);
        if (rc < 0) {
            perror("write");
            exit(42);
        }

        close(ffd);
    }

    free(buffer);
    return ret;
}

void free_frag_t(frag_t *frags) {
    frag_t *curr = frags;
    frag_t *next;
    while(curr->next != NULL) {
        next = curr->next;
        free(curr);
        curr = next;
    }
    free(curr);
}

void reassemble_files(frag_t *frags) {

}
