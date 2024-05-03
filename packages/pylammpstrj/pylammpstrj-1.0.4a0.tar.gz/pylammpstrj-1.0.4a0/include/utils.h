/**
 * \file
 * Contains the utilities' prototypes and definitions.
 *
 * Contains the trajectory, box, atom definitions as well as
 * their `define`s, and their functions.
 */
#ifndef _UTILS_H
#define _UTILS_H

#include <stdio.h>

/** The maximum number of characters read at once. */
#define BUFFER_LIMIT 192

/** */
#define FILE_NAME_LIMIT FILENAME_MAX

/** An enum to compare `Atom`s properties. */
// enum Operator
// {
//     OPERATOR_LT,
//     OPERATOR_LEQ,
//     OPERATOR_EQ,
//     OPERATOR_GEQ,
//     OPERATOR_GT
// };

/** Replaces all new line characters in `str` by `chr`. */
void string_remove_newlines(char *str, char chr);

/** Go to next occurence of character. */
char *str_go_to_next(const char *str, const char chr);

char *str_skip_spaces(const char *str);

int uint_lt(const void *a, const void *b);
int uint_leq(const void *a, const void *b);
int uint_eq(const void *a, const void *b);
int uint_geq(const void *a, const void *b);
int uint_gt(const void *a, const void *b);

int double_lt(const void *a, const void *b);
int double_leq(const void *a, const void *b);
int double_eq(const void *a, const void *b);
int double_geq(const void *a, const void *b);
int double_gt(const void *a, const void *b);

int int_lt(const void *a, const void *b);
int int_leq(const void *a, const void *b);
int int_eq(const void *a, const void *b);
int int_geq(const void *a, const void *b);
int int_gt(const void *a, const void *b);

int str_eq(const void *a, const void *b);

#endif
