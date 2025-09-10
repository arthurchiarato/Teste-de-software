
#include <stdio.h>

void avaliar_aluno(float nota1, float nota2, float nota3, float nota4) {
    float media = (nota1 + nota2 + nota3 + nota4) / 4.0;

    if (media >= 7.0) {
        printf("O aluno passou com media: %.2f\n", media);
    } else if (media >= 5.0) {
        printf("O aluno esta em final com media: %.2f\n", media);
    } else {
        printf("O aluno foi reprovado com media: %.2f\n", media);
    }
}

int main() {
    float nota1, nota2, nota3, nota4;

    printf("Digite as 4 notas do aluno: ");
    scanf("%f %f %f %f", &nota1, &nota2, &nota3, &nota4);


    avaliar_aluno(nota1, nota2, nota3, nota4);

    return 0;
}
