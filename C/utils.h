typedef struct mealy_machine {
    unsigned int nb_letters, nb_states;
    unsigned int *delta, *rho;
} mealy_t;

mealy_t *mealy(unsigned int nb_states, unsigned int nb_letters);

char mealy_eq(const mealy_t *m1, const mealy_t *m2);

char *mealy_to_string(const mealy_t *m);

void free_mealy(mealy_t *m);

mealy_t *dual(const mealy_t *m);

mealy_t *min(const mealy_t *m);

mealy_t *md_reduce(const mealy_t *a);

char is_trivial(const mealy_t *m);

char is_md_trivial(const mealy_t *m);

mealy_t *product(const mealy_t *m1, const mealy_t *m2);

unsigned int mexp(const mealy_t *m, unsigned int bound, unsigned int max,
                  int fd_out);
