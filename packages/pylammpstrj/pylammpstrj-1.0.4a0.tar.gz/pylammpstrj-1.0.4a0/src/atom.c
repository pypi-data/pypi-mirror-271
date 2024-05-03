#include "atom.h"
#include "utils.h"

#include <ctype.h>
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

void atom_delete(struct Atom *atom)
{
    if (atom->additionnal_fields != NULL) atom->additionnal_fields = NULL;  // Only need to dereference
    if (atom->N_bonds != 0)
    {
        free(atom->ids);
        free(atom->bond_orders);
    }
}

void atom_copy(struct Atom *dest, const struct Atom src, const struct AtomBuilder atom_builder)
{
    dest->id = src.id;
    dest->type = src.type;
    strncpy(dest->label, src.label, LABEL_LIMIT);
    memcpy(dest->position, src.position, 3 * sizeof(double));
    dest->charge = src.charge;
    if (atom_builder.N_additional != 0)
        memcpy(dest->additionnal_fields, src.additionnal_fields, atom_builder.N_additional * sizeof(union AtomField));  // To check
    dest->N_bonds = src.N_bonds;
    if (src.N_bonds != 0)
    {
        dest->ids = calloc(src.N_bonds, sizeof(unsigned int));
        if (dest->ids == NULL)
        {
            errno = ENOMEM;
            perror("Error while allocating memory (atom_copy.dest.ids)");
            return;
        }
        memcpy(dest->ids, src.ids, src.N_bonds * sizeof(unsigned int));
        if (src.bond_orders != NULL)
        {
            dest->bond_orders = calloc(src.N_bonds, sizeof(double));
            if (dest->bond_orders == NULL)
            {
                errno = ENOMEM;
                perror("Error while allocating memory (atom_copy.dest.bond_orders)");
                return;
            }
            memcpy(dest->bond_orders, src.bond_orders, src.N_bonds * sizeof(double));
            dest->total_bo = src.total_bo;
        }
    }
}

#define FIELDS_BASE_SIZE 10
#define FIELDS_SIZE_INCR 10

void get_field_names(struct AtomBuilder *ab)
{
    char buffer[BUFFER_LIMIT], *ptr;
    char(*names)[FIELD_NAME_LIMIT] = calloc(FIELDS_BASE_SIZE, sizeof(char[FIELD_NAME_LIMIT]));

    if (names == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (AtomBuilder.names)");
        return;
    }

    unsigned int names_size = FIELDS_BASE_SIZE;
    unsigned int n = 0;

    strncpy(buffer, ab->dump_format, BUFFER_LIMIT);
    ptr = strtok(buffer, " ");

    while (ptr != NULL)
    {
        if (n >= names_size)
        {
            char(*new_names)[FIELD_NAME_LIMIT] = realloc(names, (names_size + FIELDS_SIZE_INCR) * sizeof(char[FIELD_NAME_LIMIT]));

            if (new_names == NULL)
            {
                free(new_names);
                errno = ENOMEM;
                perror("Error while reallocating memory (AtomBuilder.names)");
                return;
            }

            names_size += FIELDS_SIZE_INCR;
            names = new_names;
        }

        if (strlen(ptr) < FIELD_NAME_LIMIT - 1)  // !
            strncpy(names[n], ptr, FIELD_NAME_LIMIT);

        ptr = strtok(NULL, " ");
        n++;
    }

    ab->N_fields = n;
    names[n - 1][strcspn(names[n - 1], "\n")] = 0;
    ab->field_names = names;
}

