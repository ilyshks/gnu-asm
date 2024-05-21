.globl main

.data
input: .string "%d"
output: .string "z = %d\n"
x: .int 0

.text
main:
    sub $8, %rsp

    lea input(%rip), %rcx
    leaq x(%rip), %rdx

    sub $32, %rsp
    call scanf
    add $32, %rsp

    mov x(%rip), %rdx

    lea 23(%rdx, %rdx, 4), %eax

    lea output(%rip), %rcx
    mov %eax, %edx

    mov $-1, %eax

    cmp $5, %edx
    cmovle %eax, %edx

    //cmovna %eax, %edx # for unsigned

    sub $32, %rsp
    call printf
    add $32, %rsp

    add $8, %rsp
    ret
