#include "generator_struct.h"

LinkedList add_can(LinkedList list, graph *can, size_t can_sz){
    LinkedList new = malloc(sizeof(LinkedList));
    new->can = malloc(can_sz);
    memcpy(new->can, can, can_sz);
    new->next = list;
    return new;
}

short is_in_list(LinkedList list, graph *can, size_t can_sz) {
    while(list != NULL) {
        if(!memcmp(can, list->can, can_sz)) {
            return 1;
        }
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
