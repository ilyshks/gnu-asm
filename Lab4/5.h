#pragma once
#include "1.h"

void func_five(unsigned b){
    const int N = 5;
    unsigned int Ml[N];

    // Инициализация массива
    for(int i = 0; i < N; i++) {
        Ml[i] = b;
    }

    // Вывод массива на экран
    PRINT_ARRAY(Ml, N, "%08hX");

    size_t i = 1;
    unsigned int x = 0x1234;

    unsigned int* p = &x;

    asm (
        "movl (%1), %%eax;" // Загрузить значение x в регистр eax
        "movl %%eax, %0;" // Записать значение x в M[i]
        : // Нет выходных операндов
        : [Ml] "m" (Ml[i]), [p] "r" (p) 
        : "%eax", "memory" // Затрагиваемые регистры
    );

    PRINT_ARRAY(Ml, N, "%08hX");

}

void run_func_five(){
    unsigned int num2 = 0xADE1A1DA;
    func_five(num2);
}