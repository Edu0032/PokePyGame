# Build e distribuição do executável

## Arquitetura da distribuição

```text
PokePY.exe -> HTTPS -> API no Render -> PostgreSQL no Supabase
```

O pacote contém cliente, assets, dependências e configuração pública. Banco, senha e `DATABASE_URL` não fazem parte do executável.

## Pré-requisitos

- Windows 10 ou 11;
- Python 3.11;
- Git;
- repositório atualizado;
- API respondendo em `https://pokepygame.onrender.com/health/ready`.

## Preparar ambiente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-build.txt
```

## Verificar API

```powershell
python scripts/check_online_api.py
```

## Gerar build oficial

```powershell
python scripts/build_executable.py --api-url "https://pokepygame.onrender.com" --onedir
```

Não é necessário editar `configure_api_url.py` ou `build_executable.py`. A URL é um argumento do comando.

O script:

1. rejeita localhost em build público;
2. remove `build/`, a distribuição anterior e arquivos `.spec`;
3. cria `pokepy_client.json` com backend `api`, timeout 65 e fallback desativado;
4. incorpora configuração e assets pelo PyInstaller;
5. grava uma cópia da configuração ao lado do executável;
6. gera `BUILD_INFO.json`;
7. compacta a distribuição;
8. calcula SHA-256.

## Saídas

```text
dist/PokePY/
  PokePY.exe
  pokepy_client.json
  BUILD_INFO.json
  _internal/

release/
  PokePY-Windows.zip
  PokePY-Windows.zip.sha256
```

A pasta completa é necessária no modo `--onedir`. Não distribua somente `PokePY.exe`.

## Por que `--onedir`

Jogos carregam imagens, mapas e bibliotecas nativas. A distribuição em pasta reduz tempo de inicialização e torna o carregamento de assets mais previsível. O usuário recebe um único ZIP, extrai e abre o executável.

## Validação

```powershell
python scripts/validate_release.py --distribution dist/PokePY
```

O validador confirma:

- existência da distribuição;
- presença de `pokepy_client.json`;
- URL HTTPS hospedada;
- ausência de localhost;
- backend multiplayer em modo API;
- fallback oficial desativado;
- presença do manifesto.

Teste manual:

1. extrair o ZIP em uma pasta nova;
2. abrir `PokePY.exe`;
3. abrir ranking;
4. concluir uma run e conferir `leaderboard_scores`;
5. abrir duas instâncias;
6. usar o mesmo nome nas duas;
7. confirmar pareamento e combate;
8. confirmar básico, especial, cura e troca.

## Build de desenvolvimento local

Somente para testes:

```powershell
python scripts/build_executable.py --api-url "http://127.0.0.1:8000" --onedir --allow-local-api
```

Não publique essa saída.

## Publicação

`dist/` e `release/` permanecem no `.gitignore`. Binários não devem entrar no histórico normal do repositório.

Código:

```powershell
git add .
git commit -m "release: finalize multiplayer combat and Windows packaging"
git push
```

Tag:

```powershell
git tag v5.0.0
git push origin v5.0.0
```

Na página **Releases**, criar a versão `v5.0.0` e anexar:

```text
release/PokePY-Windows.zip
release/PokePY-Windows.zip.sha256
```

O README usa `/releases/latest`, portanto aponta automaticamente para a release mais nova.
