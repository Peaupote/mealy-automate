CC = gcc
FLAGS = -O3 -g -Wall
SRC = C
LIBS = -I nauty26r11 -L nauty26r11
DEPS = nauty26r11/nauty.o nauty26r11/nautil.o \
		nauty26r11/naugraph.o nauty26r11/schreier.o \
		nauty26r11/naurng.o nauty26r11/nautinv.o
DEPS_SPARSE = nauty26r11/nautil.o nauty26r11/nausparse.o \
				nauty26r11/naugraph.o nauty26r11/schreier.o \
				nauty26r11/naurng.o nauty26r11/nauty.o

all: prettyprint generator generator_sparse

$(SRC)/%.o: $(SRC)/%.c
	@echo "Compiling $?"
	@$(CC) $(FLAGS) -c $? -o $@ $(LIBS)

generator: $(SRC)/utils.o $(SRC)/generator.o
	@echo "Generate executable generator"
	@$(CC) $(FLAGS) $(SRC)/utils.o $(DEPS) $(SRC)/generator.o -o generator $(LIBS)

generator_sparse: $(SRC)/utils.o $(SRC)/generator_sparse.o
	@echo "Compiling excutable generator_sparse"
	@$(CC) $(FLAGS) $(SRC)/utils.o $(DEPS_SPARSE) \
		$(SRC)/generator_sparse.o -o generator_sparse $(LIBS)

prettyprint: $(SRC)/utils.o $(SRC)/frags.o $(SRC)/prettyprint.o
	@echo "Generate executable prettyprint"
	@$(CC) $(FLAGS) $(SRC)/utils.o $(SRC)/frags.o $(DEPS) $(SRC)/prettyprint.o -o prettyprint $(LIBS)

report:
	$(MAKE) -C rapport

clean:
	@echo "Clean executable"
	@rm -rf generator prettyprint generator_sparse $(SRC)/*.o

re: clean all
