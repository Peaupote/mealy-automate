#include "nausparse.h"

struct LinkedList{
	graph *can;
	size_t can_sz;
	struct LinkedList *next;
};

typedef struct LinkedList *LinkedList;

LinkedList new_node(int m, int n);
short is_in_list(LinkedList list, graph *can, int m, int n);
int size_of_list(LinkedList list);

struct LinkedListSparse{
	sparsegraph *sg;
	struct LinkedListSparse *next;
};

typedef struct LinkedListSparse *LinkedListSparse;

LinkedListSparse new_node_sparse(int nb_vertices, int nb_edges);
short is_in_list_sparse(LinkedListSparse list, sparsegraph *can);
void print_sparse_list(LinkedListSparse list);