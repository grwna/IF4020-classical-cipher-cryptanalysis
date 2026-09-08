CC ?= cc
CFLAGS ?= -O3 -std=c17 -Wall -Wextra -Wpedantic
CPPFLAGS ?= -Iheaders

.PHONY: all clean
all: machine encode
machine: machine.c enigma.c headers/enigma.h headers/rotor.h headers/plugboard.h headers/reflector.h
	$(CC) $(CPPFLAGS) $(CFLAGS) machine.c enigma.c rotor.c plugboard.c reflector.c -o $@
encode: encode.c
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm -f machine encode