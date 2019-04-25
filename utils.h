typedef struct mealy_machine {
    unsigned int nb_letters, nb_states;
    u_int8_t *delta, *rho;
} mealy_t;


mealy_t *mealy(uint nb_states, uint nb_letters);

char mealy_eq(mealy_t *m1, mealy_t *m2);

void free_mealy(mealy_t *m);

mealy_t *dual(mealy_t *m);

mealy_t *min(mealy_t *m);

mealy_t *md_reduce(mealy_t *a);

mealy_t *product(mealy_t *m1, mealy_t *m2);

unsigned int mexp(mealy_t *m, unsigned int bound);
