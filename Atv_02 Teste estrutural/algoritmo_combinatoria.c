
#include <stdio.h>

long long fatorial(int n) {
    long long resultado = 1;
    for (int i = 1; i <= n; i++) {
        resultado *= i;
    }
    return resultado;
}

long long combinatoria(int n, int k) {
    return fatorial(n) / (fatorial(k) * fatorial(n - k));
}

int main() {
    int n, k;
   
    printf("Digite os valores de n (n < k) e k: ");
    scanf("%d %d", &n, &k);

    if (n >= k) {
        printf("Erro: n deve ser menor que k.\n");
    } else {

        printf("A combinatoria de %d elementos tomados %d a %d e: %lld\n", n, k, k, combinatoria(n, k));
    }

    return 0;
}
