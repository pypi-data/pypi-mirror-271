#include "bond.h"
#include "atom.h"
#include "box.h"
#include "trajectory.h"
#include "utils.h"

#include <errno.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct BondTable bondtable_new(const unsigned int N_entries, ...)
{
    // Initializing the bond table
    struct BondTable table = {0};
    struct BondTableEntry *entries = calloc(N_entries, sizeof(struct BondTableEntry));
    if (entries == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (bondtable_new.entries)");
        return table;
    }

    // Parsing the arguments
    va_list args;
    va_start(args, N_entries);
    for (unsigned int e = 0; e < N_entries; e++) entries[e] = va_arg(args, struct BondTableEntry);
    va_end(args);

    // Transfering the data
    table.N_entries = N_entries;
    table.entries = entries;
    return table;
}

double bondtable_get_length_from_types(const struct BondTable table, const void *t1, const void *t2)
{
    const unsigned int type1 = *(unsigned int *) t1, type2 = *(unsigned int *) t2;
    for (unsigned int e = 0; e < table.N_entries; e++)
    {
        const struct BondTableEntry entry = table.entries[e];
        if ((entry.atoms[0].type == type1 && entry.atoms[1].type == type2) ||
            (entry.atoms[1].type == type1 && entry.atoms[0].type == type2))
            return entry.length;
    }

    fprintf(stderr, "Warning: Type not found in table\n");
    return 0.;
}

double bondtable_get_length_from_elements(const struct BondTable table, const void *e1, const void *e2)
{
    const char *element1 = (char *) e1, *element2 = (char *) e2;
    for (unsigned int e = 0; e < table.N_entries; e++)
    {
        const struct BondTableEntry entry = table.entries[e];
        if ((strncmp(element1, entry.atoms[0].element, LABEL_LIMIT) == 0 && strncmp(element2, entry.atoms[1].element, LABEL_LIMIT) == 0) ||
            (strncmp(element1, entry.atoms[1].element, LABEL_LIMIT) == 0 && strncmp(element2, entry.atoms[0].element, LABEL_LIMIT) == 0))
            return entry.length;
    }

    // fprintf(stderr, "Warning: Type not found in table\n");
    return 0.;
}

void bondtable_copy(const struct BondTable src, struct BondTable *dest)
{
    dest->N_entries = src.N_entries;
    dest->entries = calloc(src.N_entries, sizeof(struct BondTableEntry));
    if (dest->entries == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (bondtable_copy)");
        return;
    }

    memcpy(dest->entries, src.entries, src.N_entries * sizeof(struct BondTableEntry));
}

void bondtable_delete(struct BondTable *table)
{
    if (table->entries != NULL) free(table->entries);
}

struct BondMap bondmap_new(const struct BondTable table, const bool by_type)
{
    struct BondMap map = {0};
    map.seed = 31;
    if (by_type)
        for (unsigned int e = 0; e < table.N_entries; e++)
            map.table[bondmap_hash_types(&(table.entries[e].atoms[0].type), &(table.entries[e].atoms[1].type))] = table.entries[e].length;
    else
        for (unsigned int e = 0; e < table.N_entries; e++)
            map.table[bondmap_hash_elements(&(table.entries[e].atoms[0].element), &(table.entries[e].atoms[1].element))] =
                table.entries[e].length;
    return map;
}

unsigned int bondmap_hash_types(void *t1, void *t2) { return (*(unsigned int *) t1 * *(unsigned int *) t2) % BOND_MAP_SIZE; }

unsigned int bondmap_hash_elements(void *e1, void *e2)
{
    unsigned int element1 = 0, element2 = 0;
    for (unsigned int c = 0; c < LABEL_LIMIT; c++)
    {
        element1 += (unsigned int) *(char *) (e1 + c);
        element2 += (unsigned int) *(char *) (e2 + c);
    }
    return (element1 * element2) % BOND_MAP_SIZE;
}

struct BondBuilder bondbuilder_new(const char *file_name, const enum BondMode mode, const enum BondSource source,
                                   const struct BondTable table)
{
    struct BondBuilder bond_builder = {0};
    if (file_name != NULL) strncpy(bond_builder.file_name, file_name, BUFFER_LIMIT - 1);
    bond_builder.mode = mode;
    bond_builder.source = source;
    bond_builder.table = table;
    return bond_builder;
}

