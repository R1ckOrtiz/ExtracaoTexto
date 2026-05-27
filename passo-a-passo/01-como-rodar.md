# 01 - Como rodar a aplicacao

Este passo a passo assume que voce esta usando o Windows.

## 1. Abrir a pasta do projeto

Abra o PowerShell e entre na pasta:

```powershell
cd C:\Users\henri\Desktop\ExtracaoTexto
```

## 2. Criar o ambiente Python

Se a pasta `.venv` ainda nao existir, rode:

```powershell
uv venv .venv
```

## 3. Instalar as dependencias

```powershell
uv pip install -r requirements.txt
```

## 4. Rodar a aplicacao

```powershell
.venv\Scripts\streamlit run app.py
```

## 5. Abrir no navegador

Abra este endereco:

```text
http://127.0.0.1:8501
```

Se o terminal mostrar outro endereco, use o endereco exibido no terminal.

