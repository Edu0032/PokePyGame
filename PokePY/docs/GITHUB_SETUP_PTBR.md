# Publicação no GitHub do zero

## 1. Instalar ferramentas

- Git.
- Python 3.11+.
- Docker Desktop.
- Conta no GitHub.
- Conta no Render.

## 2. Criar repositório local

```bash
git init
git add .
git commit -m "Initial PokePY portfolio release"
```

## 3. Criar repositório no GitHub

1. Abrir GitHub.
2. Criar novo repositório.
3. Nome sugerido: `pokepy`.
4. Marcar como público para portfólio.
5. Não criar README pelo GitHub, pois o projeto já contém README.

## 4. Conectar repositório local

```bash
git remote add origin https://github.com/seu-usuario/pokepy.git
git branch -M main
git push -u origin main
```

## 5. Verificar GitHub Actions

Abrir a aba **Actions** e aguardar a execução do workflow.

O resultado esperado é o pipeline de testes concluído com sucesso.

## 6. Criar deploy no Render

Usar o arquivo:

```text
render.yaml
```

Fluxo recomendado:

1. Render > New + > Blueprint.
2. Selecionar o repositório.
3. Confirmar serviço Web e banco PostgreSQL.
4. Aguardar build e deploy.
5. Abrir `/health` e `/docs`.

## 7. Gerar executável com API pública

```powershell
.\scripts\build_windows.ps1 -ApiUrl "https://sua-api.onrender.com"
```

O pacote ficará em:

```text
dist/
```

## 8. Criar release no GitHub

1. Abrir a aba **Releases**.
2. Selecionar **Draft a new release**.
3. Tag sugerida: `v4.0.0`.
4. Título sugerido: `PokePY v4.0.0 - Portfolio Distribution Release`.
5. Anexar o `.zip` do executável.
6. Descrever mudanças principais:
   - API hospedável no Render;
   - suporte PostgreSQL cloud;
   - executável com PyInstaller;
   - documentação profissional;
   - testes automatizados.

## 9. Fixar no perfil

Depois da publicação:

1. Abrir o perfil do GitHub.
2. Selecionar **Customize your pins**.
3. Fixar o repositório `pokepy`.

## 10. Descrição curta para currículo

```text
PokePY — jogo 2D em Python com API REST, persistência relacional e multiplayer.
Projeto educacional com Pygame, FastAPI, SQLAlchemy, MySQL/PostgreSQL, Docker, Render, Pytest, CI e distribuição por executável com PyInstaller.
```
