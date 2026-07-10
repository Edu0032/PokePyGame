# Build e distribuição do executável

## Objetivo

Distribuir o PokePY para usuários que não querem instalar Python, dependências, API local ou banco de dados.

A versão distribuível usa a arquitetura:

```text
PokePY.exe -> API hospedada no Render -> PostgreSQL no Supabase
```

O executável contém:

- código do cliente;
- assets do jogo;
- dependências necessárias para o cliente;
- `pokepy_client.json` com a URL pública da API.

O executável não contém banco de dados.

## Pré-requisitos no Windows

Instalar:

- Python 3.11;
- Git;
- ambiente virtual Python;
- dependências de build do projeto.

Na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements-build.txt
```

## Configurar URL da API

A API pública usada nesta versão é:

```text
https://pokepygame.onrender.com
```

Gravar a URL nos arquivos de configuração:

```powershell
python scripts/configure_api_url.py --api-url "https://pokepygame.onrender.com"
```

Arquivos atualizados:

```text
pokepy_client.json
packaging/pokepy_client.json
```

## Gerar executável

Recomendação para jogos com assets: usar distribuição em pasta (`--onedir`). Esse formato facilita o carregamento de imagens e reduz problemas comuns de empacotamento.

```powershell
python scripts/build_executable.py --api-url "https://pokepygame.onrender.com" --onedir
```

O resultado fica em:

```text
dist/
```

Normalmente será criada uma pasta parecida com:

```text
dist/PokePY/
```

## Testar antes de publicar

Copiar a pasta gerada para outro local e testar como usuário final:

1. Abrir `PokePY.exe`.
2. Verificar se a janela do jogo abre.
3. Criar nome de treinador.
4. Jogar até registrar ranking ou progresso.
5. Abrir duas instâncias.
6. Entrar no multiplayer nas duas.
7. Confirmar se a API online recebe as ações.

Também testar a API no navegador:

```text
https://pokepygame.onrender.com/health
https://pokepygame.onrender.com/health/ready
https://pokepygame.onrender.com/docs
```

## Compactar para distribuição

Compactar a pasta gerada dentro de `dist/`, por exemplo:

```text
PokePY-Windows.zip
```

O arquivo compactado deve conter a pasta ou os arquivos necessários para abrir o jogo.

## Onde publicar o executável

O local recomendado é **GitHub Releases**, não a raiz do repositório.

Fluxo recomendado:

1. Fazer commit das alterações do código e da configuração.
2. Enviar para o GitHub.
3. Criar uma tag, por exemplo `v1.0.0`.
4. Criar uma Release no GitHub.
5. Anexar `PokePY-Windows.zip` como asset da Release.

Exemplo de texto para a Release:

```text
PokePY v1.0.0 - Windows

Versão executável do cliente PokePY para Windows.
A aplicação já vem configurada para consumir a API hospedada em https://pokepygame.onrender.com.
Não é necessário instalar Python, banco de dados ou executar a API localmente.
```

## Atualizar README após publicar

Depois de criar a Release, o README deve apontar para:

```text
https://github.com/Edu0032/PokePyGame/releases/latest
```

Esse link sempre direciona para a versão mais recente publicada.
