/**
 * \file
 * Implementation of the reading functions.
 *
 * The API currently implements two versions of the reading function: a serial,
 * and a parallel one.
 */
#include "read.h"
#include "atom.h"
#include "bond.h"
#include "box.h"
#include "trajectory.h"
#include "utils.h"

#include <errno.h>
#include <omp.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void read_current_step(FILE *input, unsigned long *current_step)
{
    char dump[BUFFER_LIMIT];
    long pos = ftell(input);
    while (fscanf(input, "ITEM: TIMESTEP %lu", current_step) != 1)
        if (fgets(dump, BUFFER_LIMIT, input) == NULL)
        {
            errno = EIO;
            perror("Error while skipping a line (read_current_step)");
            return;
        }
    fseek(input, pos, SEEK_SET);
}

void read_dump_format(FILE *input, char dump_format[BUFFER_LIMIT])
{
    char line[BUFFER_LIMIT];

    long pos = ftell(input);
    do
        if (fgets(line, BUFFER_LIMIT, input) == NULL)
        {
            errno = EIO;
            perror("Error while skipping a line (read_dump_format)");
            return;
        }
    while (strncmp(line, "ITEM: ATOMS", DUMP_FORMAT_OFFSET - 1) != 0);

    strncpy(dump_format, line + DUMP_FORMAT_OFFSET, BUFFER_LIMIT);
    string_remove_newlines(dump_format, '\0');
    fseek(input, pos, SEEK_SET);
}

#define HEADER_N_LINES 9

void read_parameters(FILE **input, const char dump_format[BUFFER_LIMIT], unsigned int *timestep, unsigned int *N_atoms, struct Box *box)
{
    char lines[HEADER_N_LINES][BUFFER_LIMIT] = {0};
    for (unsigned int l = 0; l < HEADER_N_LINES; l++)
        if (fgets(lines[l], BUFFER_LIMIT, *input) == NULL)
        {
            perror("Error while reading the header lines");
            return;
        }

    // Hard-coded but straighforward and parallelizable
    if (sscanf(lines[1], "%u\n", timestep) != 1)
    {
        errno = EINVAL;
        perror("Error while scanning the current timestep");
        return;
    }

    if (sscanf(lines[3], "%u\n", N_atoms) != 1)
    {
        errno = EINVAL;
        perror("Error while scanning the number of atoms");
        return;
    }

    if (sscanf(lines[4], "ITEM: BOX BOUNDS %" BOX_FLAG_SCANF_LIMIT "c\n", box->flag) != 1)
    {
        errno = EINVAL;
        perror("Error while scanning the box flags");
        return;
    }

    for (unsigned int b = 0; b < BOX_BOUNDS_LIMIT / 2; b++)
    {
        char *line = lines[5 + b];
        if (sscanf(line, "%lf %lf\n", box->bounds + 2 * b, box->bounds + 2 * b + 1) != 2)
        {
            errno = EINVAL;
            perror("Error while scanning box bounds");
            return;
        }
    }

    if (strncmp(lines[8] + DUMP_FORMAT_OFFSET, dump_format, strlen(dump_format)) != 0)
    {
        errno = EINVAL;
        perror("Error while checking the dump format");
        return;
    }
}

void read_atoms(FILE **input, const struct AtomBuilder atom_builder, const unsigned int N_atoms, struct Atom *atoms,
                union AtomField *additional_fields)
{
    // Preparing the buffer
    char *buffer = calloc(BUFFER_LIMIT * N_atoms, sizeof(char));
    if (buffer == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (read_atoms)");
        return;
    }
    for (unsigned int a = 0; a < N_atoms; a++)  // Copying all the atoms entries to the buffer
        if (fgets(buffer + a * BUFFER_LIMIT, BUFFER_LIMIT, *input) == NULL)
        {
            free(buffer);
            errno = EINVAL;
            perror("Error while copying a line to the buffer (read_atoms)");
            return;
        }

    // Parsing the atoms
    int err = 0;
#pragma omp parallel for
    for (unsigned int a = 0; a < N_atoms; a++)
    {
        if (err) continue;
        atom_read_entry(atoms + a, atom_builder, buffer + a * BUFFER_LIMIT, additional_fields + atom_builder.N_additional * a);
        if (errno != 0)  // Something went wrong
#pragma omp critical
            err = errno;
    }

    free(buffer);

