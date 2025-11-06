
# SGBU - Equipe 3 (Empréstimo e Devolução)

Este repositório implementa o módulo de **Empréstimo e Devolução** do SGBU
(Sistema de Gestão de Biblioteca Universitária), com **backend em Flask + SQLite**,
**frontend simples em HTML/Bootstrap** e **testes (pytest)**.

> Base tecnológica inspirada no projeto demonstrado em aula pelo professor
> (replit "PersonalExpenseOrganizer") – mantivemos **Flask**, camadas simples de
> modelo/rotas e testes automatizados.

## Rodando localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=app/app.py
export FLASK_ENV=development
flask run  # abre em http://127.0.0.1:5000
```

A primeira execução criará `sgbu.db` com as tabelas necessárias. Também criamos
dados de exemplo **apenas** para facilitar a integração/avaliação (1-2 usuários e livros).

## Estrutura

```text
app/
  app.py            # App Flask e rotas
  models.py         # SQLAlchemy models (User, Book, Loan)
  seed.py           # carga de dados exemplo
  templates/        # páginas (Jinja2)
  static/
tests/
  conftest.py
  test_unit_loans.py
  test_contracts.py
```

## Endpoints principais (REST)

- `POST /api/loans` – cria empréstimo `{user_id, book_id, loan_days}`
- `POST /api/loans/<loan_id>/return` – registra devolução
- `GET /api/loans` – lista empréstimos (query: `status=abertos|todos`)
- `GET /api/loans/<loan_id>` – detalhes do empréstimo

### Regras

- Só empresta se `book.available == True`.
- `loan_days` padrão: 7 (se não informado).
- Na devolução, o livro volta a `available=True`.

## Frontend

- Página inicial com atalho para **Emprestar** e **Listar Empréstimos**.
- Formulário simples (select de usuário e livro disponível, dias de empréstimo).
- Tabela de empréstimos com botão **Devolver**.

## Testes (TDD)

Incluímos **10 testes unitários** e **5 testes de contrato/integridade**.
Para executar:

```bash
pytest -q
```

## Observação de Integração

Este módulo **depende** de Usuários e Catálogo. Para facilitar a integração em
laboratório, colocamos `User` e `Book` aqui também (com chaves estrangeiras e regras).
Em produção, você pode apontar para os módulos/serviços reais mantendo os mesmos
contratos de campos (`id`, `name` para `User`; `id`, `title`, `available` para `Book`).

