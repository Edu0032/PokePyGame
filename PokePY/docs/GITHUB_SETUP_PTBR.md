# Publicação correta no GitHub

## Preparar o repositório local

```bash
git init
git status
git add .
git commit -m "Initial portfolio release"
```

## Criar repositório remoto

No GitHub, criar um repositório chamado:

```text
PokePyGame
```

Depois conectar:

```bash
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/PokePyGame.git
git push -u origin main
```

## Conferir antes de divulgar

- README abre corretamente.
- O link de licença aparece.
- O workflow de CI passa.
- A pasta `dist/`, `.venv/`, `__pycache__/`, `.pytest_cache/` e arquivos `.env` não aparecem no GitHub.
- O Render está com `/health` e `/docs` acessíveis.
- O executável foi publicado em Releases.

## Commits recomendados

```bash
git add .
git commit -m "docs: improve practical setup and multiplayer flow"
git commit -m "chore: simplify repository documentation"
git commit -m "build: add hosted API client configuration script"
```

## Atualizar URL da API no código-fonte

Depois do deploy, executar:

```bash
python scripts/configure_api_url.py --api-url "https://SEU-SERVICO.onrender.com"
```

O arquivo `pokepy_client.json` pode ser mantido fora do Git quando contiver URL de ambiente pessoal. Para publicar uma configuração de demonstração, revisar antes de commitar.
