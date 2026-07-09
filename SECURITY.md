# Política de segurança

## Escopo

Esta política cobre código Python, API FastAPI, configuração Docker, uso de variáveis de ambiente e persistência de dados do PokePY.

## Boas práticas

- Não versionar arquivos `.env` com credenciais reais.
- Usar `.env.example` apenas com valores de exemplo.
- Evitar exposição de stack trace em respostas HTTP.
- Manter dependências atualizadas.
- Revisar alterações em endpoints e persistência.
- Ativar Dependabot alerts, secret scanning e branch protection no GitHub.

## Reporte

Vulnerabilidades devem ser reportadas por issue privada ou canal definido pelo mantenedor do repositório.

Inclua, quando possível:

- Descrição do problema.
- Passos para reprodução.
- Impacto esperado.
- Ambiente usado.
- Sugestão de correção, se houver.
