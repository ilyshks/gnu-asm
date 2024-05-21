#pragma once
#include <stdio.h>

#define PRINT_ARRAY(array, size, mod) \
        for (int i = 0; i < size; ++i) { \
            printf(mod, array[i]); \
            printf("%s", " "); \
        } \
        printf("%s", "\n") \


void func_one(unsigned short a, unsigned int b, long long c){
    const int N = 5;
    unsigned short Ms[N]; unsigned int Ml[N]; long long Mq[N];

    // Инициализация массивов
    for(int i = 0; i < N; i++) {
        Ms[i] = a;
        Ml[i] = b;
        Mq[i] = c;
    }

    // Вывод массивов на экран
    PRINT_ARRAY(Ms, N, "%04hX");
    PRINT_ARRAY(Ml, N, "%08hX");
    PRINT_ARRAY(Mq, N, "%016llX");

    int i = 1;

    asm volatile (
    "movw $16, %0"
    : "=m" (Ms[i])
    : 
    : "memory"
    );

    asm volatile (
    "movl $16, %0"
    : "=m" (Ml[i])
    : 
    : "memory"
    );

    asm volatile (
    "movq $16, %0"
    : "=m" (Mq[i])
    : 
    : "memory"
    );
    PRINT_ARRAY(Ms, N, "%04hX");
    PRINT_ARRAY(Ml, N, "%08hX");
    PRINT_ARRAY(Mq, N, "%016llX");

}

void run_func_one(){
    unsigned short num1 = 0xFADE;
    unsigned int num2 = 0xADE1A1DA;
    long long num3 = 0xC1A551F1AB1E;
    func_one(num1, num2, num3);
}