void check_names(struct AtomBuilder *ab)
{
    ab->offsets = calloc(ab->N_fields, sizeof(size_t));
    ab->is_additional = calloc(ab->N_fields, sizeof(int));
    ab->fields_types = malloc(ab->N_fields * sizeof(enum AtomFieldType));

    if (ab->offsets == NULL || ab->is_additional == NULL || ab->fields_types == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (AtomBuilder.check_names)");
        return;
    }

    unsigned int N_additional = 0;
    for (unsigned int f = 0; f < ab->N_fields; f++)
    {
        (ab->fields_types)[f] = AFT_NULL;
        if (strcmp((ab->field_names)[f], "id") == 0)
        {
            (ab->offsets)[f] = offsetof(struct Atom, id);
            (ab->fields_types)[f] = AFT_INT;
        }
        else if (strcmp((ab->field_names)[f], "type") == 0)
        {
            (ab->offsets)[f] = offsetof(struct Atom, type);
            (ab->fields_types)[f] = AFT_INT;
        }
        else if (strcmp((ab->field_names)[f], "element") == 0 || strcmp((ab->field_names)[f], "label") == 0)
        {
            (ab->offsets)[f] = offsetof(struct Atom, label);
            (ab->fields_types)[f] = AFT_STRING;
        }
        else if (strlen((ab->field_names)[f]) == 1)
        {
            if ((ab->field_names)[f][0] == 'x')
                (ab->offsets)[f] = offsetof(struct Atom, position[0]);
            else if ((ab->field_names)[f][0] == 'y')
                (ab->offsets)[f] = offsetof(struct Atom, position[1]);
            else if ((ab->field_names)[f][0] == 'z')
                (ab->offsets)[f] = offsetof(struct Atom, position[2]);
            else if ((ab->field_names)[f][0] == 'q')
                (ab->offsets)[f] = offsetof(struct Atom, charge);

            if ((ab->offsets)[f] != 0) (ab->fields_types)[f] = AFT_DOUBLE;
        }
        else
        {
            (ab->offsets)[f] = N_additional;  // the rank in the additional_fields array
            (ab->is_additional)[f] = 1;
            N_additional++;
        }
    }
    ab->N_additional = N_additional;
}

void get_additional_types(const char line[BUFFER_LIMIT], struct AtomBuilder *ab)
{
    char buffer[BUFFER_LIMIT];
    strncpy(buffer, line, BUFFER_LIMIT);
    buffer[BUFFER_LIMIT - 1] = '\0';

    char *ptr = strtok(buffer, " ");

    for (unsigned int f = 0; f < ab->N_fields; ptr = strtok(NULL, " "), f++)
    {
        if (!(ab->is_additional)[f]) continue;

        if (isalpha(ptr[0]))
            (ab->fields_types)[f] = AFT_STRING;
        else
            (ab->fields_types)[f] = AFT_DOUBLE;
    }
}

struct AtomBuilder atom_builder_new(const char *dump_format, FILE *input)
{
    struct AtomBuilder ab = {0};

    // Initialize the dump format
    strncpy(ab.dump_format, dump_format, BUFFER_LIMIT);
    ab.dump_format[BUFFER_LIMIT - 1] = '\0';

    // Initialize the field names
    get_field_names(&ab);
    if (errno != 0) return ab;

    // Initialize offsets, is_additional, and fields_types
    check_names(&ab);
    if (errno != 0)
    {
        free(ab.field_names);
        return ab;
    }

    // Skip to the atoms section header
    char line[BUFFER_LIMIT];
    long pos = ftell(input);
    do
        if (fgets(line, BUFFER_LIMIT, input) == NULL)
        {
            free(ab.fields_types);
            free(ab.is_additional);
            free(ab.offsets);
            free(ab.field_names);
            errno = EIO;
            perror("Error while reading a line (AtomBuilder.atom_builder_new)");
            return ab;
        }
    while (strncmp(line, "ITEM: ATOMS", 11) != 0);

    if (fgets(line, BUFFER_LIMIT, input) == NULL)
    {
        free(ab.fields_types);
        free(ab.is_additional);
        free(ab.offsets);
        free(ab.field_names);
        errno = EIO;
        perror("Error while reading a line");
        return ab;
    }
    get_additional_types(line, &ab);  // Parse the header
    fseek(input, pos, SEEK_SET);      // Reset the file pointer position

    return ab;
}

