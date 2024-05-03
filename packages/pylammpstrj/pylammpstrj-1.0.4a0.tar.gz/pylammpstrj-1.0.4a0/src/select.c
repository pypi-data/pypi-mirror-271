#include "select.h"
#include "atom.h"
#include "bond.h"
#include "box.h"
#include "trajectory.h"
#include "utils.h"

#include <errno.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void selection_parse_atom_selection(const struct Selection *selection, const struct AtomBuilder builder, size_t *offset,
                                    int (**to_select)(const void *, const void *), void **value_ptr)
{
    *offset = builder.offsets[selection->field];
    *value_ptr = (void *) &(selection->value);

    switch (builder.fields_types[selection->field])
    {
        case AFT_NULL:
            errno = EINVAL;
            perror("Error while checking the type (selection_parse_atom_selection.type)");
            return;
        case AFT_INT:
            switch (selection->op)
            {
                case OPERATOR_NULL:
                    errno = EINVAL;
                    perror("Error while checking the selection operator (selection_parse_atom_selection.op)");
                    return;
                case OPERATOR_LT:
                    *to_select = &int_lt;
                    break;
                case OPERATOR_LEQ:
                    *to_select = &int_leq;
                    break;
                case OPERATOR_EQ:
                    *to_select = &int_eq;
                    break;
                case OPERATOR_GEQ:
                    *to_select = &int_geq;
                    break;
                case OPERATOR_GT:
                    *to_select = &int_gt;
                    break;
            }
            break;
        case AFT_DOUBLE:
            switch (selection->op)
            {
                case OPERATOR_NULL:
                    errno = EINVAL;
                    perror("Error while checking the selection operator (selection_parse_atom_selection.op)");
                    return;
                case OPERATOR_LT:
                    *to_select = &double_lt;
                    break;
                case OPERATOR_LEQ:
                    *to_select = &double_leq;
                    break;
                case OPERATOR_EQ:
                    *to_select = &double_eq;
                    break;
                case OPERATOR_GEQ:
                    *to_select = &double_geq;
                    break;
                case OPERATOR_GT:
                    *to_select = &double_gt;
                    break;
            }
            break;
        case AFT_STRING:
            switch (selection->op)
            {
                case OPERATOR_EQ:
                    *to_select = &str_eq;
                    break;
                default:
                    errno = EINVAL;
                    perror("Error while checking the selection operator (selection_parse_atom_selection.op)");
                    return;
            }
            break;
    }
}

void selection_parse_bond_selection(const struct Selection *selection, size_t *offset, int (**to_select)(const void *, const void *),
                                    void **value_ptr)
{
    *value_ptr = (void *) &(selection->value);
    switch (selection->field)
    {
        // case BS_TYPES_ALL:
        //     offset = offsetof(struct Atom, type);
        //     type = BFT_UINT;
        //     compare = &uint_compare;
        //     break;
        // case BS_TYPES_ANY:
        //     offset = offsetof(struct Atom, type);
        //     type = BFT_UINT;
        //     compare = &uint_compare;
        //     break;
        case BS_N_BONDS:
            *offset = offsetof(struct Atom, N_bonds);
            switch (selection->op)
            {
                case OPERATOR_LT:
                    *to_select = &uint_lt;
                    break;
                case OPERATOR_LEQ:
                    *to_select = &uint_leq;
                    break;
                case OPERATOR_EQ:
                    *to_select = &uint_eq;
                    break;
                case OPERATOR_GEQ:
                    *to_select = &uint_geq;
                    break;
                case OPERATOR_GT:
                    *to_select = &uint_gt;
                    break;
                case OPERATOR_NULL:
                    errno = EINVAL;
                    perror("Error while checking the selection operator (trajectory_select_bonds.op)");
                    return;
            }
            break;
        case BS_TOTAL_BO:
            *offset = offsetof(struct Atom, total_bo);
            switch (selection->op)
            {
                case OPERATOR_LT:
                    *to_select = &double_lt;
                    break;
                case OPERATOR_LEQ:
                    *to_select = &double_leq;
                    break;
                case OPERATOR_EQ:
                    *to_select = &double_eq;
                    break;
                case OPERATOR_GEQ:
                    *to_select = &double_geq;
                    break;
                case OPERATOR_GT:
                    *to_select = &double_gt;
                    break;
                case OPERATOR_NULL:
                    errno = EINVAL;
                    perror("Error while checking the selection operator (trajectory_select_bonds.op)");
                    return;
            }
            break;
        default:
            errno = EINVAL;
            perror("Bond selection not yet implemented");
            return;
    }
}