    if (err)  // An error occurred
    {
        errno = err;
        for (unsigned int a = 0; a < N_atoms; a++) atom_delete(atoms + a);
        perror("Error while reading an atom entry (read_atoms.atom_read_entry)");
        return;
    }
}

void trajectory_read(const char *file_name, const unsigned long start, const char *user_format, struct Trajectory *trajectory)
{
    // To store the error value
    int errsv;

    // Opening the file
    FILE *input = fopen(file_name, "r");
    if (input == NULL)  // File could not be open
    {
        errno = EIO;
        perror("Error while opening the file (trajectory_read)");
        return;
    }

    // Skipping the first configurations
    trajectory_skip(&input, start);
    if (errno != 0)  // Something went wrong
    {
        perror("Error while skipping configurations (trajectory_read)");
        fclose(input);
        return;
    }

    // Getting the current step
    unsigned long current_step;
    read_current_step(input, &current_step);
    if (errno != 0)  // Could not read the current timestep
    {
        errsv = errno;
        fclose(input);
        errno = errsv;
        perror("Error while reading the current step (trajectory_read)");
        return;
    }

    // Getting the dump format
    char dump_format[BUFFER_LIMIT];
    if (user_format == NULL)
    {
        read_dump_format(input, dump_format);
        if (errno != 0)  // Could not read the dump format
        {
            errsv = errno;
            fclose(input);
            errno = errsv;
            perror("Error while reading the dump format (trajectory_read)");
            return;
        }
    }
    else
    {
        strncpy(dump_format, user_format, BUFFER_LIMIT);
        dump_format[BUFFER_LIMIT - 1] = '\0';
        string_remove_newlines(dump_format, '\0');
    }

    // Initializing the atom builder
    struct AtomBuilder atom_builder = atom_builder_new(dump_format, input);
    if (errno != 0)  // Something went wrong
    {
        perror("Error while creating the atom builder (trajectory_read)");
        fclose(input);
        return;
    }

    // Preparing the arrays
    unsigned int *N_atoms = malloc(BASE_N_CONFIGURATIONS * sizeof(unsigned int));
    if (N_atoms == NULL)  // Allocation failed
    {
        atom_builder_delete(&atom_builder);
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_read.N_atoms)");
        return;
    }
    unsigned int *steps = malloc(BASE_N_CONFIGURATIONS * sizeof(unsigned int));
    if (steps == NULL)
    {
        free(N_atoms);
        atom_builder_delete(&atom_builder);
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_read.steps)");
        return;
    }
    struct Box *boxes = malloc(BASE_N_CONFIGURATIONS * sizeof(struct Box));
    if (boxes == NULL)  // Allocation failed
    {
        free(steps);
        free(N_atoms);
        atom_builder_delete(&atom_builder);
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_read.boxes)");
        return;
    }
    unsigned long boxes_size = BASE_N_CONFIGURATIONS;
    struct Atom *atoms = NULL;
    union AtomField *additional_fields = NULL;
    unsigned long atoms_size = 0;

    // Preparing the variables
    unsigned long N_configurations = 0;
    unsigned long total_atoms = 0;  // To keep track of the number of atoms read

    // Reading
    int chr = fgetc(input);
    while (chr != EOF)
    {
        ungetc(chr, input);

        // Reallocating memory
        if (N_configurations == boxes_size)
        {
            unsigned int *new_N_atoms = realloc(N_atoms, (boxes_size + N_CONFIGURATIONS_INCR) * sizeof(unsigned int));
            if (new_N_atoms == NULL)  // Could not realloc memory
            {
                for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
                if (additional_fields != NULL) free(additional_fields);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory "
                    "(trajectory_read.N_atoms)");
                return;
            }
            N_atoms = new_N_atoms;

            unsigned int *new_steps = realloc(steps, (boxes_size + N_CONFIGURATIONS_INCR) * sizeof(unsigned int));
            if (new_steps == NULL)  // Could not realloc memory
            {
                for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
                if (additional_fields != NULL) free(additional_fields);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                errno = ENOMEM;
                perror("Error while reallocating memory (trajectory_read.steps)");
                return;
            }
            steps = new_steps;

            struct Box *new_boxes = realloc(boxes, (boxes_size + N_CONFIGURATIONS_INCR) * sizeof(struct Box));
            if (new_boxes == NULL)  // Could not realloc memory
            {
                for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
                if (additional_fields != NULL) free(additional_fields);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                errno = ENOMEM;
                perror("Error while reallocating memory (trajectory_read.boxes)");
                return;
            }
            boxes = new_boxes;

            boxes_size += N_CONFIGURATIONS_INCR;
        }

        read_parameters(&input, dump_format, steps + N_configurations, N_atoms + N_configurations, boxes + N_configurations);
        if (errno != 0)  // Could not read parameters
        {
            errsv = errno;
            for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
            if (additional_fields != NULL) free(additional_fields);
            if (atoms != NULL) free(atoms);
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            errno = errsv;
            perror("Error while reading the configuration parameters (trajectory_read)");
            return;
        }

        // Reallocating memory
        {
            struct Atom *new_atoms = realloc(atoms, (atoms_size + N_atoms[N_configurations]) * sizeof(struct Atom));
            if (new_atoms == NULL)
            {
                for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
                if (additional_fields != NULL) free(additional_fields);
                if (atoms != NULL) free(atoms);
                free(N_atoms);
                free(steps);
                free(boxes);
                atom_builder_delete(&atom_builder);
                fclose(input);
                errno = ENOMEM;
                perror("Error while reallocating memory (trajectory_read.atoms)");
                return;
            }
            atoms = new_atoms;

            if (atom_builder.N_additional > 0)
            {
                union AtomField *new_additional_fields = realloc(
                    additional_fields, (atoms_size + N_atoms[N_configurations]) * atom_builder.N_additional * sizeof(union AtomField));
                if (new_additional_fields == NULL)
                {
                    for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
                    if (additional_fields != NULL) free(additional_fields);
                    if (atoms != NULL) free(atoms);
                    free(N_atoms);
                    free(steps);
                    free(boxes);
                    atom_builder_delete(&atom_builder);
                    fclose(input);
                    errno = ENOMEM;
                    perror("Error while reallocating memory (trajectory_read.atoms)");
                    return;
                }
                additional_fields = new_additional_fields;
            }

            atoms_size += N_atoms[N_configurations];
        }

        read_atoms(&input, atom_builder, N_atoms[N_configurations], atoms + total_atoms,
                   additional_fields + atom_builder.N_additional * total_atoms);
        if (errno != 0)  // Could not read the atoms
        {
            errsv = errno;
            for (unsigned int at = 0; at <= total_atoms; at++) atom_delete(atoms + at);
            if (additional_fields != NULL) free(additional_fields);
            if (atoms != NULL) free(atoms);
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            errno = errsv;
            perror("Error while reading the atoms of the configuration (trajectory_read)");
            return;
        }
        total_atoms += N_atoms[N_configurations];

        N_configurations++;
        chr = fgetc(input);
    }

    fclose(input);

    // Copying the additional fields
    if (atom_builder.N_additional > 0)
    {
#pragma omp parallel for
        for (unsigned long a = 0; a < total_atoms; a++) atoms[a].additionnal_fields = additional_fields + a * atom_builder.N_additional;
    }

    // Storing the data
    trajectory_init(trajectory, atom_builder, N_configurations, steps, N_atoms, boxes, atoms, additional_fields);
}