void atom_read_entry(struct Atom *atom, const struct AtomBuilder builder, char line[BUFFER_LIMIT], union AtomField *additional_fields)
{
    *atom = (struct Atom) {0};
    char *start = line;
    for (unsigned int f = 0; f < builder.N_fields; f++)
    {
        // Parse the current field
        size_t offset = builder.offsets[f];
        if ((builder.is_additional)[f])  // Fill additional fields
        {
            union AtomField atom_field = {0};
            switch (builder.fields_types[f])
            {
                case AFT_INT:
                    if (sscanf(start, " %d ", &atom_field.i) != 1)
                    {
                        errno = EIO;
                        perror("Error while parsing an atom field (read_atom_entry.atom_field.i)");
                        return;
                    }
                    break;
                case AFT_DOUBLE:
                    if (sscanf(start, " %lf ", &atom_field.d) != 1)
                    {
                        errno = EIO;
                        perror("Error while parsing an atom field (read_atom_entry.atom_field.d)");
                        return;
                    }
                    break;
                case AFT_STRING:
                    if (sscanf(start, " %" ATOM_FIELD_STR_LIMIT_SCANF "s ", (char *) &atom_field.s) != 1)
                    {
                        errno = EIO;
                        perror("Error while parsing an atom field (read_atom_entry.atom_field.s)");
                        return;
                    }
                    break;
                default:
                    errno = EINVAL;
                    perror("Error while parging an atom field (read_atom_entry.atom_field, AFT_NULL)");
                    return;
            }
            additional_fields[offset] = atom_field;
        }
        else  // Fill base fields
            switch (builder.fields_types[f])
            {
                case AFT_INT:
                    if (sscanf(start, " %d ", (int *) ((void *) atom + offset)) != 1)
                    {
                        errno = EIO;
                        perror("Error while parsing an atom field (read_atom_entry.atom, AFT_INT)");
                        return;
                    }
                    break;
                case AFT_DOUBLE:
                    if (sscanf(start, " %lf ", (double *) ((void *) atom + offset)) != 1)
                    {
                        errno = EIO;
                        perror("Error while parsing an atom field (read_atom_entry.atom, AFT_DOUBLE)");
                        return;
                    }
                    break;
                case AFT_STRING:
                    // Only authorized str base field is the label
                    if (sscanf(start, " %" LABEL_SCANF_LIMIT "s ", (char *) atom->label) != 1)
                    {
                        errno = EIO;
                        perror("Error while parsing an atom field (read_atom_entry.atom, AFT_STRING)");
                        return;
                    }
                    break;
                default:
                    errno = EINVAL;
                    perror("Error while parging an atom field (read_atom_entry.atom, AFT_NULL)");
                    return;
            }

        // Go to next field
        start = str_go_to_next(start, ' ');
    }
}

void atom_builder_copy(struct AtomBuilder *dest, const struct AtomBuilder src)
{
    strncpy(dest->dump_format, src.dump_format, BUFFER_LIMIT);

    dest->N_fields = src.N_fields;
    dest->N_additional = src.N_additional;

    dest->field_names = malloc(src.N_fields * sizeof(char[FIELD_NAME_LIMIT]));
    if (dest->field_names == NULL)
    {
        errno = ENOMEM;
        perror(
            "Error while allocation memory "
            "(atom_builder_copy.dest.field_names)");
        return;
    }
    memcpy(dest->field_names, src.field_names, src.N_fields * sizeof(char[FIELD_NAME_LIMIT]));

    dest->offsets = malloc(src.N_fields * sizeof(size_t));
    if (dest->offsets == NULL)
    {
        free(dest->field_names);
        errno = ENOMEM;
        perror("Error while allocation memory (atom_builder_copy.dest.offsets)");
        return;
    }
    memcpy(dest->offsets, src.offsets, src.N_fields * sizeof(size_t));

    dest->is_additional = malloc(src.N_fields * sizeof(int));
    if (dest->is_additional == NULL)
    {
        free(dest->offsets);
        free(dest->field_names);
        errno = ENOMEM;
        perror(
            "Error while allocation memory "
            "(atom_builder_copy.dest.is_additional)");
        return;
    }
    memcpy(dest->is_additional, src.is_additional, src.N_fields * sizeof(int));

    dest->fields_types = malloc(src.N_fields * sizeof(enum AtomFieldType));
    if (dest->fields_types == NULL)
    {
        free(dest->is_additional);
        free(dest->offsets);
        free(dest->field_names);
        errno = ENOMEM;
        perror(
            "Error while allocation memory "
            "(atom_builder_copy.dest.fields_types)");
        return;
    }
    memcpy(dest->fields_types, src.fields_types, src.N_fields * sizeof(enum AtomFieldType));
}

void atom_builder_delete(struct AtomBuilder *ab)
{
    free(ab->field_names);
    free(ab->offsets);
    free(ab->is_additional);
    free(ab->fields_types);
}

double atom_compute_distance(const double lengths[3], const struct Atom a1, const struct Atom a2)
{
    double res = 0.;
    for (unsigned int d = 0; d < 3; d++)
    {
        double pos1 = a1.position[d], pos2 = a2.position[d];
        double img = pos2;  // the closest periodic image of a2 to a1 in the current direction

        // Applying the PBCs
        if (pos2 - pos1 < -lengths[d] / 2.)
            img += lengths[d];
        else if (pos2 - pos1 > lengths[d] / 2.)
            img -= lengths[d];

        res += (img - pos1) * (img - pos1);
    }
    return res;
}
