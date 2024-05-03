#include "atom.h"
#include "trajectory.h"

#include <errno.h>
#include <math.h>
#include <omp.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

union AtomField *trajectory_get_property(const struct Trajectory trajectory, const unsigned int field, unsigned long *size)
{
    // Preparing the array
    union AtomField *property = calloc(trajectory._total_atoms, sizeof(union AtomField));
    if (property == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_get_property)");
        return NULL;
    }

    size_t offset = trajectory.atom_builder.offsets[field];

    // Transfering the data
    if (trajectory.atom_builder.is_additional[field])
        for (unsigned int a = 0; a < trajectory._total_atoms; a++) property[a] = trajectory._additional_fields[a * trajectory.atom_builder.N_additional + offset];
    else
        for (unsigned int a = 0; a < trajectory._total_atoms; a++)
            property[a] = *(union AtomField *) ((void *) (trajectory.atoms + a) + offset);

    *size = trajectory._total_atoms;
    return property;
}

union AtomField *trajectoryfile_get_property(const struct TrajectoryFile trajectory_file, const unsigned int field, unsigned long *size)
{
    // Preparing the array
    union AtomField *properties = NULL;
    unsigned int properties_size = 0;

    // Preparing to read
    unsigned int N_batches = (unsigned int) floor((double) trajectory_file.N_configurations / trajectory_file.batch_size);
    unsigned int remaining_conf = trajectory_file.N_configurations % trajectory_file.batch_size;

    // Transfering the data
    for (unsigned int batch = 0; batch < N_batches; batch++)
    {
        struct Trajectory trajectory;
        trajectoryfile_read_slice(trajectory_file, trajectory_file.steps[batch * trajectory_file.batch_size], trajectory_file.batch_size,
                                  &trajectory);
        if (errno != 0)  // Could not read slice
        {
            if (properties != NULL) free(properties);
            perror("Error while reading a slice (trajectoryfile_average_property.trajectory)");
            return NULL;
        }

        // Sub-optimal
        unsigned long n_atoms;
        union AtomField *tmp = trajectory_get_property(trajectory, field, &n_atoms);
        if (tmp == NULL)
        {
            if (properties != NULL) free(properties);
            trajectory_delete(&trajectory);
            errno = ENOMEM;
            perror("Error while reallocating memory (trajectoryfile_get_property)");
            return NULL;
        }

        // (Re)Allocating memory
        {
            union AtomField *new_properties = realloc(properties, (properties_size + n_atoms) * sizeof(union AtomField));
            if (new_properties == NULL)  // Could not reallocate memory
            {
                if (properties != NULL) free(properties);
                trajectory_delete(&trajectory);
                errno = ENOMEM;
                perror("Error while reallocating memory (trajectoryfile_get_property)");
                return NULL;
            }
            // properties_size += n_atoms;  // Not now otherwise we won't be able to add the new properties
            properties = new_properties;
        }

        memcpy(properties + properties_size, tmp, n_atoms * sizeof(union AtomField));
        properties_size += n_atoms;
        free(tmp);
        trajectory_delete(&trajectory);
    }

    if (remaining_conf != 0)
    {
        struct Trajectory trajectory;
        trajectoryfile_read_slice(trajectory_file, trajectory_file.steps[N_batches * trajectory_file.batch_size], remaining_conf,
                                  &trajectory);
        if (errno != 0)  // Could not read slice
        {
            free(properties);
            perror("Error while reading a slice (trajectoryfile_average_property.trajectory)");
            return NULL;
        }

        unsigned long n_atoms;
        union AtomField *tmp = trajectory_get_property(trajectory, field, &n_atoms);
        if (tmp == NULL)
        {
            free(properties);
            trajectory_delete(&trajectory);
            errno = ENOMEM;
            perror("Error while reallocating memory (trajectoryfile_get_property)");
            return NULL;
        }

        // (Re)Allocating memory
        {
            union AtomField *new_properties = realloc(properties, (properties_size + n_atoms) * sizeof(union AtomField));
            if (new_properties == NULL)  // Could not reallocate memory
            {
                trajectory_delete(&trajectory);
                free(properties);
                errno = ENOMEM;
                perror("Error while reallocating memory (trajectoryfile_get_property)");
                return NULL;
            }
            // properties_size += n_atoms;  // Not now otherwise we won't be able to add the new properties
            properties = new_properties;
        }

        memcpy(properties + properties_size, tmp, n_atoms * sizeof(union AtomField));
        properties_size += n_atoms;
        free(tmp);
        trajectory_delete(&trajectory);
    }

