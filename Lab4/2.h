#pragma once
#include "1.h"

void func_two(unsigned short a){
    const int N = 5;
    unsigned short Ms[N];

    // Инициализация массива
    for(int i = 0; i < N; i++) {
        Ms[i] = a;
    }

    // Вывод массива на экран
    PRINT_ARRAY(Ms, N, "%04hX");

    size_t i = 1;

    asm volatile (
    "movw $-1, (%[base], %[index], 2)\n\t"
    :
    : [base] "r" (Ms), [index] "r" (i)
    : "memory"
    );

    PRINT_ARRAY(Ms, N, "%04hX");

}

void run_func_two(){
    unsigned short num1 = 0xFADE;
    func_two(num1);
}