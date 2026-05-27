# 04 - Problemas comuns

## O comando streamlit nao abre

Rode usando o caminho completo:

```powershell
.venv\Scripts\streamlit run app.py
```

## A aplicacao nao abre no navegador

Verifique se o terminal mostra este endereco:

```text
http://127.0.0.1:8501
```

Se a porta 8501 estiver ocupada, rode em outra porta:

```powershell
.venv\Scripts\streamlit run app.py --server.port 8502
```

Depois abra:

```text
http://127.0.0.1:8502
```

## O primeiro uso demora

Isso e normal. O Whisper baixa o modelo na primeira vez.

Depois o mesmo modelo fica salvo em cache e abre mais rapido.

## O video demora muito para transcrever

Use um modelo menor:

```text
tiny ou base
```

Tambem prefira deixar `Precisao` como:

```text
int8
```

## Erro usando cuda

Use `cpu` se a maquina nao tiver GPU NVIDIA configurada.

Na maioria dos casos, a configuracao mais segura e:

```text
Dispositivo: cpu
Precisao: int8
```

