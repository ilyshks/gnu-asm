#pragma once
#include "1.h"

void func_three(long long c){
    const int N = 5;
    long long Mq[N];

    // Инициализация массива
    for(int i = 0; i < N; i++) {
        Mq[i] = c;
    }

    // Вывод массива на экран
    PRINT_ARRAY(Mq, N, "%016llX");

    size_t i = 0;

    asm volatile (
    "movb $0xBB, 4(%[base], %[index], 2)\n\t"
    :
    : [base] "r" (Mq), [index] "r" (i)
    : "memory"
    );

    PRINT_ARRAY(Mq, N, "%016llX");

}

void run_func_three(){
    long long num3 = 0xC1A551F1AB1E;
    func_three(num3);
}