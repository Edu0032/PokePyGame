# Changelog

## 5.0.0 — Final portfolio release

### Multiplayer

- Identificação de rede separada do nome visível por UUID de sessão.
- Matchmaking compatível com jogadores de mesmo nome.
- Expiração e cancelamento de tickets abandonados.
- Validação autoritativa de turno, carga e ação.
- Interface online baseada na mesma apresentação visual do modo história.
- Cenário de batalha determinado por partida.
- Histórico idempotente por `action_id`.

### Combate e progressão

- Ataque especial liberado após dois ataques básicos.
- Alternância visual entre botão básico e especial.
- Bônus de 35% no dano especial.
- Curva de XP reduzida em 30%.
- Regras compartilhadas entre história e multiplayer.
- Caixa de diálogo posicionada acima da área de ações.

### Cliente

- Ranking disponível pelo botão no mapa e pela tecla `R`.
- Diagnóstico de falhas online com URL efetivamente carregada.
- Configuração pública com timeout de 65 segundos e fallback local desativado.

### Distribuição

- URL hospedada incorporada no bundle PyInstaller.
- Bloqueio de builds públicos com localhost.
- Limpeza automática de builds anteriores.
- Geração automática de ZIP e SHA-256.
- Validador de distribuição e manifesto `BUILD_INFO.json`.

### Qualidade

- Testes de combate, matchmaking, HTTP, configuração e packaging.
- Formatação e lint com Ruff.
- Análise estática com mypy.
- Documentação de fluxo, banco, API e release revisada.

## 4.1.0 — Render/Supabase distribution release

- API configurada no Render.
- PostgreSQL hospedado no Supabase.
- Cliente configurado para consumir `https://pokepygame.onrender.com`.
- Dependências separadas para cliente, API, desenvolvimento e build.
