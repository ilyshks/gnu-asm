#pragma once
#include "1.h"

void func_six(unsigned b){
    unsigned short x = 10;
    unsigned short y = 20;
    printf("%u %u\n", x, y);

    unsigned z = 0;
    unsigned w = 0;

    asm (
        "movw %[x], %%ax;" // Загрузить значение x в регистр ax
        "movw %[y], %%bx;"
        "addw %%bx, %%ax\n\t" // Сложить второе число с ax
        "movw %%ax, %[z]\n\t"
        "movw %[x], %%ax;"
        "subw %%bx, %%ax\n\t"
        "movw %%ax, %[w]\n\t"
        :  [z] "=m" (z), [w] "=m" (w)
        :  [x] "r" (x), [y] "r" (y)
        : "%ax", "%bx", "memory" // Затрагиваемые регистры
    );

    printf("%u %u", z, w);

}

void run_func_six(){
    unsigned int num2 = 0xADE1A1DA;
    func_six(num2);
}