EXE = a.out 
OBJS = helloworld.cpp
CC = g++ 
CFLAGS = -lm -lpthread

$(EXE): $(OBJS)
	$(CC) -g -o $@ $^ $(CFLAGS)
clean: 
	rm -rf *.o $(EXE)