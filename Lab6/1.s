.globl func
// int func(int x, int y);
// RCX - x
// RDX - y
// RAX - return
func:
    mov %ecx, %eax
    lea -113(%rax, %rdx, 2), %eax
    ret
