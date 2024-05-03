#ifndef _BOX_H
#define _BOX_H

/**
 * The length of the `Box` flag.
 *
 * The flag is in the format "xx xx xx". The extra character is the
 * null-terminator.
 */
#define BOX_FLAG_LIMIT 9

/** The length of the `Box` flag read by `scanf`. */
#define BOX_FLAG_SCANF_LIMIT "8"

/** The size of the array that stores the `Box`'s limits. */
#define BOX_BOUNDS_LIMIT 6

/** Structure used to store boxes specifications. */
struct Box
{
    char flag[BOX_FLAG_LIMIT];
    double bounds[BOX_BOUNDS_LIMIT];
};

/** Creates a `Box`. */
struct Box box_new(const char flag[BOX_FLAG_LIMIT], const double bounds[BOX_BOUNDS_LIMIT]);

/** Copies a `Box` to another. */
void box_copy(struct Box *dest, const struct Box src);

#endif