void bondbuilder_init(struct BondBuilder *bond_builder, const char *file_name, const enum BondMode mode, const enum BondSource source,
                      const struct BondTable table)
{
    if (file_name != NULL)
    {
        strncpy(bond_builder->file_name, file_name, FILE_NAME_LIMIT - 1);
        bond_builder->file_name[FILE_NAME_LIMIT - 1] = '\0';
    }

    bond_builder->mode = mode;
    bond_builder->source = source;
    bondtable_copy(table, &(bond_builder->table));
    if (errno != 0) perror("Error while copying the bond table (bondbuilder_init)");
}

void bondbuilder_copy(const struct BondBuilder src, struct BondBuilder *dest)
{
    bondbuilder_init(dest, src.file_name, src.mode, src.source, src.table);
}

void bondbuilder_read_bond_entry(const struct BondBuilder bond_builder, char line[BUFFER_LIMIT], struct Atom *atom)
{
    char *start = line;
    unsigned int id = 0, type = 0, N_bonds = 0, *bonded_ids = NULL;
    double *bonded_bos = NULL;
    double total_bo = 0.;
    if (sscanf(line, " %u %u %u ", &id, &type, &N_bonds) != 3)  // Could not read the fields
    {
        errno = EIO;
        perror("Error while scanning the first fields (bondbuilder_read_bond_entry)");
        return;
    }

    if (id != atom->id)  // Lines don't match
    {
        errno = EINVAL;
        perror("Error while checking the atom index (bondbuilder_read_bond_entry)");
        return;
    }

    // Skipping the first 3 fields (the ones already read)
    for (unsigned int f = 0; f < 3 + 1; f++)  // Need to add 1 bc of implementation of function
        start = str_go_to_next(start, ' ');

    if (N_bonds != 0)
    {
        // Reading the bonded IDs
        if (bond_builder.mode == BM_ID || bond_builder.mode == BM_FULL)
        {
            bonded_ids = calloc(N_bonds, sizeof(unsigned int));
            if (bonded_ids == NULL)  // Could not allocate memory
            {
                errno = ENOMEM;
                perror("Error while allocating the bond array (bondbuilder_read_bond_entry)");
                return;
            }

            for (unsigned int b = 0; b < N_bonds; b++)
            {
                if (sscanf(start, " %u ", &(bonded_ids[b])) != 1)
                {
                    free(bonded_ids);
                    errno = EIO;
                    perror("Error while scanning a bonded id (bondbuilder_read_bond_entry)");
                    return;
                }
                start = str_go_to_next(start, ' ');
            }
        }

        // Reading the bond orders
        if (bond_builder.mode == BM_BOND_ORDER || bond_builder.mode == BM_FULL)
        {
            // We allocate one more slot to also store the sum
            bonded_bos = calloc(N_bonds, sizeof(double));
            if (bonded_bos == NULL)
            {
                free(bonded_ids);
                errno = ENOMEM;
                perror("Error while allocating the bond orders array (bondbuiler_read_bond_entry)");
                return;
            }

            start = str_go_to_next(start, ' ');  // Skip an unused field (mol id)
            start = str_skip_spaces(start);
            for (unsigned int b = 0; b < N_bonds; b++)
            {
                if (sscanf(start, " %lf ", &(bonded_bos[b])) != 1)
                {
                    free(bonded_ids);
                    free(bonded_bos);
                    errno = EIO;
                    perror("Error while scanning a bond order (bondbuilder_read_bond_entry)");
                    return;
                }
                start = str_go_to_next(start, ' ');
                start = str_skip_spaces(start);
            }

            if (sscanf(start, " %lf ", &total_bo) != 1)
            {
                free(bonded_ids);
                free(bonded_bos);
                errno = EIO;
                perror("Error while scanning the total bond order (bondbuilder_read_bond_entry)");
                return;
            }
        }
    }

    // Transfering the data
    atom->type = type;
    atom->N_bonds = N_bonds;
    atom->ids = bonded_ids;
    atom->bond_orders = bonded_bos;
    atom->total_bo = total_bo;
}

