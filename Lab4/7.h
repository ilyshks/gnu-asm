#pragma once
#include "1.h"

void func_seven(float a){
    const int N = 5;
    float Mfs[N];
    // Инициализация массивов
    for(int i = 0; i < N; i++) {
        Mfs[i] = 0;
    }

    // Вывод массивов на экран
    PRINT_ARRAY(Mfs, N, "%f");
    //PRINT_ARRAY(Mfl, N, "%lf");

    size_t i = 1;

    asm(
        "movss %1, %%xmm1\n\t" // Перемещение значения float в регистр xmm0
        "movss %%xmm1, %0\n\t" // Перемещение значения из xmm1 в массив
        : 
        : [M] "m" (Mfs[i]), [a] "m" (a) // Входные операнды
        : "%xmm1", "memory" // Затрагиваемые регистры
    );

    PRINT_ARRAY(Mfs, N, "%f");
    //PRINT_ARRAY(Mfl, N, "%lf");

}

void run_func_seven(){
    float num1 = 1.23;
    func_seven(num1);
}