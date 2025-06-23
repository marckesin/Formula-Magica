# Ranking de Ações - Fórmula Mágica

Este é um simples aplicativo web construído com [Streamlit](https://streamlit.io/) que busca dados de ações da bolsa de valores brasileira (B3) a partir da API Yahoo Finance.

Ele aplica uma metodologia de ranking inspirada na "Fórmula Mágica" de Joel Greenblatt para classificar as melhores empresas com base em indicadores fundamentalistas.

## ✨ Features

- Busca de dados de ações em tempo real.
- Cálculo de múltiplos fundamentalistas (ROA, ROE, P/L, EV/EBIT, etc.).
- Ranking de ações com base na combinação de múltiplos.
- Filtros interativos para refinar a busca por empresas.
- Interface web simples e intuitiva.

## 🚀 Como Executar

1.  Navegue até o diretório onde o arquivo `app.py` está localizado.

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    pip install pipenv
    ```

3.  **Instale as dependências:**
    ```bash
    pipenv sync
    ```

4.  **Inicie o shell:**
    ```bash
    pipenv shell
    ```

5.  **Execute o aplicativo:**
    ```bash
    streamlit run app.py
    ```

Acesse `http://localhost:8501` no seu navegador.

