typedef struct mealy_machine {
    unsigned int nb_letters, nb_states;
    unsigned int *delta, *rho;
} mealy_t;


mealy_t *mealy(unsigned int nb_states, unsigned int nb_letters);

char mealy_eq(mealy_t *m1, mealy_t *m2);

void free_mealy(mealy_t *m);

mealy_t *dual(const mealy_t *m);

mealy_t *min(const mealy_t *m);

mealy_t *md_reduce(mealy_t *a);

char is_trivial(mealy_t *m);

char is_md_trivial(mealy_t *m);

mealy_t *product(mealy_t *m1, mealy_t *m2);

unsigned int mexp(mealy_t *m, unsigned int bound);
