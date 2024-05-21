.globl main

.data
input: .string "%lf"
output: .string "z = %d"
output_x: .string "x = %f"
x: .double 0
const: .double 11

.text
main:
    sub $8, %rsp

    leaq input(%rip), %rcx
    leaq x(%rip), %rdx

    sub $32, %rsp
    call scanf
    add $32, %rsp

    // lea output_x(%rip), %rcx
    // movsd x(%rip), %xmm0
    // movq %xmm0, %rdx
    // sub $32, %rsp
    // call printf
    // add $32, %rsp

    movsd x(%rip), %xmm0
    movsd const(%rip), %xmm1

    vcomisd	%xmm1, %xmm0 # сравниваем x и 11
	setc	%al
	movzbl	%al, %edx

    lea output(%rip), %rcx

    sub $32, %rsp
    call printf
    add $32, %rsp

    add $8, %rsp
    ret
