# 05 - Publicar no Streamlit

Antes de publicar, confira se nenhum arquivo sensivel vai para o GitHub.

## Arquivos que nao devem subir

O arquivo `.gitignore` ja bloqueia:

```text
uploads/
transcricoes/
.venv/
__pycache__/
.streamlit/secrets.toml
videos e audios
```

Isso evita subir videos, audios, transcricoes e secrets.

## Conferir antes de enviar para o GitHub

Se o projeto estiver em um repositorio Git, rode:

```powershell
git status
```

Verifique se aparecem apenas arquivos do aplicativo, como:

```text
app.py
transcriber.py
requirements.txt
README.md
.gitignore
.streamlit/config.toml
passo-a-passo/
```

Nao devem aparecer:

```text
uploads/
transcricoes/
*.mkv
*.mp4
*.wav
*.srt
```

## Publicar

1. Suba o projeto para um repositorio no GitHub.
2. Abra o Streamlit Community Cloud.
3. Crie um novo app apontando para o repositorio.
4. Use `app.py` como arquivo principal.

## Importante

A aplicacao publicada no Streamlit nao deve receber videos sigilosos se o ambiente nao for privado e controlado.

Para dados sensiveis, prefira rodar localmente ou publicar em um ambiente privado.
