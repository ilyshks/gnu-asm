#include <stdio.h>


int main(){
    int N = 0;
    scanf("%d", &N);

    for (int i=0; i < N; i++)
        printf("%d ", 2*i);

    return 0;
}