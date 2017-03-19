CC=g++
LIBSOCKET=-lnsl
CCFLAGS=-Wall -g
CLT=client

build: $(CLT)

$(CLT):	$(CLT).cpp
	$(CC)  $(CCFLAGS) -o $(CLT) $(LIBSOCKET) $(CLT).cpp

clean:
	rm -f  $(CLT)
