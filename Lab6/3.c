#include <stdio.h>

extern
int func3(int a, int b, int c, int d, int e, int f, int g){
    printf("%d %d %d %d %d %d %d\n", a, b, c, d, e, f, g);
    return b;
};

// extern
// int func3(int a, int b, int c, int d, int e){
//     printf("%d %d %d %d %d\n", a, b, c, d, e);
//     return b;
// };