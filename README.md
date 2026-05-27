# Extracao de texto de video

Aplicacao simples em Streamlit para extrair audio de videos e transcrever com Whisper local.

## Como rodar

```powershell
uv venv .venv
uv pip install -r requirements.txt
.venv\Scripts\streamlit run app.py
```

Depois abra o endereco mostrado no terminal.

## Passo a passo

Tambem existe uma pasta com guias separados:

- `passo-a-passo/01-como-rodar.md`
- `passo-a-passo/02-como-transcrever-videos.md`
- `passo-a-passo/03-videos-grandes.md`
- `passo-a-passo/04-problemas-comuns.md`
- `passo-a-passo/05-publicar-no-streamlit.md`

## Uso

- Selecione um video que ja esteja na pasta do projeto, ou envie um arquivo pela tela.
- Clique em `Transcrever`.
- A transcricao sera exibida na tela e salva em `transcricoes/`.
- Cada execucao gera `transcricao.txt`, `transcricao.srt`, `segmentos.json` e o audio temporario `audio_16khz.wav`.

## Observacoes

- O primeiro uso baixa o modelo Whisper escolhido.
- `base` e um bom equilibrio para comecar. `tiny` e mais rapido; `small`, `medium` e `large-v3` tendem a ser melhores e mais lentos.
- A aplicacao usa `imageio-ffmpeg`, entao nao precisa instalar `ffmpeg` manualmente.
