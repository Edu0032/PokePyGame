# Build e distribuição do executável

## Objetivo

Distribuir o jogo para usuários que não querem instalar Python, dependências ou banco de dados local.

## Arquitetura da versão distribuível

```text
PokePY.exe -> API hospedada no Render -> PostgreSQL no Render
```

O executável contém:

- código do cliente;
- assets do jogo;
- dependências necessárias;
- arquivo `pokepy_client.json` com a URL da API.

O executável não contém banco de dados.

## Gerar executável no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-build.txt
python scripts/build_executable.py --api-url "https://SEU-SERVICO.onrender.com"
```

O resultado fica em:

```text
dist/
```

## Gerar usando script PowerShell

```powershell
.\scriptsuild_windows.ps1 -ApiUrl "https://SEU-SERVICO.onrender.com"
```

## Testar antes de publicar

1. Abrir o executável.
2. Concluir uma partida.
3. Verificar se o ranking aparece.
4. Abrir duas instâncias.
5. Entrar no modo online nas duas.
6. Confirmar criação de partida multiplayer.
7. Validar `/docs` da API hospedada.

## Publicar no GitHub Releases

1. Ir até a página do repositório.
2. Abrir **Releases**.
3. Criar uma nova tag, por exemplo `v1.0.0`.
4. Anexar o `.zip` com o conteúdo de `dist/`.
5. Inserir instruções curtas de execução.
