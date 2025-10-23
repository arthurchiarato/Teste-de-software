
# TecLearn TABAJARA – Equipe 3 (Empréstimo & Devolução)

Projeto mínimo em Python para praticar **Teste de Integração** com foco no módulo de Empréstimos, integrando com os módulos de Usuários e Catálogo por meio de repositórios em memória.

## Como rodar

1. Crie um ambiente e instale o pytest:
   ```bash
   python -m venv .venv && . .venv/bin/activate
   pip install pytest
   ```
2. Execute os testes:
   ```bash
   pytest
   ```

## TDD (formato de commits)

- `[TDD red] descrição do teste`
- `[TDD green] descrição do teste`
- `[TDD refactor] descrição`

Implemente os testes primeiro, rode, veja falhar (red), implemente a menor mudança para passar (green), e depois refatore com segurança.

## Regras implementadas

- Limite de empréstimos: aluno = 3, professor = 5
- Prazo: aluno = 14 dias, professor = 28 dias
- Não permitir empréstimo se não houver exemplares
- Não permitir o mesmo usuário pegar o mesmo livro enquanto houver empréstimo ativo
- Devolução incrementa estoque
