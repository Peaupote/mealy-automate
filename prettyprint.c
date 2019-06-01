#include <fcntl.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <wait.h>

#include "frags.h"
#include "nauty.h"
#include "utils.h"

#define POWER 100
#define MAX_FORK 2
#define TAMPON_SIZE 51200

int fd, fd_max, fd_out, fd_not_trivial, fd_plot;
u_int8_t nb_states, nb_letters, size;
unsigned long count = 0, trivial_count = 0;
unsigned char *buffer, *delta, *rho;
mealy_t *machine, *red;

unsigned int max_md_trivial(int fd_in, int fd_out, int fd_not_trivial) {
    int rc;
    unsigned int mass, trivial_mass_max = 0;

    while ((rc = read(fd_in, buffer, 2*size)) > 0) {
        if (rc < 2*size) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        machine = mealy(nb_states, nb_letters);

        printf("Machine %lu\n", ++count);
        // printf("delta:\n");
        unsigned int c;
        for (unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->delta + i, &c, sizeof(unsigned int));
        }

        // printf("rho:\n");
        for (unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[size+i];
            memcpy(machine->rho + i, &c, sizeof(unsigned int));
        }

        if (is_md_trivial(machine)) {
            trivial_count++;
            mass = mexp(machine, POWER, -1, fd_out);
            printf("mass upper bound %u\n", mass);

            if (mass > trivial_mass_max) {
                trivial_mass_max = mass;
            }
        } else {
            rc = write(fd_not_trivial, buffer, 2*size);
            if(rc != 2*size) {
                fprintf(stderr, "Erreur de copie dans not_trivial\n");
                exit(42);
            }
        }

        free_mealy(machine);
    }

    return trivial_mass_max;
}

mealy_t *check_not_trivial(unsigned int trivial_mass_max, int fd_out,
                           int fd_not_trivial) {
    int rc;
    unsigned int mass;

    while ((rc = read(fd_not_trivial, buffer, 2*size)) > 0) {

        if (rc < 2*size) {
            fprintf(stderr, "Corrupted file\n");
            exit(42);
        }

        machine = mealy(nb_states, nb_letters);

        // printf("delta:\n");
        unsigned int c;
        for (unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[i];
            memcpy(machine->delta + i, &c, sizeof(unsigned int));
        }

        // printf("rho:\n");
        for (unsigned int i = 0; i < size; i++) {
            c = (unsigned int)buffer[size+i];
            memcpy(machine->rho + i, &c, sizeof(unsigned int));
        }

        mass = mexp(machine, POWER * 10, trivial_mass_max, fd_out);

        if (mass < trivial_mass_max) {
            printf("problem here %u < %u\n", mass, trivial_mass_max);
            return machine;
        }

        printf("mass %u > %u\n", mass, trivial_mass_max);

        free_mealy(machine);
    }

    return 0;
}

int work_md_trivial(int fd_in, int fd_out, int fd_not_trivial) {
    unsigned int trivial_mass_max = max_md_trivial(fd_in, fd_out, fd_not_trivial);

    write(fd_max, &trivial_mass_max, sizeof(unsigned int));

    printf("md trivial %lu.\n", trivial_count);
    printf("Total count %lu.\n", count);
    printf("Max mass upper bound found: %u\n", trivial_mass_max);
    return 0;
}

int work_not_md_trivial(unsigned int trivial_mass_max, int fd_out,
                        int fd_not_trivial) {
    printf("Look for non-md-trivial.\n");

    mealy_t *res = check_not_trivial(trivial_mass_max, fd_out, fd_not_trivial);
    if (!res) {
        printf("Seems to work !\n");
    } else {
        printf("This one seems to be a counter example.\n");
    }

    if (res != NULL) {
        printf("create file %s\n", "RES");
        int fd_res = open("RES", O_CREAT | O_WRONLY | O_APPEND, 0644);
        if (fd_res < 0) {
            perror("open");
            exit(42);
        }
        write(fd_res, "CONTRE EXEMPLE ", 16);
        char *res_str = mealy_to_string(res);
        printf("CONTRE EXEMPLE %s\n", res_str);
        write(fd_res, res_str, strlen(res_str));
        free(res_str);
        close(fd_res);
    }
    free_mealy(res);
    return 0;
}

void process(int st) {
    switch (WEXITSTATUS(st)) {
    case 0:
        printf("Fork done. Found no counter examples\n");
        break;
    case 1:
        printf("Fork done. Counter example founded !!!\n");
        break;

    default:
        printf("Something terrible happend !!\n");
        exit(42);
    }
}

unsigned int get_trivial_mass_max(int nb) {
    unsigned int buff[nb];
    lseek(fd_max, 0, SEEK_SET);
    if (read(fd_max, buff, nb * sizeof(unsigned int)) !=
        nb * sizeof(unsigned int)) {
        perror("fraglent trivial mass");
        exit(42);
    }
    unsigned int trivial_mass_max = buff[0];
    for (unsigned int i = 0; i < nb; i++) {
        if (buff[i] > trivial_mass_max) {
            trivial_mass_max = buff[i];
        }
    }
    close(fd_max);
    printf("Remove /tmp/max_list\n");
    int rc = remove("/tmp/max_list");
    if (rc != 0) {
        perror("remove /tmp/max_list");
        exit(42);
    }
    return trivial_mass_max;
}