#define REAXFF_BONDS_HEADER_LINES 7

void trajectory_read_bonds(const char *file_name, enum BondMode mode, struct Trajectory *trajectory)
{
    // Initializing the bond builder
    struct BondBuilder bond_builder = bondbuilder_new(file_name, mode, BS_REAXFF, (struct BondTable){0});

    // Openging the file
    FILE *input = fopen(bond_builder.file_name, "r");
    if (input == NULL)
    {
        perror("Error while opening the file (trajectory_read_bonds)");
        return;
    }

    // Skipping the first configurations
    unsigned long current_step = 0;
    unsigned long start = trajectory->steps[0];
    char line[BUFFER_LIMIT] = {0};
    do
    {
        // Read a line
        if (fgets(line, BUFFER_LIMIT, input) == NULL)  // Could not read a line
        {
            fclose(input);
            errno = EIO;
            perror("Error while skipping a line (trajectory_read_bonds)");
            return;
        }

        if (strncmp(line, "# Timestep", 10) == 0)
        {
            if (sscanf(line, "# Timestep %ld", &current_step) != 1)
            {
                fclose(input);
                errno = EINVAL;
                perror("Error while reading a step (trajectory_read_bonds)");
                return;
            }
            else if (current_step == start)
                break;
        }
    } while (!feof(input));

    // Skipping to the first configuration
    for (unsigned int l = 0; l < REAXFF_BONDS_HEADER_LINES - 1; l++)
        if (fgets(line, BUFFER_LIMIT, input) == NULL)  // Could not read a line
        {
            fclose(input);
            errno = EIO;
            perror("Error while skipping the first header lines (trajectory_read_bonds)");
            return;
        }

    // Reading the bonds
    // The file is already aligned with the atoms
    unsigned long at = 0;
    for (unsigned int c = 0; c < trajectory->N_configurations; c++)
    {
        // Reading all the lines of the configuration
        char *buffer = calloc(BUFFER_LIMIT * (trajectory->N_atoms)[c], sizeof(char));
        if (buffer == NULL)  // Could not allocate memory
        {
            fclose(input);
            errno = ENOMEM;
            perror("Error while allocating memory (trajectory_read_bonds)");
            return;
        }
        for (unsigned int a = 0; a < trajectory->N_atoms[c]; a++)
            if (fgets(buffer + a * BUFFER_LIMIT, BUFFER_LIMIT, input) == NULL)
            {
                free(buffer);
                fclose(input);
                errno = EIO;
                perror("Error while reading a bond entry (trajectory_read_bonds)");
                return;
            }

        // Dumping the last line of the configuration
        if (fgets(line, BUFFER_LIMIT, input) == NULL)
        {
            free(buffer);
            fclose(input);
            errno = EIO;
            perror("Error while dumping a line (trajectory_read_bonds)");
            return;
        }

        // Parse the bond entries
        int skip = 0;
        struct Atom *atoms = trajectory->atoms + at;
#pragma omp parallel for
        for (unsigned int a = 0; a < trajectory->N_atoms[c]; a++)
        {
            if (skip) continue;
            bondbuilder_read_bond_entry(bond_builder, buffer + a * BUFFER_LIMIT, atoms + a);
            if (errno != 0)
#pragma omp critical
                skip = errno;
        }

        if (skip)
        {
            free(buffer);
            fclose(input);
            errno = skip;
            perror("Error while reading a bond entry (trajectory_read_bonds)");
            return;
        }

        at += trajectory->N_atoms[c];
        free(buffer);

        // Skipping to the next configuration
        for (unsigned int l = 0; l < REAXFF_BONDS_HEADER_LINES; l++)
        {
            if (fgets(line, BUFFER_LIMIT, input) == NULL && !feof(input))
            {
                fclose(input);
                errno = EIO;
                perror("Error while dumping the header (trajectory_read_bonds)");
                return;
            }
        }
    }

    fclose(input);

    // Saving the bond builder data
    bondbuilder_copy(bond_builder, &(trajectory->bond_builder));
}

