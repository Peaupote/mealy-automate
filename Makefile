LATEX = pdflatex
BIB = bibtex
CC = gcc
FLAGS = -O3 -g
LIBS = -I nauty26r11 -L nauty26r11
DEPS = nauty26r11/nauty.c nauty26r11/nautil.c nauty26r11/naugraph.c nauty26r11/schreier.c nauty26r11/naurng.c
DEPS_SPARSE = nauty26r11/nausparce.o

all: prettyprint generator

%.o: %.c
	@echo "Compiling $?"
	@$(CC) $(FLAGS) -c $? -o $@ $(LIBS)

generator: utils.o generator.o
	@echo "Generate executable generator"
	@$(CC) $(FLAGS) utils.o $(DEPS) generator.o -o generator $(LIBS)

prettyprint: utils.o prettyprint.o
	@echo "Generate executable prettyprint"
	@$(CC) $(FLAGS) utils.o $(DEPS) prettyprint.o -o prettyprint $(LIBS)

report: rapport/project.tex rapport/project.bib
	@echo "Compiling latex report"
	@$(LATEX) rapport/project
	@$(BIB) rapport/project
	@$(LATEX) rapport/project

clean:
	@echo "Clean executable"
	@rm -rf generator prettyprint *.o

re: clean all