int main(int argc, char *argv[]) {
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
    buffer = malloc(2*size);

    int nb, st, forkcount = 0;
    frag_t *p, *frags = fragment_file(fd, &nb);
    close(fd);

    printf("Number of fragments %d\n", nb);

    printf("create file /tmp/max_list\n");
    fd_max = open("/tmp/max_list", O_CREAT|O_RDWR, 0644);
    if (fd_max < 0) {
        perror("open /tmp/max_list");
        exit(42);
    }

    for (p = frags; p; p = p->next) {
        if (forkcount >= MAX_FORK) {
            wait(&st);
            process(st);
        }

        if (fork() == 0) {
            printf("start file %s\n", p->fragname);
            fd = open(p->fragname, O_RDONLY);
            if (fd < 0) {
                perror("open");
                exit(42);
            }

            int len = strlen(p->fragname);
            char out[len + 5];
            memcpy(out, p->fragname, len);
            strcpy(out + len, ".out");

            printf("create file %s\n", out);
            fd_out = open(out, O_CREAT | O_WRONLY, 0644);
            if (fd_out < 0) {
                perror("open");
                exit(42);
            }

            char not_trivial[len + 13];
            memcpy(not_trivial, p->fragname, len);
            strcpy(not_trivial + len, ".not_trivial");
            fd_not_trivial = open(not_trivial, O_CREAT | O_WRONLY, 0644);
            if (fd_out < 0) {
                perror("open");
                exit(42);
            }

            work_md_trivial(fd, fd_out, fd_not_trivial);

            close(fd_out);
            close(fd_not_trivial);
            exit(0);
        } else {
            forkcount++;
        }
    }

    while (forkcount > 0) {
        wait(&st);
        forkcount--;
    }

    unsigned int trivial_mass_max = get_trivial_mass_max(nb);

    for (p = frags; p; p = p->next) {
        printf("666666666666666666666666666666666666666666666666666666\n");
        if (forkcount >= MAX_FORK) {
            wait(&st);
            process(st);
        }

        if (fork() == 0) {
            int len = strlen(p->fragname);
            char not_trivial_str[len + 13];
            memcpy(not_trivial_str, p->fragname, len);
            strcpy(not_trivial_str + len, ".not_trivial");
            printf("open file %s\n", not_trivial_str);
            fd_not_trivial = open(not_trivial_str, O_RDONLY);
            if (fd < 0) {
                perror("open");
                exit(42);
            }

            char out[len + 5];
            memcpy(out, p->fragname, len);
            strcpy(out + len, ".out");
            printf("open file %s\n", out);
            fd_out = open(out, O_WRONLY, O_APPEND);
            if (fd_out < 0) {
                perror("open");
                exit(42);
            }

            work_not_md_trivial(trivial_mass_max, fd_out, fd_not_trivial);
 
            close(fd_out);
            close(fd_not_trivial);

            printf("remove file %s\n", p->fragname);
            rc = remove(p->fragname);
            if (rc < 0) {
                perror("remove");
                exit(42);
            }

            printf("remove file %s\n", not_trivial_str);
            rc = remove(not_trivial_str);
            if (rc < 0) {
                perror("remove");
                exit(42);
            }

            printf("Remove %s\n", not_trivial_str);
            exit(0);
        } else {
            forkcount++;
        }
    }

    while (forkcount > 0) {
        wait(&st);
        forkcount--;
        process(st);
    }

    // On concatène les fichiers de sorties

    int len = strlen(argv[1]);
    char plot[len+6];
    memcpy(plot, argv[1], len);
    strcpy(plot+len, ".plot");
    printf("Create file %s\n", plot);
    fd_plot = open(plot, O_CREAT | O_WRONLY, 0644);
    if (fd_plot < 0) {
        perror("open fd_plot");
        exit(42);
    } 

    char tampon[TAMPON_SIZE];
    ssize_t cpy;

    for (p = frags; p; p = p->next) {
        len = strlen(p->fragname);
        char out[len + 4];
        memcpy(out, p->fragname, len);
        strcpy(out + len, ".out");
        fd_out = open(out, O_RDONLY);
        if (fd_out < 0) {
            perror("open");
            exit(42);
        }
        printf("copy file %s at the end of %s\n", out, plot);
        while((rc = read(fd_out, tampon, TAMPON_SIZE)) != 0) {
            if(rc < 0) {
                perror("Erreur de lecture pendant la concaténation");
                exit(42);
            }
            cpy = write(fd_plot, tampon, rc);
            if(cpy != rc) {
                printf("ERREUR PENDANT LA CONCATENATION : ECRITURE PARTIELLE");
                exit(42);
            }
        }
        close(fd_out);
        remove(out);
        remove(p->fragname);
    }
    close(fd_plot);
    return 0;
}
