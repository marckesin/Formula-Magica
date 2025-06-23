import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st  # type: ignore
import time
import yfinance as yf  # type: ignore
from concurrent.futures import ThreadPoolExecutor


def get_data(ticker):
    update_ticker = ticker.strip() + ".SA"
    try:
        # Obter dados do Yahoo Finance
        acao = yf.Ticker(update_ticker)
        info = acao.info

        # Extrair os dados necessários
        ativo = {
            "Ticker": ticker,
            "Preço": info.get("currentPrice", np.nan),
            "P/L": info.get("trailingPE", np.nan),
            "ROA": info.get("returnOnAssets", np.nan),
            "ROE": info.get("returnOnEquity", np.nan),
            "EV/EBIT": info.get("enterpriseToEbitda", np.nan),
            "Valor Mercado": info.get("marketCap", np.nan),
            "Setor": info.get("sector", np.nan),
            "Subsetor": info.get("industry", np.nan),
        }
        return ativo
    except Exception as e:
        print(f"Erro ao processar {ticker}: {str(e)}")
    finally:
        time.sleep(1)


@st.cache_data
def info_dataframe(tickers):
    with ThreadPoolExecutor(max_workers=7) as executor, st.spinner(
        "Buscando dados...", show_time=True
    ):
        results = list(executor.map(get_data, tickers))
        st.success("Busca de dados finalizada!")

    df = pd.DataFrame(results)
    df.drop_duplicates(keep="first", inplace=True)
    df.dropna(inplace=True, subset=["P/L", "ROA", "ROE", "EV/EBIT"])
    df.reset_index(drop=True, inplace=True)
    df[["ROA", "ROE"]] = df[["ROA", "ROE"]] * 100
    df[["ROA", "ROE", "P/L", "EV/EBIT"]] = df[["ROA", "ROE", "P/L", "EV/EBIT"]].round(2)
    return df


def main():
    st.title("Ranking de Empresas")
    st.write(
        "Extrai dados de ações, aplica a metodologia da "
        "Fórmula Mágica e gera um ranking de melhores empresas."
    )
    st.divider()
    st.subheader("Filtros")

    # Cria os sliders para que o usuário possa filtrar as ações.
    col1, col2 = st.columns(2)

    with col1:
        slider_roa = st.slider("ROA", min_value=0, max_value=100)
        slider_roe = st.slider("ROE", min_value=0, max_value=100)
    with col2:
        slider_pl = st.slider("P/L", min_value=0, max_value=100, value=20)
        slider_ev_ebit = st.slider("EV/EBIT", min_value=1, max_value=100, value=20)

    with open("codigos_acoes.txt", "r") as f:
        tickers = f.read().splitlines()

    df = info_dataframe(tickers)

    # Cria uma cópia do DataFrame para manipulação.
    df2 = df.copy()

    # Define as métricas para o ranking e a direção da ordenação.
    # ascending=True: quanto maior o valor, maior o rank.
    # ascending=False: quanto menor o valor, maior o rank.
    ranking_metrics = {
        "R_ROA": {"column": "ROA", "ascending": True},
        "R_EV_EBIT": {"column": "EV/EBIT", "ascending": False},
        "R_ROE": {"column": "ROE", "ascending": True},
        "R_PL": {"column": "P/L", "ascending": False},
    }

    # Calcula o rank para cada métrica e o adiciona ao DataFrame.
    for rank_col, config in ranking_metrics.items():
        df2[rank_col] = df2[config["column"]].rank(ascending=config["ascending"])

    # Soma os rankings individuais para obter um ranking total.
    df2["Total"] = df2[list(ranking_metrics.keys())].sum(axis=1)

    # Aplica os filtros definidos pelo usuário e outros filtros de qualidade.
    df2 = df2[
        (df2["ROA"] >= slider_roa)
        & (df2["EV/EBIT"] <= slider_ev_ebit)
        & (df2["EV/EBIT"] > 0)
        & (df2["P/L"] > 0)
        & (df2["P/L"] < slider_pl)
        & (df2["ROE"] > slider_roe)
    ]

    # Ordena o DataFrame final pelo ranking total e exibe na tela.
    df2 = df2.iloc[:].sort_values(by=["Total"], ascending=False)
    df2 = df2.reset_index(drop=True)
    st.dataframe(df2, hide_index=True)


if __name__ == "__main__":
    main()
