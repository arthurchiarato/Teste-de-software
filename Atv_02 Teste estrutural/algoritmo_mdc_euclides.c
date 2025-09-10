
#include <stdio.h>

int mdc_euclides(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int numero1, numero2;

    printf("Digite o primeiro nÃºmero: ");
    scanf("%d", &numero1);

    printf("Digite o segundo nÃºmero: ");
    scanf("%d", &numero2);

    printf("O MÃ¡ximo Divisor Comum (MDC) de %d e %d Ã©: %d\n", numero1, numero2, mdc_euclides(numero1, numero2));

    return 0;
}
