
#include <stdio.h>

void divisores(int num) {
    printf("Os divisores de %d sao: ", num);
    for (int i = 1; i <= num; i++) {
        if (num % i == 0) {
            printf("%d ", i);
        }
    }
    printf("\n");
}

int main() {
    int numero;

    printf("Digite um numero: ");
    scanf("%d", &numero);

    divisores(numero);

    return 0;
}
