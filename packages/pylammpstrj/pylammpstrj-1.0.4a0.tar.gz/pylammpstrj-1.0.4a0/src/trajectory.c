#include "trajectory.h"
#include "atom.h"
#include "bond.h"
#include "box.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void trajectory_init(struct Trajectory *trajectory, const struct AtomBuilder atom_builder, const unsigned long N_configurations,
                     unsigned int *steps, unsigned int *N_atoms, struct Box *box, struct Atom *atoms, union AtomField *additional_fields)
{
    *trajectory = (struct Trajectory){0};
    trajectory->atom_builder = atom_builder;
    trajectory->N_configurations = N_configurations;
    trajectory->N_atoms = N_atoms;
    for (unsigned int c = 0; c < N_configurations; c++)
        for (unsigned int a = 0; a < N_atoms[c]; a++) (trajectory->_total_atoms)++;
    trajectory->steps = steps;
    trajectory->box = box;
    trajectory->atoms = atoms;
    trajectory->_additional_fields = additional_fields;
}

void trajectory_delete_atoms(struct Trajectory *trajectory)
{
    // Preparing to deallocate the atom fields
    int additional_flag = (trajectory->atom_builder.N_additional != 0);
    int bo_flag = trajectory->bond_builder.mode == BM_BOND_ORDER || trajectory->bond_builder.mode == BM_FULL;
    int id_flag = trajectory->bond_builder.mode == BM_ID || trajectory->bond_builder.mode == BM_FULL;

    if (trajectory->atoms != NULL)
    {
        // Deallocating the atom fields
        for (unsigned int a = 0; a < trajectory->_total_atoms; a++)
        {
            // Dereferencing the additional fields
            if (additional_flag) trajectory->atoms[a].additionnal_fields = NULL;

            // Deallocating the bond fields
            if (trajectory->atoms[a].N_bonds != 0)
            {
                if (id_flag) free(trajectory->atoms[a].ids);
                if (bo_flag) free(trajectory->atoms[a].bond_orders);
            }
        }

        // Deallocating the additional fields
        free(trajectory->_additional_fields);
        trajectory->_additional_fields = NULL;

        // Deallocating the atoms
        free(trajectory->atoms);
        trajectory->atoms = NULL;

        trajectory->_total_atoms = 0;
    }
}

void trajectory_delete(struct Trajectory *trajectory)
{
    // Deallocating the atoms and related data
    trajectory_delete_atoms(trajectory);

    // Deallocating the atom builder
    atom_builder_delete(&(trajectory->atom_builder));

    // Deallocating the boxes
    if (trajectory->box != NULL)
    {
        free(trajectory->box);
        trajectory->box = NULL;
    }

    // Deallocating the steps
    if (trajectory->steps != NULL)
    {
        free(trajectory->steps);
        trajectory->steps = NULL;
    }

    // Deallocating the number of atoms
    if (trajectory->N_atoms != NULL)
    {
        free(trajectory->N_atoms);
        trajectory->N_atoms = NULL;
    }

    // Deallocating the bond builder
    if (trajectory->bond_builder.source == BS_COMPUTE) bondbuilder_delete(&(trajectory->bond_builder));
}
