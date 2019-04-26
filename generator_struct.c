#include "generator_struct.h"
#include "nauty.h"

LinkedList new_node(int m, int n){
    LinkedList new = malloc(sizeof(LinkedList));
    DYNALLOC2(graph, new->can, new->can_sz, n, m, "malloc");
    new->next = NULL;
    return new;
}

short is_in_list(LinkedList list, graph *can, int m, int n) {
    int k;
    short in;
    while(list != NULL) {
        in = 1;
        for (k = 0; k < m*(size_t)n; k++) {
           if (list->can[k] != can[k]) { 
               in = 0;
               break;
           }
        }
        if(in) return 1;
        list = list->next;
    }
    return 0;
}

int size_of_list(LinkedList list) {
    int compteur = 0;
    while(list != NULL) {
        compteur ++;
        list = list->next;
    }
    return compteur;
}
