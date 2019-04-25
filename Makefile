LATEX = pdflatex
BIB = bibtex
CC = gcc
FLAGS = -O3 -g
LIBS = -I nauty26r11 -L nauty26r11
DEPS = nauty26r11/nauty.c nauty26r11/nautil.c nauty26r11/naugraph.c nauty26r11/schreier.c nauty26r11/naurng.c

all: prettyprint generator

%.o: %.c
	@echo "Compiling $?"
	@$(CC) $(FLAGS) -c $? -o $@ $(LIBS)

generator: generator_struct.o utils.o generator.c
	@echo "Generate executable generator"
	@$(CC) $(FLAGS) generator_struct.o utils.o $(DEPS) generator.c -o generator $(LIBS)

prettyprint: utils.o prettyprint.c
	@echo "Generate executable prettyprint"
	@$(CC) $(FLAGS) $? $(DEPS) -o prettyprint $(LIBS)

article:
	@echo "Compiling article to latex"
	@$(LATEX) project
	@$(BIB) project
	@$(LATEX) project

clean:
	@echo "Clean executable"
	@rm -rf generator prettyprint *.o

re: clean all
