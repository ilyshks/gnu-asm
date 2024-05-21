.globl main

.data
# определяем формат ввода
input_pow: .string "%lf%lf"
# определяем формат вывода
output_pow: .string "Pow(x, y) = %lf\n\n"
# переменные, которые инициализируются нулевыми значениями
// valx_double: .double 0.0 # x
// valy_double: .double 0.0 # y

.text
main:
    sub $8, %rsp
    sub $16, %rsp

    lea input_pow(%rip), %rcx # Загружает адрес input_pow в регистр %rcx.

    leaq (%rsp), %rdx # x
    leaq 8(%rsp), %r8 # y

    sub $32, %rsp 
    call scanf
    add $32, %rsp 

    movsd (%rsp), %xmm0 # Загружает значение переменной valx_double в регистр %xmm0.
    movsd 8(%rsp), %xmm1
    sub $32, %rsp 
    call pow
    add $32, %rsp

    lea output_pow(%rip), %rcx # Загружает адрес output_pow в регистр %rcx.

    vmovq %xmm0, %rdx # Перемещает результат вычисления степени из %xmm2 в %rdx.
    vmovsd %xmm0, %xmm0, %xmm1
    sub $32, %rsp
    call printf
    add $32, %rsp

    add $16, %rsp
    add $8, %rsp
    ret
