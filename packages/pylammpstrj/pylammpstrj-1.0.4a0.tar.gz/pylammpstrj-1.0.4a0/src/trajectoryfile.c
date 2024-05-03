#include "read.h"
#include "trajectory.h"
#include "utils.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct TrajectoryFile trajectoryfile_new(const char *file_name, const char *user_format, const unsigned int batch_size)
{
    struct TrajectoryFile trajectory_file = {.file_name = {0}, .N_configurations = 0, .conf_pos = NULL};

    // Reading the file
    FILE *input = fopen(file_name, "r");
    if (input == NULL)  // File could not be open
    {
        errno = EIO;
        perror("Error while opening the file (trajectoryfile_new)");
        return trajectory_file;
    }

    // Preparing to read
    char dump[BUFFER_LIMIT] = {0};
    unsigned long N_configurations = 0;
    unsigned long step;
    long pos;

    // Allocating memory
    unsigned long *steps = malloc(BASE_N_CONFIGURATIONS * sizeof(unsigned long));
    if (steps == NULL)
    {
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectoryfile_new.steps)");
        return trajectory_file;
    }
    long *conf_pos = malloc(BASE_N_CONFIGURATIONS * sizeof(long));
    if (conf_pos == NULL)  // Could not allocate memory
    {
        fclose(input);
        errno = ENOMEM;
        perror("Error while allocating memory (trajectoryfile_new)");
        return trajectory_file;
    }
    size_t steps_size = BASE_N_CONFIGURATIONS;

    // Reading
    int chr = fgetc(input);
    while (chr != EOF)
    {
        ungetc(chr, input);

        // Reallocating memory if necessary
        if (N_configurations >= steps_size)
        {
            unsigned long *new_steps = realloc(steps, (steps_size + N_CONFIGURATIONS_INCR) * sizeof(unsigned long));
            if (new_steps == NULL)
            {
                free(conf_pos);
                free(steps);
                fclose(input);
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory "
                    "(trajectoryfile_new.new_steps)");
                return trajectory_file;
            }
            steps = new_steps;

            long *new_conf_pos = realloc(conf_pos, (steps_size + N_CONFIGURATIONS_INCR) * sizeof(long));
            if (new_conf_pos == NULL)  // Could not reallocate memory
            {
                free(conf_pos);
                fclose(input);
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory "
                    "(trajectoryfile_new.new_conf_pos)");
                return trajectory_file;
            }

            steps_size += N_CONFIGURATIONS_INCR;
            conf_pos = new_conf_pos;
        }

        do
        {
            pos = ftell(input);
            if (fgets(dump, BUFFER_LIMIT, input) == NULL && !feof(input))
            {
                free(conf_pos);
                free(steps);
                fclose(input);
                perror("Error while reading a line (trajectoryfile_new.dump)");
                return trajectory_file;
            }
            if (fscanf(input, " %lu ", &step) != 1)
            {
            }                                                             // res doesn't need to be checked
        } while (strcmp(dump, "ITEM: TIMESTEP\n") != 0 && !feof(input));  // it is checked here

        // Reached end of file
        if (feof(input)) break;

        // Saving the data
        steps[N_configurations] = step;
        conf_pos[N_configurations] = pos;
        N_configurations++;

        chr = fgetc(input);
    }
    fclose(input);

    // Resizing the array
    if (steps_size != N_configurations)
    {
        unsigned long *new_steps = realloc(steps, (steps_size + N_CONFIGURATIONS_INCR) * sizeof(unsigned long));
        if (new_steps == NULL)
        {
            free(conf_pos);
            free(steps);
            errno = ENOMEM;
            perror("Error while reallocating memory (trajectoryfile_new.new_steps)");
            return trajectory_file;
        }
        steps = new_steps;

        long *new_conf_pos = realloc(conf_pos, N_configurations * sizeof(long));
        if (new_conf_pos == NULL)  // Could not reallocate memory
        {
            free(conf_pos);
            free(steps);
            errno = ENOMEM;
            perror("Error while reallocating memory (trajectoryfile_new.new_conf_pos)");
            return trajectory_file;
        }

        steps_size = N_configurations;
        conf_pos = new_conf_pos;
    }

    // Copying the data
    strncpy(trajectory_file.file_name, file_name, FILE_NAME_LIMIT);
    trajectory_file.file_name[FILE_NAME_LIMIT - 1] = '\0';
    if (user_format != NULL)  // if a user format is provided
    {
        strncpy(trajectory_file.user_format, user_format, BUFFER_LIMIT);
        trajectory_file.user_format[BUFFER_LIMIT - 1] = '\0';
    }
    else
        trajectory_file.user_format[0] = '\0';  // Disables the user format
    trajectory_file.batch_size = batch_size;
    trajectory_file.N_configurations = N_configurations;
    trajectory_file.steps = steps;
    trajectory_file.conf_pos = conf_pos;
    trajectory_file.selections = NULL;
    return trajectory_file;
}

void trajectoryfile_delete(struct TrajectoryFile *trajectory_file)
{
    trajectoryfile_clear_selections(trajectory_file);
    free(trajectory_file->steps);
    free(trajectory_file->conf_pos);
}
