#include "box.h"
#include "utils.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void trajectory_skip(FILE **input, const unsigned long start)
{
    unsigned long current_step = 0;
    long starting_pos;
    unsigned int N_atoms;
    char dump[BUFFER_LIMIT];

    // Skipping the first configurations
    do
    {
        starting_pos = ftell(*input);

        // Reading the current timestep and number of atoms
        if (fscanf(*input,
                   "ITEM: TIMESTEP %lu ITEM: NUMBER OF ATOMS %u ITEM: BOX "
                   "BOUNDS %*" BOX_FLAG_SCANF_LIMIT "c\n",
                   &current_step, &N_atoms) != 2)
        {
            errno = EINVAL;
            if (feof(*input))
                perror("Error reached end of file (trajectory_skip)");
            else
                perror("Error while scanning a line (trajectory_skip)");
            return;
        }

        for (unsigned int b = 0; b < BOX_BOUNDS_LIMIT / 2; b++)
            if (fgets(dump, BUFFER_LIMIT, *input) == NULL)
            {
                errno = EIO;
                perror("Error while skipping the box bounds (trajectory_skip)");
                return;
            }

        if (fgets(dump, BUFFER_LIMIT, *input) == NULL)
        {
            errno = EIO;
            perror("Error while skipping the dumping format (trajectory_skip)");
            return;
        }

        if (current_step >= start)
        {
            // Returning to the start position
            fseek(*input, starting_pos, SEEK_SET);
            break;
        }

        // Skipping the atom entries
        for (unsigned int a = 0; a < N_atoms; a++)
        {
            if (fgets(dump, BUFFER_LIMIT, *input) == NULL)
            {
                errno = EIO;
                perror("Error while dumping an atom entry");
                return;
            }
        }

    } while (current_step < start);
}
