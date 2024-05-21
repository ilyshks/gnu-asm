.globl main

.data
format: .string "%d"
a: .int 1
b: .int 2
c: .int 3
d: .int 4
// int func3(int a, int b, int c, int d, int e, int f, int g)
.text
main:
    subq $8, %rsp
    // 32 + 3*8 = 32 + 24 = 56
    subq $56, %rsp 

    mov a(%rip), %ecx
    mov b(%rip), %edx
    mov c(%rip), %r8d
    mov d(%rip), %r9d
    
	movq	$5, 32(%rsp)
    movq	$6, 40(%rsp)
    movq	$7, 48(%rsp)
    
    call func3
    

    lea format(%rip), %rcx
    mov %eax, %edx

    call printf

	movl $0, %eax
    addq $56, %rsp
	addq $8, %rsp
    ret
