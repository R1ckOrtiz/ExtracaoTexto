# 02 - Como transcrever videos

## Opcao recomendada para videos grandes

Coloque o video direto dentro desta pasta:

```text
C:\Users\henri\Desktop\ExtracaoTexto
```

Depois abra a aplicacao e selecione o video na lista.

Essa opcao e melhor para arquivos pesados porque evita o upload pelo navegador.

## Opcao para videos menores

Na tela da aplicacao:

1. Selecione `Enviar arquivo`.
2. Escolha o video.
3. Clique em `Transcrever`.

O limite atual de upload pela tela e de 2 GB.

## Configuracao recomendada

Para comecar, use:

```text
Modelo Whisper: base
Idioma: pt
Dispositivo: cpu
Precisao: int8
Filtrar silencio: ligado
```

Se quiser mais velocidade, use `tiny`.

Se quiser mais qualidade, tente `small`, `medium` ou `large-v3`, mas eles demoram mais.

## Onde ficam os resultados

As transcricoes ficam na pasta:

```text
transcricoes
```

Cada execucao gera uma nova pasta com:

```text
transcricao.txt
transcricao.srt
segmentos.json
audio_16khz.wav
```

