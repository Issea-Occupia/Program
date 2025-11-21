#include <stdio.h>
#include <stdlib.h>

struct Point;

typedef struct {
    void (*move)(struct Point *self, int dx, int dy);
    void (*print)(struct Point *self);
} PointMethods;

typedef struct Point {
    int x;
    int y;
    PointMethods *vptr;
} Point;

void Point_move(Point *self, int dx, int dy) {
    self->x += dx;
    self->y += dy;
}

void Point_print(Point *self) {
    printf("Point(%d, %d)\n", self->x, self->y);
}

PointMethods point_methods = {
    .move = Point_move,
    .print = Point_print
};

Point *Point_new(int x, int y) {
    Point *obj = (Point*)malloc(sizeof(Point));

    obj->x = x;
    obj->y = y;
    obj->vptr = &point_methods;
    return obj;
}

void Point_delete(Point *self) {
    free(self);
}

int main() {
    Point *p = Point_new(3, 4);
    Point *p1 = p;
    p->vptr->print(p);
    p->vptr->move(p, 10, 20);
    p->vptr->print(p);
    p1->vptr->print(p1);
    p1->vptr->move(p1, -5, -5);
    p->vptr->print(p);
    Point_delete(p);
}