void trajectory_select(struct Trajectory *src, const struct Selection selection, const int inplace, struct Trajectory *dest)
{
    // Parsing the selection
    size_t offset = 0;
    int (*to_select)(const void *a, const void *b) = NULL;
    void *value_ptr = NULL;
    switch (selection.type)
    {
        case SELECTION_FIELDS:
            selection_parse_atom_selection(&selection, src->atom_builder, &offset, &to_select, &value_ptr);
            break;
        case SELECTION_BONDS:
            selection_parse_bond_selection(&selection, &offset, &to_select, &value_ptr);
            break;
        default:
            errno = EINVAL;
            perror("Error with the selection type (trajectory_select)");
            return;
    }

    if (errno != 0)
    {
        perror("Error while parsing the selection (trajectory_select.selection)");
        return;
    }

    // Preparing the arrays
    unsigned int *N_atoms = calloc(src->N_configurations, sizeof(unsigned int));
    if (N_atoms == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_select_atoms.N_atoms)");
        return;
    }

    unsigned int *steps = NULL;
    struct Box *boxes = NULL;
    struct Atom *atoms = NULL;
    union AtomField *additional_fields = NULL;

    unsigned long *selected = calloc(src->_total_atoms, sizeof(unsigned long));
    if (selected == NULL)
    {
        free(N_atoms);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_select_atoms)");
        return;
    }
    unsigned long N_selected = 0;
    unsigned long at = 0;

    if (selection.type == SELECTION_FIELDS &&
        src->atom_builder.is_additional[selection.field])  // If we select according to additional atom fields
        for (unsigned int c = 0; c < src->N_configurations; c++)
        {
            for (unsigned int a = 0; a < src->N_atoms[c]; a++)
            {
                if (to_select((void *) &(src->atoms[at + a].additionnal_fields[offset]), value_ptr))
                {
                    selected[N_selected] = at + a;
                    N_atoms[c]++;
                    N_selected++;
                }
            }
            at += src->N_atoms[c];
        }
    else  // If we select according to bonds or base fields
        for (unsigned int c = 0; c < src->N_configurations; c++)
        {
            for (unsigned int a = 0; a < src->N_atoms[c]; a++)
            {
                if (to_select((void *) (src->atoms + at + a) + offset, value_ptr))
                {
                    selected[N_selected] = at + a;
                    N_atoms[c]++;
                    N_selected++;
                }
            }
            at += src->N_atoms[c];
        }

    auto unsigned long *new_selected = realloc(selected, N_selected * sizeof(unsigned long));
    if (N_selected != 0 && new_selected == NULL)
    {
        free(selected);
        free(N_atoms);
        errno = ENOMEM;
        perror("Error while reallocating memory (trajectory_select_atoms.selected)");
        return;
    }
    selected = new_selected;

    atoms = calloc(N_selected, sizeof(struct Atom));
    if (N_selected != 0 && atoms == NULL)
    {
        free(selected);
        free(N_atoms);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_select_atoms.atoms)");
        return;
    }

    additional_fields = calloc(src->atom_builder.N_additional * N_selected, sizeof(union AtomField));
    if (N_selected != 0 && additional_fields == NULL)
    {
        free(atoms);
        free(selected);
        free(N_atoms);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_select_atoms.additional_fields)");
        return;
    }

    int err = 0;
