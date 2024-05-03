#include "box.h"

#include <string.h>

// To build a new box
struct Box box_new(const char flag[BOX_FLAG_LIMIT],
                   const double bounds[BOX_BOUNDS_LIMIT])
{
    struct Box box;
    strncpy(box.flag, flag, BOX_FLAG_LIMIT - 1);
    box.flag[BOX_FLAG_LIMIT - 1] = '\0';
    memcpy(box.bounds, bounds, BOX_BOUNDS_LIMIT * sizeof(double));
    return box;
}

// To copy a box to another
void box_copy(struct Box *dest, const struct Box src)
{
    strncpy(dest->flag, src.flag, BOX_FLAG_LIMIT);
    memcpy(dest->bounds, src.bounds, BOX_BOUNDS_LIMIT * sizeof(double));
}
