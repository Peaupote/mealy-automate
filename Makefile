FILES = generator.c
OBJ = $(FILES:%.c=%.o)

CC = gcc
FLAGS = -O3
LIBS = -I nauty26r11 -L nauty26r11
DEPS = nauty26r11/nauty.c nauty26r11/nautil.c nauty26r11/naugraph.c nauty26r11/schreier.c nauty26r11/naurng.c

%.o: %.c
	@echo "Compiling $?"
	@$(CC) $(FLAGS) -c $? -o $@ $(LIBS)

generator: $(OBJ)
	@echo "Generate executable generator"
	@$(CC) $(FLAGS) $(LIBS) $(OBJ) $(DEPS) -o generator

all: generator

clean:
	@echo "Clean object files"
	@rm -rf $(OBJ)

fclean: clean
	@echo "Clean executable"
	@rm -rf generator

re: fclean all
