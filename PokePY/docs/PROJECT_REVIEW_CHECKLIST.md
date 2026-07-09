# Checklist de revisão profissional

## Código

- [ ] Arquivos extensos evitados ou justificados.
- [ ] Classes com responsabilidade clara.
- [ ] Regras de negócio fora de rotas e views.
- [ ] Nomes claros para módulos, classes e funções.
- [ ] Type hints em funções públicas.
- [ ] Exceções específicas para regras de negócio.
- [ ] Configurações fora do código rígido.

## Arquitetura

- [ ] Separação entre domínio, serviços, infraestrutura, UI e API.
- [ ] State Machine controlando fluxo do jogo.
- [ ] Repository Pattern aplicado à persistência.
- [ ] API desacoplada do cliente Pygame.
- [ ] Multiplayer com servidor validando ações.
- [ ] Evolução para WebSocket documentada.

## Banco de dados

- [ ] Tabelas versionadas por migration.
- [ ] URL de banco em variável de ambiente.
- [ ] Testes sem dependência obrigatória de MySQL real.
- [ ] Repositórios isolando SQLAlchemy.

## API

- [ ] Schemas Pydantic para entrada e saída.
- [ ] Rotas separadas por domínio.
- [ ] Status codes coerentes.
- [ ] Tratamento de erros padronizado.
- [ ] Documentação interativa disponível em `/docs`.

## Testes

- [ ] Pytest configurado.
- [ ] Fixtures reutilizáveis.
- [ ] Testes de ranking.
- [ ] Testes de progresso.
- [ ] Testes de matchmaking.
- [ ] Testes de ação multiplayer.
- [ ] Testes de idempotência.
- [ ] Testes rodando no CI.

## Repositório

- [ ] README com visão geral, stack, execução e arquitetura.
- [ ] Documentação técnica separada.
- [ ] Templates de issue e pull request.
- [ ] SECURITY.md.
- [ ] CONTRIBUTING.md.
- [ ] CHANGELOG.md.
- [ ] `.env.example` sem credenciais reais.
- [ ] `.gitignore` cobrindo cache, ambiente virtual e arquivos locais.

## Demonstração

- [ ] Jogo roda localmente.
- [ ] API sobe via Docker Compose.
- [ ] `/docs` abre no navegador.
- [ ] Dois clientes conseguem entrar em matchmaking.
- [ ] Ranking persiste tempo.
- [ ] Progresso salva e carrega.
