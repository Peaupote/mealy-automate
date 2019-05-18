#include "nauty.h"
#include "generator_struct.h"

int main() {
  u_int8_t delta1[9] = {2, 2, 2, 0, 1, 1, 1, 0, 0};
  u_int8_t rho1[9] = {1, 2, 0, 1, 0, 2, 1, 0, 2};
  u_int8_t delta2[9] = {2, 2, 1, 1, 1, 2, 0, 0, 0};
  u_int8_t rho2[9] = {2, 1, 0, 2, 1, 0, 1, 2, 0};

  u_int8_t delta3[9] = {1, 1, 1, 0, 0, 0, 2, 2, 2};
  u_int8_t rho3[9] = {1, 0, 2, 2, 1, 0, 1, 0, 2};

  int nb_states = 3;
  int nb_letters = 3;

  DYNALLSTAT(int, lab1, lab1_sz);
  DYNALLSTAT(int, lab2, lab2_sz);
  DYNALLSTAT(int, lab3, lab3_sz);
  DYNALLSTAT(int, ptn, ptn_sz);
  DYNALLSTAT(int, orbits, orbits_sz);
  DYNALLSTAT(int, map, map_sz);
  DYNALLSTAT(graph, g1, g1_sz);
  DYNALLSTAT(graph, g2, g2_sz);
  DYNALLSTAT(graph, g3, g3_sz);
  DYNALLSTAT(graph, cg1, cg1_sz);
  DYNALLSTAT(graph, cg2, cg2_sz);
  DYNALLSTAT(graph, cg3, cg3_sz);
  DYNALLSTAT(graph, ccg3, ccg3_sz);
  static DEFAULTOPTIONS_GRAPH(options);
  statsblk stats;
  int size, st, sl, n, m, i;
  size_t k;
  /* Select option for canonical labelling */
  options.getcanon = TRUE;

  size = nb_states * nb_letters;
  st = size + nb_states;
  sl = st + nb_letters;
  n = st + 3;
  m = SETWORDSNEEDED(n);

  nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
  DYNALLOC1(int, lab1, lab1_sz, n, "malloc");
  DYNALLOC1(int, lab2, lab2_sz, n, "malloc");
  DYNALLOC1(int, lab3, lab3_sz, n, "malloc");
  DYNALLOC1(int, ptn, ptn_sz, n, "malloc");
  DYNALLOC1(int, orbits, orbits_sz, n, "malloc");
  DYNALLOC1(int, map, map_sz, n, "malloc");

  printf("Make first graph\n");
  /* Now make the first graph */
  DYNALLOC2(graph, g1, g1_sz, n, m, "malloc");

  EMPTYGRAPH(g1, m, n);

  ADDONEEDGE(g1, sl + 1, sl + 2, m);

  for (int x = 0; x < nb_letters; x++) {
    ADDONEEDGE(g1, st + x, sl + 1, m);
  }

  for (int p = 0; p < nb_states; p++) {
    ADDONEEDGE(g1, size + p, sl, m);
    for (int x = 0; x < nb_letters; x++) {
      int index = p * nb_letters + x;
      ADDONEEDGE(g1, index, delta1[index] * nb_letters + rho1[index], m);
      ADDONEEDGE(g1, index, size + p, m);
      ADDONEEDGE(g1, index, st + x, m);
    }
  }

  printf(("Make second graph\n"));
  /* Now make the second graph */
  DYNALLOC2(graph, g2, g2_sz, n, m, "malloc");
  EMPTYGRAPH(g2, m, n);

  ADDONEEDGE(g2, sl + 1, sl + 2, m);

  for (int x = 0; x < nb_letters; x++) {
    ADDONEEDGE(g2, st + x, sl + 1, m);
  }

  for (int p = 0; p < nb_states; p++) {
    ADDONEEDGE(g2, size + p, sl, m);
    for (int x = 0; x < nb_letters; x++) {
      int index = p * nb_letters + x;
      ADDONEEDGE(g2, index, delta2[index] * nb_letters + rho2[index], m);
      ADDONEEDGE(g2, index, size + p, m);
      ADDONEEDGE(g2, index, st + x, m);
    }
  }

  printf(("Make canonical graphs\n"));
  DYNALLOC2(graph, cg1, cg1_sz, n, m, "malloc");
  DYNALLOC2(graph, cg2, cg2_sz, n, m, "malloc");
  densenauty(g1, lab1, ptn, orbits, &options, &stats, m, n, cg1);
  densenauty(g2, lab2, ptn, orbits, &options, &stats, m, n, cg2);
  /* Compare canonically labelled graphs */
  for (k = 0; k < m * (size_t)n; ++k)
    if (cg1[k] != cg2[k])
      break;
  if (k == m * (size_t)n) {
    printf("Isomorphic.\n");
    if (n <= 1000) {
      /* Write the isomorphism. For each i, vertex lab1[i]
      of sg1 maps onto vertex lab2[i] of sg2. We compute
      the map in order of labelling because it looks better. */
      for (i = 0; i < n; ++i)
        map[lab1[i]] = lab2[i];
      for (i = 0; i < n; ++i)
        printf(" %d-%d", i, map[i]);
      printf("\n");
    }
  } else
    printf("Not isomorphic.\n");

  printf("Make third graph\n");
  /* Now make the third graph */
  DYNALLOC2(graph, g3, g3_sz, n, m, "malloc");

  EMPTYGRAPH(g3, m, n);

  ADDONEEDGE(g3, sl + 1, sl + 2, m);

  for (int x = 0; x < nb_letters; x++) {
    ADDONEEDGE(g3, st + x, sl + 1, m);
  }

  for (int p = 0; p < nb_states; p++) {
    ADDONEEDGE(g3, size + p, sl, m);
    for (int x = 0; x < nb_letters; x++) {
      int index = p * nb_letters + x;
      ADDONEEDGE(g3, index, delta3[index] * nb_letters + rho3[index], m);
      ADDONEEDGE(g3, index, size + p, m);
      ADDONEEDGE(g3, index, st + x, m);
    }
  }

  printf(("Make canonical graphs\n"));
  DYNALLOC2(graph, cg3, cg3_sz, n, m, "malloc");
  DYNALLOC2(graph, ccg3, ccg3_sz, n, m, "malloc");
  densenauty(g3, lab3, ptn, orbits, &options, &stats, m, n, cg3);
  
  for (k = 0; k < m * (size_t)n; ++k)
    if (g3[k] != cg3[k])
      break;
  if (k == m * (size_t)n) {
    printf("Isomorphic.\n");
  } else
    printf("Not isomorphic.\n");
}