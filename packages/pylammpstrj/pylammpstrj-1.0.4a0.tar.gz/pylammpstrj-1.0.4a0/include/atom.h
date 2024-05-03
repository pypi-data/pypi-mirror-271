#ifndef _ATOM_H
#define _ATOM_H
#include "box.h"
#include "utils.h"

#include <stdio.h>

/** The number of characters for additional fields of type str. */
#define ATOM_FIELD_STR_LIMIT 10
#define ATOM_FIELD_STR_LIMIT_SCANF "9"

/** An union to store additional `Atom` fields. */
union AtomField
{
    int i;
    double d;
    char s[ATOM_FIELD_STR_LIMIT];
};

/**
 * The maximum number of characters of element names.
 *
 * The value is 3 for 2 characters and the null-terminator.
 */
#define LABEL_LIMIT 3
/**
 * The maximum number of characters to read for element strings.
 *
 * The null-terminator is excluded.
 */
#define LABEL_SCANF_LIMIT "2"

#define N_BONDS_LIMIT 8

/**
 * The data structure used to represent atoms.
 *
 * The atoms are identified by their `id`.
 *
 * This data structure holds the informations about an atom's `label`,
 * `position`, and `charge`.
 */
struct Atom
{
    unsigned int id;
    unsigned int type;
    char label[LABEL_LIMIT];
    double position[3];
    double charge;

    union AtomField *additionnal_fields;

    // Non-essential attributes
    unsigned int N_bonds;
    unsigned int *ids;
    double *bond_orders;  // Stores one more slot for the sum
    double total_bo;
};

/** Deletes an atom. */
void atom_delete(struct Atom *atom);

typedef union AtomField (*AtomBuilderParsingFunction)(const char[BUFFER_LIMIT]);

/** An enum to identify additional `Atom` fields types. */
enum AtomFieldType
{
    AFT_NULL,
    AFT_INT,
    AFT_DOUBLE,
    AFT_STRING
};

/** Number of characters in the field names. */
#define FIELD_NAME_LIMIT 15

/** Structure used to create `Atom`s. */
struct AtomBuilder
{
    char dump_format[BUFFER_LIMIT];

    unsigned int N_fields;
    unsigned int N_additional;
    char (*field_names)[FIELD_NAME_LIMIT];  // A pointer to static arrays
    size_t *offsets;
    int *is_additional;
    enum AtomFieldType *fields_types;
};

/** Creates an `AtomBuilder`. */
struct AtomBuilder atom_builder_new(const char *dump_format, FILE *input);

/** Copies an `AtomBuilder` to another */
void atom_builder_copy(struct AtomBuilder *, const struct AtomBuilder);

/** Deletes an `AtomBuilder`. */
void atom_builder_delete(struct AtomBuilder *ab);

/** Copies an `Atom` to another. */
void atom_copy(struct Atom *dest, const struct Atom src, const struct AtomBuilder atom_builder);

/** Creates an `Atom` from a line of a trajectory file. */
void atom_read_entry(struct Atom *atom, const struct AtomBuilder atom_builder, char line[BUFFER_LIMIT], union AtomField *additional_fields);

double atom_compute_distance(const double lengths[3], const struct Atom a1, const struct Atom a2);

#endif
