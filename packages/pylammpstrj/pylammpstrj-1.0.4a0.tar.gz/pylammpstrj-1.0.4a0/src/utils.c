#include "utils.h"
#include <ctype.h>
#include <string.h>

void string_remove_newlines(char *str, char chr)
{
    for (int c = strlen(str) - 1; 0 <= c; c--)
        if (str[c] == '\0')
            continue;
        else if (str[c] == '\n')
            str[c] = chr;
}

char *str_go_to_next(const char *str, const char chr)
{
    char *start = (char *) str;
    while (*start != chr && *start != '\0') start++;
    if (*start == '\0') return NULL;
    return ++start;
}

char *str_skip_spaces(const char *str)
{
    char *start = (char *) str;
    while (isspace(*start)) start++;
    if (*start == '\0') return NULL;
    return start;
}

int uint_lt(const void *a, const void *b) { return *(unsigned int *) a < *(unsigned int *) b; }

int uint_leq(const void *a, const void *b) { return *(unsigned int *) a <= *(unsigned int *) b; }

int uint_eq(const void *a, const void *b) { return *(unsigned int *) a == *(unsigned int *) b; }

int uint_geq(const void *a, const void *b) { return *(unsigned int *) a >= *(unsigned int *) b; }

int uint_gt(const void *a, const void *b) { return *(unsigned int *) a > *(unsigned int *) b; }

int double_lt(const void *a, const void *b) { return *(double *) a < *(double *) b; }

int double_leq(const void *a, const void *b) { return *(double *) a <= *(double *) b; }

int double_eq(const void *a, const void *b) { return *(double *) a == *(double *) b; }

int double_geq(const void *a, const void *b) { return *(double *) a >= *(double *) b; }

int double_gt(const void *a, const void *b) { return *(double *) a > *(double *) b; }

int int_lt(const void *a, const void *b) { return *(int *) a < *(int *) b; }

int int_leq(const void *a, const void *b) { return *(int *) a <= *(int *) b; }

int int_eq(const void *a, const void *b) { return *(int *) a == *(int *) b; }

int int_geq(const void *a, const void *b) { return *(int *) a >= *(int *) b; }

int int_gt(const void *a, const void *b) { return *(int *) a > *(int *) b; }

int str_eq(const void *a, const void *b) { return strcmp((char *) a, (char *) b) == 0; }
