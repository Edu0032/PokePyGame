# Checklist de release para portfólio

## Código

- [ ] Testes passando com `pytest`.
- [ ] Cobertura gerada com `pytest --cov=PokePY`.
- [ ] Lint sem erros com `ruff check PokePY tests`.
- [ ] Formatação validada com `black --check PokePY tests`.
- [ ] Imports e módulos sem arquivos temporários.
- [ ] Nenhuma credencial real commitada.

## API

- [ ] Deploy no Render concluído.
- [ ] `/health` retornando `ok`.
- [ ] `/health/ready` retornando `ready`.
- [ ] `/docs` acessível.
- [ ] Migrations aplicadas com Alembic.
- [ ] Ranking cria e lista entradas.
- [ ] Progresso salva e carrega jogador.
- [ ] Matchmaking cria partida entre dois clientes.

## Executável

- [ ] Build gerado por `scripts/build_executable.py`.
- [ ] URL da API correta no build.
- [ ] Jogo abre em máquina limpa.
- [ ] Ranking online funciona.
- [ ] Progresso online funciona.
- [ ] Multiplayer funciona com duas instâncias.
- [ ] Arquivo `.zip` anexado à release do GitHub.

## GitHub

- [ ] README com badges e documentação principal.
- [ ] `LICENSE` presente.
- [ ] `CONTRIBUTING.md` presente.
- [ ] `SECURITY.md` presente.
- [ ] `CHANGELOG.md` atualizado.
- [ ] `EVALUATOR_GUIDE.md` disponível.
- [ ] Release criada com tag semântica.
- [ ] Prints/GIF adicionados quando disponíveis.

## Demonstração

- [ ] GIF do gameplay.
- [ ] Print da documentação `/docs`.
- [ ] Print do ranking.
- [ ] Print ou GIF do multiplayer.
- [ ] Descrição curta para currículo.
