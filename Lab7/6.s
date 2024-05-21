
// void func(int* array, int length){
//     int cnt = 0;
//     for (int i = 0; i < length; i++){
//         array[i] = cnt;
//         cnt += 2;
//     }
// }

.globl task6

.text
task6:
	pushq	%rbp
	movq	%rsp, %rbp

	subq	$16, %rsp

	movq	%rcx, 16(%rbp) # array
	movl	%edx, 24(%rbp) # length
	movl	$0, -4(%rbp) # cnt
	movl	$0, -8(%rbp) # i

	jmp	.loop
.iteration:

	leaq	0(,%rax,4), %rdx # вычисляем сдвиг
	movq	16(%rbp), %rax
	addq	%rax, %rdx # перемещаемся к следующему элементу

	movl	-4(%rbp), %eax # cnt -> EAX
	movl	%eax, (%rdx)  # cnt записали в массив (перемещается ECX в память, на которую указывает RDX)

	addl	$2, -4(%rbp) # cnt += 2
	addl	$1, -8(%rbp) # i += 1
.loop:
	movl	-8(%rbp), %eax # i -> EAX
	cmpl	24(%rbp), %eax # i - length < 0

	jl	.iteration

	addq	$16, %rsp
	popq	%rbp
	ret
    

