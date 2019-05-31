CC = gcc
FLAGS = -O3 -g -Wall
LIBS = -I nauty26r11 -L nauty26r11
DEPS = nauty26r11/nauty.o nauty26r11/nautil.o \
		nauty26r11/naugraph.o nauty26r11/schreier.o \
		nauty26r11/naurng.o nauty26r11/nautinv.o
DEPS_SPARSE = nauty26r11/nautil.o nauty26r11/nausparse.o \
				nauty26r11/naugraph.o nauty26r11/schreier.o \
				nauty26r11/naurng.o nauty26r11/nauty.o

all: prettyprint generator generator_sparse

%.o: %.c
	@echo "Compiling $?"
	@$(CC) $(FLAGS) -c $? -o $@ $(LIBS)

generator: utils.o generator.o
	@echo "Generate executable generator"
	@$(CC) $(FLAGS) utils.o $(DEPS) generator.o -o generator $(LIBS)

generator_sparse: utils.o generator_sparse.o
	@echo "Compiling excutable generator_sparse"
	@$(CC) $(FLAGS) utils.o $(DEPS_SPARSE) \
		generator_sparse.o -o generator_sparse $(LIBS)

prettyprint: utils.o frags.o prettyprint.o
	@echo "Generate executable prettyprint"
	@$(CC) $(FLAGS) utils.o frags.o $(DEPS) prettyprint.o -o prettyprint $(LIBS)

report:
	$(MAKE) -C rapport

clean:
	@echo "Clean executable"
	@rm -rf generator prettyprint *.o

re: clean all
