#ifndef _TRAJECTORY_H
#define _TRAJECTORY_H
#include "atom.h"
#include "bond.h"
#include "box.h"
#include "select.h"
#include "utils.h"

#include <stdbool.h>
#include <stdio.h>

/** Trajectory file structure. */
struct TrajectoryFile
{
    char file_name[FILE_NAME_LIMIT];
    char user_format[BUFFER_LIMIT];
    unsigned int batch_size;
    unsigned long N_configurations;
    unsigned long *steps;
    long *conf_pos;
    unsigned int N_selections;
    struct Selection *selections;
};

/** Creating a `TrajectoryFile`. */
struct TrajectoryFile trajectoryfile_new(const char *file_name, const char *user_format, const unsigned int batch_size);

/** Copying a `TrajectoryFile` to another. */
struct TrajectoryFile trajectoryfile_copy(struct TrajectoryFile *dest, const struct TrajectoryFile src);

/** Deleting a `TrajectoryFile`. */
void trajectoryfile_delete(struct TrajectoryFile *trajectory_file);

/** To extract a property from all atoms of the trajectory. */
union AtomField *trajectoryfile_get_property(const struct TrajectoryFile, const unsigned int field, unsigned long *size);

/** To compute the average of a property over the configurations. */
double *trajectoryfile_average_property(const struct TrajectoryFile trajectory_file, const unsigned int field);

/** Stores atoms selection parameters. */
void trajectoryfile_select_atoms(struct TrajectoryFile *trajectory_file, const struct Selection selection);

void trajectoryfile_clear_selections(struct TrajectoryFile *trajectory_file);

/** The data structure used to represent a trajectory. */
struct Trajectory
{
    struct AtomBuilder atom_builder;
    struct BondBuilder bond_builder;
    unsigned long N_configurations;
    unsigned int *N_atoms;
    unsigned long _total_atoms;
    unsigned int *steps;
    struct Box *box;
    struct Atom *atoms;
    union AtomField *_additional_fields;
};

/** Creating a `Trajectory` from a `TrajectoryFile`. */
void trajectoryfile_read_slice(struct TrajectoryFile trajectory_file, unsigned long start, unsigned long N_configurations,
                               struct Trajectory *trajectory);

void trajectory_init(struct Trajectory *trajectory, const struct AtomBuilder atom_builder, const unsigned long N_configurations,
                     unsigned int *N_atoms, unsigned int *steps, struct Box *box, struct Atom *atoms, union AtomField *additional_fields);

void trajectory_skip(FILE **input, const unsigned long start);

void trajectory_read(const char *file_name, const unsigned long start, const char *user_format, struct Trajectory *trajectory);

void trajectory_read_bonds(const char *file_name, enum BondMode bond_mode, struct Trajectory *trajectory);

void trajectory_compute_bonds(struct Trajectory *trajectory, const struct BondTable table);

void trajectory_write_bonds(const struct Trajectory trajectory, const char *file_name);

void trajectory_select(struct Trajectory *trajectory, const struct Selection selection, const int inplace, struct Trajectory *selected);

void trajectory_moving_select(struct Trajectory *trajectory, const struct Selection *selection, const int inplace, struct Trajectory *selected);

/** Extract a property from all atoms for the whole trajectory. */
union AtomField *trajectory_get_property(const struct Trajectory trajectory, const unsigned int field, unsigned long *size);

union AtomField *trajectory_get_property_par(const struct Trajectory trajectory, const unsigned int field, unsigned long *size);

/** To compute the average of a property over the configurations. */
double *trajectory_average_property(const struct Trajectory, const unsigned int);

void trajectory_delete_atoms(struct Trajectory *trajectory);

/** Deletes a trajectory. */
void trajectory_delete(struct Trajectory *trajectory);

#endif