void bondbuilder_delete(struct BondBuilder *builder) { bondtable_delete(&(builder->table)); }

void trajectory_compute_bonds(struct Trajectory *trajectory, const struct BondTable table)
{
    // Getting the atoms types checking attribute (either type or label)
    bool flag = (bool) trajectory->atoms[0].type;

    // Preparing to compute the optimizations
    unsigned long *N_atoms_so_far = malloc(trajectory->N_configurations * sizeof(unsigned long));
    if (N_atoms_so_far == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_compute_bonds.N_atoms_so_far)");
        return;
    }

    unsigned int offset = 0;
    unsigned int N_max_atoms = 0, N_traversed = 0;
    for (unsigned int c = 0; c < trajectory->N_configurations; c++)
    {
        if (c == 0)
            N_atoms_so_far[c] = 0;
        else
            N_atoms_so_far[c] = N_traversed;
        if (N_max_atoms < trajectory->N_atoms[c])
        {
            N_max_atoms = trajectory->N_atoms[c];
            offset = N_traversed;
        }
        N_traversed += trajectory->N_atoms[c];
    }

    // Using a hash table to match types to bond lengths
    struct BondMap map = bondmap_new(table, flag);
    unsigned int (*hash)(void *a, void *b) = NULL;
    size_t type_offset = 0;

    if (flag)
    {
        hash = &bondmap_hash_types;
        type_offset = offsetof(struct Atom, type);
    }
    else
    {
        hash = &bondmap_hash_elements;
        type_offset = offsetof(struct Atom, label);
    }

    // Using a mask to optimize the first atom loop
    bool *mask = calloc(N_max_atoms, sizeof(bool));
    if (mask == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_compute_bonds.mask)");
        return;
    }

    int skip = 0;
#pragma omp parallel for
    for (unsigned int a = 0; a < N_max_atoms; a++)
    {
        if (skip) continue;
        const struct Atom atom = trajectory->atoms[offset + a];
        for (unsigned int e = 0; e < table.N_entries; e++)
        {
            const struct BondTableEntry entry = table.entries[e];
            if (atom.id - 1 >= N_max_atoms)
            {
                skip = EINVAL;
                break;
            }
            // mask[atom.id - 1] = (atom.type == entry.atoms[0].type) || (atom.type == entry.atoms[1].type) ||
            //                     (strncmp(atom.label, entry.atoms[0].element, LABEL_LIMIT) == 0) ||
            //                     (strncmp(atom.label, entry.atoms[1].element, LABEL_LIMIT) == 0);
            mask[atom.id - 1] = flag ? ((atom.type == entry.atoms[0].type) || (atom.type == entry.atoms[1].type))
                                     : ((strncmp(atom.label, entry.atoms[0].element, LABEL_LIMIT) == 0) ||
                                        (strncmp(atom.label, entry.atoms[1].element, LABEL_LIMIT) == 0));
            if (mask[atom.id - 1]) break;
        }
    }

    if (skip)
    {
        free(mask);
        errno = skip;
        perror("Error while computing the mask (trajectory_compute_bonds)");
        return;
    }


