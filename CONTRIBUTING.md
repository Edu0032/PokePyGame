# Guia de contribuição

Este repositório segue um fluxo simples de desenvolvimento com branches, testes automatizados e revisão antes de merge.

## Ambiente

```bash
python -m venv .venv
pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Fluxo recomendado

1. Criar uma branch a partir de `main`.
2. Fazer alterações pequenas e focadas.
3. Rodar testes e checks locais.
4. Atualizar documentação quando necessário.
5. Abrir pull request descrevendo objetivo, mudanças e validações.

## Commits

Formato recomendado:

```text
feat: nova funcionalidade
fix: correção de bug
refactor: melhoria interna
docs: documentação
test: testes
chore: manutenção
ci: pipeline e automações
```

## Checks locais

```bash
pytest
ruff check PokePY tests
black PokePY tests
mypy PokePY
```

## Banco de dados

Alterações de schema devem vir acompanhadas de migration Alembic.

```bash
alembic revision --autogenerate -m "descricao"
alembic upgrade head
```

## Pull requests

Um pull request deve informar:

- Objetivo da mudança.
- Arquivos ou módulos afetados.
- Como a mudança foi testada.
- Impacto esperado no jogo, API ou banco.