void trajectoryfile_read_slice(struct TrajectoryFile trajectory_file, unsigned long start, unsigned long N_configurations,
                               struct Trajectory *trajectory)
{
    // To store an error value
    int errsv;

    // Opening the file
    FILE *input = fopen(trajectory_file.file_name, "r");
    if (input == NULL)
    {
        errno = EIO;
        perror("Error while opening the trajectory file (trajectoryfile_read)");
        return;
    }

    // Moving to the right configuration
    long pos = 0;
    for (unsigned int c = 0; c < trajectory_file.N_configurations; c++)
        if (trajectory_file.steps[c] >= start)
        {
            pos = trajectory_file.conf_pos[c];
            break;
        }
    fseek(input, pos, SEEK_SET);

    // Getting the dump format
    char dump_format[BUFFER_LIMIT];
    if (trajectory_file.user_format[0] == '\0')
    {
        read_dump_format(input, dump_format);
        if (errno != 0)
        {
            errsv = errno;
            fclose(input);
            errno = errsv;
            perror("Error while reading the dump format");
            return;
        }
    }
    else
    {
        strncpy(dump_format, trajectory_file.user_format, BUFFER_LIMIT);
        string_remove_newlines(dump_format, '\0');
    }

    // Initializing the atom builder
    struct AtomBuilder atom_builder = atom_builder_new(dump_format, input);
    if (errno != 0)  // Something went wrong
    {
        perror("Error while creating the atom builder (trajectoryfile_read)");
        fclose(input);
        return;
    }

