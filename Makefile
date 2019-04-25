LATEX = pdflatex
BIB = bibtex
CC = gcc
FLAGS = -O3
LIBS = -I nauty26r11 -L nauty26r11
DEPS = nauty26r11/nauty.c nauty26r11/nautil.c nauty26r11/naugraph.c nauty26r11/schreier.c nauty26r11/naurng.c

all: prettyprint generator

generator: generator.c 
	@echo "Generate executable generator"
	@$(CC) $(FLAGS) $(LIBS) generator.c $(DEPS) -o generator

prettyprint: prettyprint.c
	@echo "Generate executable prettyprint"
	@$(CC) $(FLAGS) $(LIBS) prettyprint.c $(DEPS) -o prettyprint

article:
	@echo "Compiling article to latex"
	@$(LATEX) project
	@$(BIB) project
	@$(LATEX) project

clean:
	@echo "Clean executable"
	@rm -rf generator prettyprint

re: clean all
