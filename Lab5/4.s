.section .data
    format_in: .asciz "%lf %lf"
    format_out: .asciz "You entered: %f and %f\n"

.section .text
.globl main
main:
    subl $16, %esp  
    movl $format_in, %eax  
    leal -16(%ebp), %ebx   
    push %ebx             
    call scanf            
    addl $4, %esp          

    fldl -8(%ebp)          
    fstpl (%esp)           
    fldl -16(%ebp)        
    fstpl 4(%esp)          
    push $format_out     
    call printf            
    addl $16, %esp         

    movl $0, %eax          
    leave                 
    ret