#pragma omp parallel for
    for (unsigned int c = 0; c < trajectory->N_configurations; c++)
    {
        if (skip) continue;
        // Trying to use the cache thangs, stack or sum like this...
        struct Atom *atoms = trajectory->atoms + N_atoms_so_far[c];
        unsigned int N_atoms = trajectory->N_atoms[c];
        double box_lengths[3] = {0};
        for (unsigned int d = 0; d < 3; d++) box_lengths[d] = trajectory->box[c].bounds[2 * d + 1] - trajectory->box[c].bounds[2 * d];

        for (unsigned int i = 0; i < N_atoms; i++)
        {
            struct Atom *a1 = atoms + i;
            if (!mask[a1->id - 1] || skip) continue;
            for (unsigned int j = i + 1; j < N_atoms; j++)
            {
                struct Atom *a2 = atoms + j;

                // Gathering the bond length
                double length = map.table[hash((void *) a1 + type_offset, (void *) a2 + type_offset)];

                if (length != 0. && atom_compute_distance(box_lengths, *a1, *a2) <= length * length)
                {
                    // Modifying the bonds lists
                    if (a1->N_bonds == 0)
                    {
                        unsigned int *new_ids = realloc(a1->ids, N_BONDS_LIMIT * sizeof(unsigned int));
                        if (new_ids == NULL)  // Could not reallocate memory
                        {
#pragma omp critical
                            skip = ENOMEM;
                            perror("Error while reallocating memory (trajectory_compute_bonds.new_ids)");
                            break;
                        }
                        a1->ids = new_ids;
                    }
                    else if (a1->N_bonds % N_BONDS_LIMIT == N_BONDS_LIMIT - 1)
                    {
                        unsigned int *new_ids = realloc(a1->ids, (a1->N_bonds + 1 + N_BONDS_LIMIT) * sizeof(unsigned int));
                        if (new_ids == NULL)  // Could not reallocate memory
                        {
#pragma omp critical
                            skip = ENOMEM;
                            perror("Error while reallocating memory (trajectory_compute_bonds.new_ids)");
                            break;
                        }
                        a1->ids = new_ids;
                    }
                    a1->ids[a1->N_bonds] = a2->id;
                    (a1->N_bonds)++;

                    if (a2->N_bonds == 0)
                    {
                        unsigned int *new_ids = realloc(a2->ids, N_BONDS_LIMIT * sizeof(unsigned int));
                        if (new_ids == NULL)  // Could not reallocate memory
                        {
#pragma omp critical
                            skip = ENOMEM;
                            perror("Error while reallocating memory (trajectory_compute_bonds.new_ids)");
                            break;
                        }
                        a2->ids = new_ids;
                    }
                    else if (a2->N_bonds % N_BONDS_LIMIT == N_BONDS_LIMIT - 1)
                    {
                        unsigned int *new_ids = realloc(a2->ids, (a2->N_bonds + 1 + N_BONDS_LIMIT) * sizeof(unsigned int));
                        if (new_ids == NULL)  // Could not reallocate memory
                        {
#pragma omp critical
                            skip = ENOMEM;
                            perror("Error while reallocating memory (trajectory_compute_bonds.new_ids)");
                            break;
                        }
                        a2->ids = new_ids;
                    }
                    a2->ids[a2->N_bonds] = a1->id;
                    (a2->N_bonds)++;
                }
            }
        }
    }

    free(mask);
    free(N_atoms_so_far);

    if (skip)
    {
        errno = skip;
        return;
    }

    // Initializing the bond builder
    bondbuilder_init(&(trajectory->bond_builder), NULL, BM_ID, BS_COMPUTE, table);
}

void trajectory_write_bonds(const struct Trajectory trajectory, const char *file_name)
{
    // Opening the file
    FILE *output = NULL;
    if (file_name == NULL || strcmp(file_name, "stdout") == 0)  // Enable outputting to stdout
        output = stdout;
    else
        output = fopen(file_name, "w");
    if (output == NULL)
    {
        perror("Error while opening the file (trajectory_write_bonds)");
        return;
    }

    // Preparing for writing
    bool flag = (bool) trajectory.atoms[0].type;  // if 0 then flag is false

    // Writing the bonds
    fprintf(output, "# id");

    if (flag)
        fprintf(output, " type");
    else
        fprintf(output, " element");

    fprintf(output, " N_bonds id_0...id_N\n");
    unsigned long a = 0;
    for (unsigned int c = 0; c < trajectory.N_configurations; c++)
    {
        const struct Atom *atoms = trajectory.atoms + a;
        const unsigned int N_atoms = trajectory.N_atoms[c];
        fprintf(output, "# Timestep: %u\n# Number of atoms: %u\n", trajectory.steps[c], N_atoms);
        for (unsigned int i = 0; i < N_atoms; i++)
        {
            const struct Atom atom = atoms[i];

            // The id
            fprintf(output, " %u", atom.id);

            // The type or element
            if (flag)
                fprintf(output, " %u", atom.type);
            else
                fprintf(output, " %s", atom.label);

            // The number of bonds
            fprintf(output, " %u", atom.N_bonds);

            // The bonded ids
            for (unsigned int b = 0; b < atom.N_bonds; b++) fprintf(output, " %u", atom.ids[b]);

            fprintf(output, "\n");
        }
        a += N_atoms;
    }

    // Closing the file
    fclose(output);
}