    *size = properties_size;
    return properties;
}

double *trajectory_average_property(const struct Trajectory trajectory, const unsigned int field)
{
    // Preparing the array
    double *averages = calloc(trajectory.N_configurations, sizeof(double));
    if (averages == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_average_property)");
        return NULL;
    }

    // Checking the type of data
    enum AtomFieldType type = trajectory.atom_builder.fields_types[field];

    // Gathering the data
    unsigned long size;
    union AtomField *properties = trajectory_get_property(trajectory, field, &size);
    if (properties == NULL)  // Something went wrong
    {
        free(averages);
        perror("Error while getting the property (trajectory_average_property)");
        return NULL;
    }

    // Computing the averages
    if (type == AFT_INT)
        for (unsigned int c = 0, n_atoms = 0; c < trajectory.N_configurations; c++)
        {
            for (unsigned int a = 0; a < trajectory.N_atoms[c]; a++, n_atoms++) averages[c] += (double) properties[n_atoms].i;
            averages[c] /= trajectory.N_atoms[c];
        }
    else if (type == AFT_DOUBLE)
        for (unsigned int c = 0, n_atoms = 0; c < trajectory.N_configurations; c++)
        {
            for (unsigned int a = 0; a < trajectory.N_atoms[c]; a++, n_atoms++) averages[c] += properties[n_atoms].d;
            averages[c] /= trajectory.N_atoms[c];
        }
    else  // Can not compute the average of string values
    {
        free(properties);
        free(averages);
        errno = EINVAL;
        perror("Can not compute the average of string values");
        return NULL;
    }

    free(properties);

    return averages;
}

double *trajectoryfile_average_property(const struct TrajectoryFile trajectory_file, const unsigned int field)
{
    // Preparing the array
    double *averages = calloc(trajectory_file.N_configurations, sizeof(double));
    if (averages == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectoryfile_average_property)");
        return NULL;
    }

    // Preparing to read
    unsigned int N_batches = (unsigned int) floor((double) trajectory_file.N_configurations / trajectory_file.batch_size);
    unsigned int remaining_conf = trajectory_file.N_configurations % trajectory_file.batch_size;

    // Transfering the data
    for (unsigned int batch = 0; batch < N_batches; batch++)
    {
        struct Trajectory trajectory;
        trajectoryfile_read_slice(trajectory_file, trajectory_file.steps[batch * trajectory_file.batch_size], trajectory_file.batch_size,
                                  &trajectory);
        if (errno != 0)  // Could not read slice
        {
            trajectory_delete(&trajectory);
            free(averages);
            perror("Error while reading a slice (trajectoryfile_average_property.trajectory)");
            return NULL;
        }

        double *tmp = trajectory_average_property(trajectory, field);
        if (tmp == NULL)
        {
            trajectory_delete(&trajectory);
            free(averages);
            errno = ENOMEM;
            perror("Error while computing the average (trajectoryfile_average_property)");
            return NULL;
        }
        memcpy(averages + batch * trajectory_file.batch_size, tmp, trajectory_file.batch_size * sizeof(double));
        free(tmp);
        trajectory_delete(&trajectory);
    }

    if (remaining_conf != 0)
    {
        struct Trajectory trajectory;
        trajectoryfile_read_slice(trajectory_file, trajectory_file.steps[N_batches * trajectory_file.batch_size], remaining_conf,
                                  &trajectory);
        if (errno != 0)  // Could not read slice
        {
            trajectory_delete(&trajectory);
            free(averages);
            perror("Error while reading a slice (trajectoryfile_average_property.trajectory)");
            return NULL;
        }

        double *tmp = trajectory_average_property(trajectory, field);
        if (tmp == NULL)
        {
            trajectory_delete(&trajectory);
            free(averages);
            errno = ENOMEM;
            perror("Error while computing the average (trajectoryfile_average_property)");
            return NULL;
        }
        memcpy(averages + N_batches * trajectory_file.batch_size, tmp, remaining_conf * sizeof(double));
        free(tmp);
        trajectory_delete(&trajectory);
    }

    return averages;
}
