.globl main

.data
# определяем формат ввода
input_16: .string "%hd"
input_32: .string "%d"
input_64: .string "%lld"
input_float: .string "%f"
input_double: .string "%lf"
# определяем формат вывода
output_16: .string "16 bit:\nNumber (short) = %hd\n\n"
output_32: .string "32 bit:\nNumber (int) = %d\n\n"
output_64: .string "64 bit:\nNumber (long long) = %lld\n\n"
output_float: .string "FLOAT:\nNumber = %f\n\n"
output_double: .string "DOUBLE:\nNumber = %lf\n\n"
# переменные, которые инициализируются нулевыми значениями
valx_16: .short 0 
valx_32: .int 0 
valx_64: .quad 0 
valx_float: .float 0.0 
valx_double: .double 0.0 

.text
main:
    sub $8, %rsp
    lea input_16(%rip), %rcx # Загружает адрес input_16 в регистр %rcx.
    leaq valx_16(%rip), %rdx
    sub $32, %rsp # Выделяет место в стеке
    call scanf
    add $32, %rsp # Освобождает выделенное место в стеке.
    xor %eax, %eax
    lea output_16(%rip), %rcx
    movw valx_16(%rip), %dx
    sub $32, %rsp
    call printf
    add $32, %rsp
    xor %eax, %eax

    lea input_32(%rip), %rcx
    leaq valx_32(%rip), %rdx
    sub $32, %rsp
    call scanf
    add $32, %rsp
    xor %eax, %eax
    lea output_32(%rip), %rbx
    movq valx_32(%rip), %rdx
    movq %rbx, %rcx
    sub $32, %rsp
    call printf
    add $32, %rsp
    xor %eax, %eax

    lea input_64(%rip), %rcx
    leaq valx_64(%rip), %rdx
    sub $32, %rsp
    call scanf
    add $32, %rsp
    xor %eax, %eax
    lea output_64(%rip), %rbx
    movq valx_64(%rip), %rdx
    movq %rbx, %rcx
    sub $32, %rsp
    call printf
    add $32, %rsp
    xor %eax, %eax

    lea input_float(%rip), %rcx
    leaq valx_float(%rip), %rdx
    sub $32, %rsp
    call scanf
    add $32, %rsp
    xor %eax, %eax
    lea output_float(%rip), %rcx
    CVTSS2sd valx_float(%rip), %xmm0
    movq %xmm0, %rdx
    sub $32, %rsp
    call printf
    add $32, %rsp
    xor %eax, %eax

    lea input_double(%rip), %rcx
    leaq valx_double(%rip), %rdx
    sub $32, %rsp
    call scanf
    add $32, %rsp
    xor %eax, %eax
    lea output_double(%rip), %rcx
    movsd valx_double(%rip), %xmm0
    movlhps %xmm0, %xmm0
    movq %xmm0, %rdx
    sub $32, %rsp
    call printf
    add $32, %rsp
    xor %eax, %eax

    add $8, %rsp
    ret
