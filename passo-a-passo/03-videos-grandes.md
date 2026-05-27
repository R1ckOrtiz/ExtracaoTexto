# 03 - Videos grandes

Para videos muito pesados, nao envie pelo botao de upload.

Use este fluxo:

1. Copie o video para `C:\Users\henri\Desktop\ExtracaoTexto`.
2. Abra a aplicacao.
3. Selecione o video na lista.
4. Clique em `Transcrever`.

## Limites praticos

Nao existe um limite fixo quando o video esta direto na pasta do projeto.

O que mais importa e:

- Espaco livre no disco.
- Duracao do video.
- Modelo Whisper escolhido.
- Velocidade do processador.

## Espaco usado pelo audio temporario

A aplicacao extrai um audio temporario em WAV.

Como referencia:

```text
1 hora de video = aproximadamente 115 MB de audio temporario
10 horas de video = aproximadamente 1,1 GB de audio temporario
```

Depois da transcricao, o audio temporario fica salvo junto dos resultados.
Se quiser liberar espaco depois, voce pode apagar o arquivo `audio_16khz.wav` das pastas antigas em `transcricoes`.

## Aumentar limite de upload

O limite fica neste arquivo:

```text
.streamlit\config.toml
```

Para 10 GB, use:

```toml
[server]
maxUploadSize = 10240
```

Mesmo assim, para arquivos grandes, usar a pasta do projeto continua sendo mais estavel.

