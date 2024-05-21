.globl main

.data
input: .string "%d"
output: .string "%d "
N: .int 0

.text
main:
    sub $8, %rsp

    pushq	%rbp
    movq	%rsp, %rbp
    subq	$40, %rsp

	movl	$0, -4(%rbp) # i

    lea input(%rip), %rcx # for scanf
    leaq N(%rip), %rdx # for scanf

    call scanf

	jmp	.loop
.iteration:
    movl	-4(%rbp), %eax # i -> EAX
    addl	%eax, %eax # 2*i
    movl	%eax, %edx # 2*i -> EDX

    lea output(%rip), %rcx

    call printf

	addl $1, -4(%rbp) # i += 1
.loop:
    movl	N(%rip), %eax # N -> EAX

	cmpl	%eax, -4(%rbp) # i - N < 0

	jl	.iteration

    addq	$40, %rsp
	add $8, %rsp
    popq	%rbp
	ret
