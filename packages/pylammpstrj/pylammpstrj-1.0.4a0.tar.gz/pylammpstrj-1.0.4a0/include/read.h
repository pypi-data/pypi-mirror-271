#ifndef _READ_H
#define _READ_H

#include "atom.h"
#include "box.h"
#include "utils.h"

#include <stdio.h>

/** The base number of configurations for memory allocation. */
#define BASE_N_CONFIGURATIONS 100

/** The number of configurations increment for memory allocation. */
#define N_CONFIGURATIONS_INCR 100

/** The number of characters to skip in the header line to obtain the dump format. */
#define DUMP_FORMAT_OFFSET 12

void read_current_step(FILE *input, unsigned long *current_step);

void read_dump_format(FILE *input, char dump_format[BUFFER_LIMIT]);

void read_parameters(FILE **input, const char dump_format[BUFFER_LIMIT], unsigned int *timestep, unsigned int *N_atoms, struct Box *box);

void read_atoms(FILE **input, const struct AtomBuilder atom_builder, const unsigned int N_atoms, struct Atom *atoms, union AtomField *additional_fields);

#endif
