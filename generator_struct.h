#include "nauty.h"

struct LinkedList{
	graph *can;
	struct LinkedList *next;
};

typedef struct LinkedList *LinkedList;

LinkedList add_can(LinkedList list, graph *can, size_t can_sz);
short is_in_list(LinkedList list, graph *can, size_t can_sz);
int size_of_list(LinkedList list);