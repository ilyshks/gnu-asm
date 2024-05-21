#include <stdio.h>

extern int func(int x, int y);


int main(){
    int x = 2; int y = 3;
    printf("Asm result = %d\n", func(x, y));
    printf("C result = %d\n", x + 2*y - 113);
    return 0;
}