typedef struct frag_list {
    char fragname[255];
    struct frag_list *next;
} frag_t;

frag_t *fragment_file(int fd, int *nb);

void free_frag_t(frag_t *frags);

void reassemble_files(frag_t *frags);
