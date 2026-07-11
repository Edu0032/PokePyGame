# Validação da versão 5.0.0

## Escopo

A validação cobre regras de combate, matchmaking, persistência, API, configuração do cliente, estrutura do executável e integridade do código-fonte.

## Resultados automatizados

| Verificação | Resultado |
| --- | --- |
| Pytest | 46 testes aprovados |
| Cobertura | 40% do projeto completo |
| Ruff | sem erros |
| mypy | sem erros em 86 arquivos |
| `compileall` | aprovado |
| Validador da árvore-fonte | aprovado |
| Build PyInstaller `onedir` | aprovado em Linux |
| Validador do bundle | aprovado |
| Smoke test do código-fonte | processo permaneceu estável |
| Smoke test do bundle | processo permaneceu estável |

A cobertura total inclui telas Pygame e loops interativos, que exigem testes visuais. Regras de negócio, API, SQLAlchemy, configuração, matchmaking e packaging possuem testes automatizados direcionados.

## Casos críticos cobertos

- dois jogadores com o mesmo nome recebem UUIDs multiplayer diferentes;
- criação e cancelamento de tickets;
- pareamento e criação de partida;
- expiração de fila abandonada;
- rejeição de ação fora do turno;
- idempotência de `action_id`;
- bloqueio do especial sem carga;
- bloqueio do básico quando o especial está pronto;
- multiplicador de 35% do especial;
- reset da carga;
- redução de 30% da curva de XP;
- preservação de `false` no JSON de configuração;
- prioridade de configuração em source e bundle;
- rejeição de localhost em build público;
- inclusão da API hospedada no executável;
- separação visual entre diálogo e botões;
- cliente HTTP e gateway multiplayer compatíveis.

## Validação manual antes da release Windows

1. gerar o build em Windows com Python 3.11;
2. executar `scripts/validate_release.py`;
3. extrair o ZIP em uma pasta diferente;
4. abrir duas instâncias;
5. usar o mesmo nome nas duas;
6. confirmar início da partida;
7. executar dois básicos e um especial;
8. conferir ranking e progresso no Supabase;
9. anexar ZIP e checksum à GitHub Release.

## Deploy

A versão 5 altera regras executadas pelo backend. O commit deve ser implantado no Render antes do teste final do multiplayer. O cliente antigo e a API antiga não formam um par compatível para essas regras.