#pragma omp parallel for
    for (unsigned long a = 0; a < N_selected; a++)
    {
        if (err) continue;
        atoms[a].additionnal_fields = additional_fields + src->atom_builder.N_additional * a;
        atom_copy(atoms + a, src->atoms[selected[a]], src->atom_builder);
        if (errno != 0)
#pragma omp critical
            err = errno;
    }

    if (err)  // An error occurred
    {
        free(additional_fields);
        for (unsigned long a = 0; a < N_selected; a++) atom_delete(atoms + a);
        free(atoms);
        free(selected);
        free(N_atoms);
        errno = err;
        perror("Error while copying the atoms (trajectory_select_atoms)");
        return;
    }

    // Freeing up
    free(selected);

    // Transfering the data
    if (!inplace)
    {
        struct AtomBuilder atom_builder = {0};
        atom_builder_copy(&atom_builder, src->atom_builder);
        if (errno != 0)
        {
            free(additional_fields);
            free(atoms);
            free(N_atoms);
            perror("Error while copying the atom builder (trajectory_select_atoms.atom_builder)");
            return;
        }

        steps = calloc(src->N_configurations, sizeof(unsigned int));
        if (steps == NULL)
        {
            atom_builder_delete(&atom_builder);
            free(additional_fields);
            free(atoms);
            free(N_atoms);
            errno = ENOMEM;
            perror("Error while allocating memory (trajectory_select_atoms.steps)");
            return;
        }
        memcpy(steps, src->steps, src->N_configurations * sizeof(unsigned int));

        size_t size = src->N_configurations * sizeof(struct Box);
        boxes = malloc(size);
        if (boxes == NULL)
        {
            free(steps);
            atom_builder_delete(&atom_builder);
            free(additional_fields);
            free(atoms);
            free(N_atoms);
            errno = ENOMEM;
            perror("Error while allocating memory (trajectory_select_atoms.boxes)");
            return;
        }
        memcpy(boxes, src->box, size);

        trajectory_init(dest, atom_builder, src->N_configurations, steps, N_atoms, boxes, atoms, additional_fields);

        bondbuilder_copy(src->bond_builder, &(dest->bond_builder));
        if (errno != 0)
        {
            free(boxes);
            free(steps);
            atom_builder_delete(&atom_builder);
            free(additional_fields);
            free(atoms);
            free(N_atoms);
            perror("Error while copying the bond builder (trajectory_select_atoms.bond_builder)");
            return;
        }

        return;
    }

    free(src->N_atoms);
    src->N_atoms = N_atoms;
    trajectory_delete_atoms(src);
    src->_additional_fields = additional_fields;
    src->atoms = atoms;
    src->_total_atoms = N_selected;
}

void trajectory_moving_select(struct Trajectory *src, const struct Selection *selections, const int inplace, struct Trajectory *dest)
{
    // Declaring some variables
    const unsigned int N_configurations = src->N_configurations;
    const unsigned int *N_atoms = src->N_atoms;
    const struct AtomBuilder atom_builder = src->atom_builder;

    unsigned int *N_selected = calloc(N_configurations, sizeof(unsigned int));
    if (N_selected == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_moving_select.N_selected)");
        return;
    }

    unsigned long *selected = calloc(src->_total_atoms, sizeof(unsigned long));
    if (selected == NULL)
    {
        free(N_selected);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_moving_select.N_selected)");
        return;
    }
    unsigned long total_selected = 0;

    size_t offset = 0;
    int (*to_select)(const void *, const void *) = NULL;
    void *value_ptr = NULL;
    unsigned long at = 0;

    // Going through the configurations
    for (unsigned int c = 0; c < N_configurations; c++)
    {
        const struct Selection selection = selections[c];
        if (selection.type == SELECTION_FIELDS && atom_builder.is_additional[selection.field])
        {
            // Parsing the current selection
            selection_parse_atom_selection(&selection, atom_builder, &offset, &to_select, &value_ptr);
            if (errno != 0)
            {
                perror("Error while parsing the atom selection (trajectory_moving_select)");
                return;
            }

            for (unsigned int a = 0; a < N_atoms[c]; a++)
            {
                if (to_select((void *) &(src->atoms[at + a].additionnal_fields[offset]), value_ptr))
                {
                    selected[total_selected] = at + a;
                    N_selected[c]++;
                    total_selected++;
                }
            }
        }
        else
        {
            // Parsing the current selection
            if (selection.type == SELECTION_FIELDS)
                selection_parse_atom_selection(&selection, atom_builder, &offset, &to_select, &value_ptr);
            else if (selection.type == SELECTION_BONDS)
                selection_parse_bond_selection(&selection, &offset, &to_select, &value_ptr);
            else
            {
                errno = EINVAL;
                perror("Error while parsing the selection (trajectory_moving_select)");
                return;
            }

            if (errno != 0)
            {
                perror("Error while parsing the selection (trajectory_moving_select)");
                return;
            }

            for (unsigned int a = 0; a < src->N_atoms[c]; a++)
            {
                if (to_select((void *) (src->atoms + at + a) + offset, value_ptr))
                {
                    selected[total_selected] = at + a;
                    N_selected[c]++;
                    total_selected++;
                }
            }
        }

        at += N_atoms[c];
    }

    // Copying the results
    auto unsigned long *new_selected = realloc(selected, total_selected * sizeof(unsigned long));
    if (total_selected != 0 && new_selected == NULL)
    {
        free(selected);
        free(N_selected);
        errno = ENOMEM;
        perror("Error while reallocating memory (trajectory_moving_select.new_selected)");
        return;
    }
    selected = new_selected;

    struct Atom *atoms = calloc(total_selected, sizeof(struct Atom));
    if (total_selected != 0 && atoms == NULL)
    {
        free(selected);
        free(N_selected);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_moving_select.atoms)");
        return;
    }

    union AtomField *additional_fields = calloc(atom_builder.N_additional * total_selected, sizeof(union AtomField));
    if (total_selected != 0 && additional_fields == NULL)
    {
        free(atoms);
        free(selected);
        free(N_selected);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_moving_select.additional_fields)");
        return;
    }

    int err = 0;
