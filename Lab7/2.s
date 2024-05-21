.globl main

.data
input: .string "%u"
output: .string "z = %u\n"
x: .quad 0

.text
main:
    sub $8, %rsp

    lea input(%rip), %rcx
    leaq x(%rip), %rdx

    sub $32, %rsp
    call scanf
    add $32, %rsp

    lea output(%rip), %rcx
    mov x(%rip), %edx
    
    cmp $11, %edx
    setc %al # flag CF (dest - src < 0)
    movzbl	%al, %eax  # Копируем значение из al в eax, заполняя остальные биты eax нулями
    movl	%eax, %edx

    sub $32, %rsp
    call printf
    add $32, %rsp

    add $8, %rsp
    ret
