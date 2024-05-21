.globl func2
// double func2(double x, double y);
// XMM0 - x
// XMM1 - y
// XMM0 - return
func2:
    vsubsd %xmm1, %xmm0, %xmm0
    ret