#pragma omp parallel for
    for (unsigned long a = 0; a < total_selected; a++)
    {
        if (err) continue;
        atoms[a].additionnal_fields = additional_fields + atom_builder.N_additional * a;
        atom_copy(atoms + a, src->atoms[selected[a]], src->atom_builder);
        if (errno != 0)
#pragma omp critical
            err = errno;
    }

    if (err)  // An error occurred
    {
        free(additional_fields);
        for (unsigned long a = 0; a < total_selected; a++) atom_delete(atoms + a);
        free(atoms);
        free(selected);
        free(N_selected);
        errno = err;
        perror("Error while copying the atoms (trajectory_select_atoms)");
        return;
    }

    free(selected);

    // Transfering the data
    if (!inplace)
    {
        struct AtomBuilder builder = {0};
        atom_builder_copy(&builder, atom_builder);
        if (errno != 0)
        {
            free(additional_fields);
            for (unsigned long a = 0; a < total_selected; a++) atom_delete(atoms + a);
            free(atoms);
            free(N_selected);
            perror("Error while copying the atom builder (trajectory_select_atoms.atom_builder)");
            return;
        }

        size_t size = N_configurations * sizeof(unsigned int);
        unsigned int *steps = malloc(size);
        if (steps == NULL)
        {
            atom_builder_delete(&builder);
            free(additional_fields);
            for (unsigned long a = 0; a < total_selected; a++) atom_delete(atoms + a);
            free(atoms);
            free(N_selected);
            errno = ENOMEM;
            perror("Error while allocating memory (trajectory_select_atoms.steps)");
            return;
        }
        memcpy(steps, src->steps, size);

        size = N_configurations * sizeof(struct Box);
        struct Box *boxes = malloc(size);
        if (boxes == NULL)
        {
            free(steps);
            atom_builder_delete(&builder);
            free(additional_fields);
            for (unsigned long a = 0; a < total_selected; a++) atom_delete(atoms + a);
            free(atoms);
            free(N_selected);
            errno = ENOMEM;
            perror("Error while allocating memory (trajectory_select_atoms.boxes)");
            return;
        }
        memcpy(boxes, src->box, size);

        trajectory_init(dest, builder, N_configurations, steps, N_selected, boxes, atoms, additional_fields);

        bondbuilder_copy(src->bond_builder, &(dest->bond_builder));
        if (errno != 0)
        {
            free(boxes);
            free(steps);
            atom_builder_delete(&builder);
            free(additional_fields);
            for (unsigned long a = 0; a < total_selected; a++) atom_delete(atoms + a);
            free(atoms);
            free(N_selected);
            perror("Error while copying the bond builder (trajectory_select_atoms.bond_builder)");
            return;
        }

        return;
    }

    free(src->N_atoms);
    src->N_atoms = N_selected;
    trajectory_delete_atoms(src);
    src->_additional_fields = additional_fields;
    src->atoms = atoms;
    src->_total_atoms = total_selected;
}

void trajectoryfile_select_atoms(struct TrajectoryFile *trajectory_file, const struct Selection selection)
{
    unsigned int N_selections = trajectory_file->N_selections;
    struct Selection *selections = realloc(trajectory_file->selections, (N_selections + 1) * sizeof(struct Selection));
    if (selections == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while reallocating memory (trajectoryfile_select_atoms)");
        return;
    }

    selections[N_selections] = selection;
    N_selections++;

    trajectory_file->N_selections = N_selections;
    trajectory_file->selections = selections;
}

void trajectoryfile_clear_selections(struct TrajectoryFile *trajectory_file)
{
    if (trajectory_file->selections != NULL) free(trajectory_file->selections);
    trajectory_file->selections = NULL;
}
