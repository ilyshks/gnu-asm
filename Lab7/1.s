.globl main

.data
input: .string "%d %d"
output: .string "z = %d\nw = %d"
x: .int 0
y: .int 0

.text
main:
    sub $8, %rsp

    lea input(%rip), %rcx
    leaq x(%rip), %rdx
    leaq y(%rip), %r8

    sub $32, %rsp
    call scanf
    add $32, %rsp

    lea output(%rip), %rcx
    mov x(%rip), %edx
    mov y(%rip), %r8d

    add %r8d, %edx
    cmp $0, %edx
    setz %r8b # flag ZF (dest - src = 0)
    movzbl	%r8b, %r8d  # Копируем значение из al в eax, заполняя остальные биты eax нулями

    sub $32, %rsp
    call printf
    add $32, %rsp

    add $8, %rsp
    ret
