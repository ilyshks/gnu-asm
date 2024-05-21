#pragma once
#include "1.h"

void func_eight(int a){
    const int N = 5;
    float Mfs[N];

    // Инициализация массивов
    for(int i = 0; i < N; i++) {
        Mfs[i] = 0;
    }

    // Вывод массивов на экран
    PRINT_ARRAY(Mfs, N, "%f");

    size_t i = 1;


    asm (
        "movl %[a], %%eax\n\t"
        "cvtsi2ss %%eax, %%xmm0\n\t"
        "movss %%xmm0, %[Mfs]\n\t"
        :
        : [a] "r" (a), [Mfs] "m" (Mfs[i])
        : "eax", "xmm0", "memory"
    );

    PRINT_ARRAY(Mfs, N, "%f");

}

void run_func_eight(){
    int num1 = 10;
    func_eight(num1);
}