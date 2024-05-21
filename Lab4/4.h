#pragma once
#include "1.h"

void func_four(unsigned b){
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


    asm (
        "movl %[x], %%eax;" // Загрузить значение x в регистр eax
        "movl %%eax, (%[Ml], %[i], 4);" // Записать значение x в M[i]
        : // Нет выходных операндов
        : [Ml] "r" (Ml), [i] "r" (i), [x] "m" (x) // Входные операнды
        : "%eax", "memory" // Затрагиваемые регистры
    );



    PRINT_ARRAY(Ml, N, "%08hX");

}

void run_func_four(){
    unsigned int num2 = 0xADE1A1DA;
    func_four(num2);
}