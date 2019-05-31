typedef struct frag_list {
    char fragname[255];
    struct frag_list *next;
} frag_t;

frag_t *fragment_file(int fd, int *nb);

void reassemble_files(frag_t *frags);
