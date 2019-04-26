Mealy automate
==============

## Installation

### Dépendances
La seule dépendance du projet est à la blibliothèque de graphe `nauty`.
Lancer le script `installnauty.sh` pour installer nauty dans le projet.

```
$ sh installnauty.sh
```

### Compilation
Un makefile est mis à disposition pour compiler le projet.

* `make generator` compile un executable `generator` qui génère les automates
```sh
$ generator
    -s n
        nombre d'état. Par défault 2.
    -l n
        nombre de lettres. Par défault 2.
    -n
        calcule les classe d'isomorphisme avec nauty si présent. Par défault absent.
    -f n
        profondeur des forks dans la génération. Le nombre de fork est (s * l)^f
    -o file
        fichier de sortie. Les deux premiers octets du fichier sont, dans cet ordre,
        le nombre d'états puis le nombre de lettres. Les automates biréversibles sont
        stocké dans le fichier dans un ordre quelconque au format

                    <---- s * l octets ----><---- s * l octets ---->
        +-----+-----+----------------------+-----------------------+------                    --+
        |  s  |  l  |        delta         |          rho          |   automates suivant ...    |
        +-----+-----+----------------------+-----------------------+-----                     --+
```

* `make prettyprinter` compile un executable `prettyprinter` qui prend un argument
  un fichier généré par `generator` à analyser.

* `make report` compile le fichier `project.tex`
