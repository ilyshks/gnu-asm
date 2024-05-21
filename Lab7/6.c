#include <stdio.h>

extern int task6(int* array, int length);

int main() {
    int N = 0;
    printf("N = ");
    scanf("%d", &N);

    int mas[N] = {};
    task6(mas, N);
    
    for (int i = 0; i < N; i++){
        printf("%d ", mas[i]);
    }

    return 0;
}