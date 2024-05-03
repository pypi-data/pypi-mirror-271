#ifndef _BOND_H
#define _BOND_H

#include <stdbool.h>
#include "atom.h"
#include "utils.h"

enum BondMode
{
    BM_NULL,
    BM_ID,
    BM_BOND_ORDER,
    BM_FULL
};

enum BondSource
{
    BS_NULL,
    BS_REAXFF,
    BS_COMPUTE
};

struct BondTableEntry
{
    union
    {
        unsigned int type;
        char element[LABEL_LIMIT];
    } atoms[2];
    double length;
};

struct BondTable
{
    unsigned int N_entries;
    struct BondTableEntry *entries;
};

struct BondTable bondtable_new(const unsigned int N_entries, ...);

unsigned int *bondtable_extract_types(const struct BondTable table);

double bondtable_get_length_from_types(const struct BondTable table, const void *t1, const void *t2);

double bondtable_get_length_from_elements(const struct BondTable table, const void *e1, const void *e2);

void bondtable_copy(const struct BondTable src, struct BondTable *dest);

void bondtable_delete(struct BondTable *table);

#define BOND_MAP_SIZE 101

struct BondMap
{
    unsigned int seed;
    double table[BOND_MAP_SIZE];
};

struct BondMap bondmap_new(const struct BondTable table, const bool by_type);

unsigned int bondmap_hash_types(void *t1, void *t2);

unsigned int bondmap_hash_elements(void *e1, void *e2);

/** The structure used to build atoms. */
struct BondBuilder
{
    char file_name[FILE_NAME_LIMIT];
    enum BondMode mode;
    enum BondSource source;
    struct BondTable table;
};

/** Initialize the BondBuilder. */
void bondbuilder_init(struct BondBuilder *bond_builder, const char *file_name, const enum BondMode mode, const enum BondSource source, const struct BondTable table);

/** Create a BondBuilder. */
struct BondBuilder bondbuilder_new(const char *file_name, const enum BondMode mode, const enum BondSource source, const struct BondTable table);

/** Copy a BondBuilder to another. */
void bondbuilder_copy(const struct BondBuilder src, struct BondBuilder *dest);

/** Read a bond entry. */
void bondbuilder_read_bond_entry(const struct BondBuilder bond_builder, char line[BUFFER_LIMIT], struct Atom *atom);

void bondbuilder_delete(struct BondBuilder *builder);

/** A mean of selection atoms according to their bond attributes. */
enum BondSelection
{
    // BS_TYPES_ALL,
    // BS_TYPES_ANY,
    BS_N_BONDS,
    BS_TOTAL_BO
};

/** An union to store a value for bond selection. */
union BondField
{
    unsigned int i;  // To select either the types or the number of bonds
    double d;  // To select the total bond order
};

#endif