    // Preparing the arrays
    unsigned int *N_atoms = malloc(N_configurations * sizeof(unsigned int));
    if (N_atoms == NULL)  // Allocation failed
    {
        atom_builder_delete(&atom_builder);
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectoryfile_read.N_atoms)");
        return;
    }
    unsigned int *steps = malloc(N_configurations * sizeof(unsigned int));
    if (steps == NULL)
    {
        free(N_atoms);
        atom_builder_delete(&atom_builder);
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectoryfile_read.steps)");
        return;
    }
    struct Box *boxes = malloc(N_configurations * sizeof(struct Box));
    if (boxes == NULL)  // Allocation failed
    {
        free(steps);
        free(N_atoms);
        atom_builder_delete(&atom_builder);
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectoryfile_read.boxes)");
        return;
    }
    struct Atom *atoms = NULL;
    union AtomField *additional_fields = NULL;
    unsigned long atoms_size = 0;

    // Preparing the variables
    unsigned long n_configurations = 0;
    unsigned long total_atoms = 0;  // To keep track of the number of atoms read

    // Reading
    int chr = fgetc(input);
    while (chr != EOF && n_configurations < N_configurations)
    {
        ungetc(chr, input);

        // Reading the parameters: `N_atoms`, `box.flags`, `box.bounds`
        read_parameters(&input, dump_format, steps + n_configurations, N_atoms + n_configurations, boxes + n_configurations);
        if (errno != 0)  // Could not read parameters
        {
            errsv = errno;
            if (atoms != NULL)
            {
                for (unsigned int a = 0; a < total_atoms; a++) atom_delete(atoms + a);
                free(atoms);
            }
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            errno = errsv;
            perror(
                "Error while reading the configuration parameters "
                "(trajectoryfile_read)");
            return;
        }

        // Reallocating memory for the atoms
        {
            // Allocating the new block of memory
            struct Atom *new_atoms = realloc(atoms, (atoms_size + N_atoms[n_configurations]) * sizeof(struct Atom));
            if (new_atoms == NULL)  // Reallocation failed
            {
                if (atoms != NULL)
                {
                    for (unsigned int a = 0; a < total_atoms; a++)  // Freeing all the atoms read so far
                        atom_delete(atoms + a);
                    free(additional_fields);
                    free(atoms);
                }
                free(N_atoms);
                free(steps);
                free(boxes);
                atom_builder_delete(&atom_builder);
                fclose(input);
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory "
                    "(trajectoryfile_read.atoms)");
                return;
            }
            atoms = new_atoms;

            union AtomField *new_additional_fields =
                realloc(additional_fields, (atoms_size + N_atoms[n_configurations]) * atom_builder.N_additional * sizeof(union AtomField));
            if (new_additional_fields == NULL)
            {
                if (atoms != NULL)
                {
                    for (unsigned int a = 0; a < total_atoms; a++)  // Freeing all the atoms read so far
                        atom_delete(atoms + a);
                    free(additional_fields);
                    free(atoms);
                }
                free(N_atoms);
                free(steps);
                free(boxes);
                atom_builder_delete(&atom_builder);
                fclose(input);
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory "
                    "(trajectoryfile_read.atoms)");
                return;
            }
            additional_fields = new_additional_fields;

            atoms_size += N_atoms[n_configurations];
        }

        // Reading the atoms
        read_atoms(&input, atom_builder, N_atoms[n_configurations], atoms + total_atoms,
                   additional_fields + atom_builder.N_additional * total_atoms);
        if (errno != 0)  // Could not read the atoms
        {
            errsv = errno;
            if (atoms != NULL)
            {
                for (unsigned int at = 0; at < total_atoms; at++) atom_delete(atoms + at);
                free(additional_fields);
                free(atoms);
            }
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            errno = errsv;
            perror(
                "Error while reading the atoms of the configuration "
                "(trajectoryfile_read)");
            return;
        }
        total_atoms += N_atoms[n_configurations];

        n_configurations++;
        chr = fgetc(input);
    }

    fclose(input);
    trajectory_init(trajectory, atom_builder, N_configurations, steps, N_atoms, boxes, atoms, additional_fields);
    for (unsigned int s = 0; s < trajectory_file.N_selections; s++)
    {
        trajectory_select(trajectory, trajectory_file.selections[s], true, NULL);
        if (errno != 0)  // Could not select atoms
        {
            trajectory_delete(trajectory);
            trajectoryfile_delete(&trajectory_file);
            perror("Error while selecting atoms (trajectoryfile_read_slice)");
            return;
        }
    }
}
