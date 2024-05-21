#include <stdio.h>

extern double func2(double x, double y);


int main(){
    double x = 15.456; double y = 12.345;
    printf("Asm result = %lf\n", func2(x, y));
    printf("C result = %lf\n", x - y);
    return 0;
}