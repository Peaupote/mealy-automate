#include "nauty.h"

struct LinkedList{
	graph *can;
	size_t can_sz;
	struct LinkedList *next;
};

typedef struct LinkedList *LinkedList;

LinkedList new_node(int m, int n);
short is_in_list(LinkedList list, graph *can, int m, int n);
int size_of_list(LinkedList list);