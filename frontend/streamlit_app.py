import pandas as pd
import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="SabIA Dashboard", layout="wide")
st.title("SabIA - Dashboard Ejecutivo")

st.sidebar.header("Parametros")
periodo = st.sidebar.selectbox(
    "Periodo",
    [
        "2024-01",
        "2024-02",
        "2024-03",
        "2024-04",
        "2024-05",
        "2024-06",
        "2024-07",
        "2024-08",
        "2024-09",
        "2024-10",
        "2024-11",
        "2024-12",
    ],
    index=1,
)
llm = st.sidebar.selectbox("LLM", ["gemini", "openai", "none"], index=0)
run_btn = st.sidebar.button("Generar reporte")


def run_report(selected_periodo: str, selected_llm: str) -> dict:
    payload = {
        "periodo": selected_periodo,
        "llm": None if selected_llm == "none" else selected_llm,
    }
    response = requests.post(f"{BASE_URL}/run", json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def get_latest() -> dict:
    response = requests.get(f"{BASE_URL}/runs/latest", timeout=60)
    response.raise_for_status()
    return response.json()


def show_metrics(kpis: dict) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total productos", kpis.get("total_productos", 0))
    col2.metric("Margen negativo", kpis.get("productos_margen_negativo_count", 0))
    col3.metric("Margen critico", kpis.get("productos_margen_critico_count", 0))


def show_alerts(alerts: list) -> None:
    st.subheader("Alertas")
    if alerts:
        df_alerts = pd.json_normalize(alerts)
        st.dataframe(df_alerts, use_container_width=True)
    else:
        st.info("No hay alertas para este periodo.")


def show_top_chart(items: list, value_key: str, title: str) -> None:
    st.subheader(title)
    df = pd.DataFrame(items)
    if df.empty or value_key not in df.columns:
        st.info("Sin datos disponibles.")
        return
    chart = df.set_index("nombre_producto")[value_key]
    st.bar_chart(chart)


try:
    if run_btn:
        data = run_report(periodo, llm)
    else:
        data = get_latest()
except requests.RequestException as exc:
    st.error(f"Error al consultar la API: {exc}")
    st.stop()

st.subheader("Reporte Ejecutivo")
st.markdown(data.get("executive_report_md", ""))

kpis = data.get("kpis", {})
alerts = data.get("alerts", [])

show_metrics(kpis)
show_alerts(alerts)

show_top_chart(
    kpis.get("top_5_productos_por_contribucion", []),
    "contribucion_total",
    "Top productos por contribucion",
)
show_top_chart(
    kpis.get("top_5_productos_por_perdida", []),
    "perdida_total",
    "Top productos por perdida",
)
