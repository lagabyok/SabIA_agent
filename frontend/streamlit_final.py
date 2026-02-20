import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import base64
st.set_page_config(page_title="SabIA - Copiloto Inteligente", layout="wide", initial_sidebar_state="collapsed")

CHART_COLORS = {
    "positive": "#2A9D8F",
    "negative": "#E76F51",
    "accent": "#667eea",
    "bar_light": "#8ECAE6",
    "bar_mid": "#5AA9E6",
    "bar_dark": "#1C4A72",
}


def style_plotly(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#061326", size=12),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def render_sabi_table(df: pd.DataFrame, table_class: str = "", escape_html: bool = True):
    classes = "sabi-table" if not table_class else f"sabi-table {table_class}"
    st.markdown(
        f'<div class="sabi-table-wrap">{df.to_html(index=False, classes=classes, border=0, escape=escape_html)}</div>',
        unsafe_allow_html=True,
    )

# CSS minimalista
st.markdown("""
    <style>
    :root {
        /* ===== Tema de tablas (edita aquí para cambiar estilo global) ===== */
        --sabi-text: #061326;
        /* Fondo cabecera (primera fila) */
        --table-header-bg: #B8B68F;
        /* Borde principal de cabecera */
        --table-header-border: #4F4E34;
        /* Línea inferior de cabecera para contraste */
        --table-header-bottom: #3F3E2A;
        /* Fondo del cuerpo de tabla */
        --table-body-bg: #eef3fa;
        /* Bordes de celdas */
        --table-cell-border: #6f8fb3;
    }
    html {
        font-size: clamp(15px, 1vw + 10px, 18px) !important;
    }
    body, .stApp {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: clamp(15px, 0.8vw + 11px, 18px);
        color: var(--sabi-text) !important;
        line-height: 1.5;
    }
    .stApp *:not(svg):not(path) {
        color: var(--sabi-text) !important;
    }
    .stApp {
        font-size: 1rem !important;
    }
    h1, h2, h3 {
        font-size: 1.3rem !important;
        color: var(--sabi-text) !important;
    }
    h4, h5, h6 {
        font-size: 1.15rem !important;
        color: var(--sabi-text) !important;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessageContent"] p,
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricValue"] div,
    [data-testid="stDataFrame"] div {
        font-size: 1rem !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #B8B68F !important;
        color: var(--sabi-text) !important;
    }
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    section.main,
    .main,
    .block-container {
        background-color: #EBE6D2  !important;
        color: var(--sabi-text) !important;
    }
    [data-testid="stHeader"] {
        background: #B8B68F !important;
        min-height: 6.4rem !important;
    }
    [data-testid="stHeader"] > div {
        min-height: 6.4rem !important;
    }
    [data-testid="stSidebar"] {
        background-color: #eaf0f7 !important;
    }
    p, li, label, .stMarkdown, .stCaption,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: var(--sabi-text) !important;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: var(--sabi-text) !important;
    }
    [data-testid="stTextInput"] input,
    textarea,
    div[data-baseweb="select"] > div {
        color: var(--sabi-text) !important;
        background-color: #eaf0f7 !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    textarea::placeholder {
        color: #51627a !important;
    }
    [data-testid="stAlertContainer"] {
        background-color: #eaf0f7 !important;
        border-color: #c7d4e6 !important;
    }
    [data-testid="stDataFrame"] {
        background-color: var(--table-body-bg) !important;
        border: 1px solid #35597a !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    [data-testid="stDataFrame"] div[role="grid"],
    [data-testid="stDataFrame"] div[role="table"] {
        border: 1px solid #35597a !important;
        border-radius: 6px !important;
    }
    [data-testid="stDataFrame"] div[role="columnheader"],
    [data-testid="stDataFrame"] div[role="gridcell"],
    [data-testid="stDataFrame"] div[role="rowheader"] {
        box-shadow: inset 0 0 0 1px #6f8fb3 !important;
        color: var(--sabi-text) !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stDataFrame"] table,
    [data-testid="stTable"] table,
    .stTable table {
        border-collapse: collapse !important;
        border-spacing: 0 !important;
        border: 2px solid #35597a !important;
    }
    [data-testid="stDataFrame"] thead th,
    [data-testid="stDataFrame"] tbody td,
    [data-testid="stTable"] thead th,
    [data-testid="stTable"] tbody td,
    .stTable thead th,
    .stTable tbody td {
        border: 1px solid var(--table-cell-border) !important;
        color: #061326 !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stDataFrame"] thead th,
    [data-testid="stTable"] thead th,
    .stTable thead th {
        background-color: var(--table-header-bg) !important;
        color: #061326 !important;
        font-size: 0.9rem !important;
        font-weight: 800 !important;
        border-color: var(--table-header-border) !important;
        border-bottom: 2px solid var(--table-header-bottom) !important;
    }
    [data-testid="stTable"] {
        border: none !important;
        border-radius: 8px !important;
        padding: 0 !important;
        background: var(--table-body-bg) !important;
    }
    /* Refuerzo global para TODAS las tablas visibles (st.table y variantes) */
    .stApp table {
        width: 100% !important;
        border-collapse: collapse !important;
        border-spacing: 0 !important;
        border: 1px solid #35597a !important;
        background: var(--table-body-bg) !important;
    }
    .stApp table thead th,
    .stApp table tbody td,
    .stApp table tbody th {
        border: 1px solid var(--table-cell-border) !important;
        color: #061326 !important;
        font-size: 0.88rem !important;
    }
    .stApp table thead th {
        background: var(--table-header-bg) !important;
        color: #061326 !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        border-color: var(--table-header-border) !important;
        border-bottom: 2px solid var(--table-header-bottom) !important;
    }
    .stApp table tbody td,
    .stApp table tbody th {
        background: var(--table-body-bg) !important;
        color: #061326 !important;
    }
    /* Tabla HTML controlada para asegurar estilo final visible */
    .sabi-table-wrap {
        border: none;
        border-radius: 8px;
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
        overflow-y: hidden;
        -webkit-overflow-scrolling: touch;
        margin-bottom: 8px;
    }
    .sabi-table {
        width: 100%;
        min-width: 100% !important;
        border-collapse: collapse;
        border-spacing: 0;
        background: var(--table-body-bg);
        border: 1px solid #35597a !important;
        table-layout: auto;
    }
    .sabi-table-muebles {
        min-width: 720px !important;
    }
    .sabi-table-top5 {
        min-width: 760px !important;
    }
    .sabi-table thead th,
    .sabi-table th {
        background: var(--table-header-bg) !important;
        color: #061326 !important;
        font-weight: 800;
        font-size: clamp(0.8rem, 0.2vw + 0.72rem, 0.9rem) !important;
        border: 1px solid var(--table-header-border) !important;
        border-bottom: 2px solid var(--table-header-bottom) !important;
        padding: 8px 10px;
        text-align: left;
    }
    .sabi-table tbody td,
    .sabi-table td {
        background: var(--table-body-bg);
        color: #061326 !important;
        font-size: clamp(0.78rem, 0.2vw + 0.7rem, 0.88rem) !important;
        font-weight: 600;
        border: 1px solid var(--table-cell-border) !important;
        padding: 8px 10px;
        text-align: left;
    }
    .sabi-table th,
    .sabi-table td {
        white-space: normal !important;
        overflow-wrap: anywhere;
        word-break: break-word;
        vertical-align: top;
    }
    .sabi-table-top5 th,
    .sabi-table-top5 td {
        white-space: nowrap !important;
        overflow-wrap: normal !important;
        word-break: normal !important;
    }
    .sabi-table * {
        color: #061326 !important;
    }
    .estado-pill {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1.2;
        color: #061326 !important;
    }
    .estado-verde { background: #72E39A; }
    .estado-amarillo { background: #FFD75E; }
    .estado-rojo { background: #FF8A8A; }
    .table-section-title {
        font-size: clamp(0.9rem, 0.2vw + 0.8rem, 1rem) !important;
        font-weight: 700 !important;
        color: var(--sabi-text) !important;
        margin: 0.15rem 0 0.45rem 0 !important;
    }
    /* Plotly: dejar menú de herramientas siempre visible */
    .js-plotly-plot .plotly .modebar {
        opacity: 1 !important;
        visibility: visible !important;
    }
    .js-plotly-plot .plotly .modebar-group {
        opacity: 1 !important;
    }
    /* Streamlit: mantener visible el ícono de ampliar SOLO en Distribución de ganancias */
    [data-testid="stElementContainer"]:has(.dist-ganancias-anchor)
    + [data-testid="stElementContainer"] [data-testid="stElementToolbar"],
    [data-testid="stElementContainer"]:has(.dist-ganancias-anchor)
    + [data-testid="stElementContainer"] [data-testid="stElementToolbar"] * {
        opacity: 1 !important;
        visibility: visible !important;
    }
    /* DataFrame renderizado como grid (no table): texto oscuro + cabecera clara */
    [data-testid="stDataFrame"] div[role="columnheader"] {
        background: var(--table-header-bg) !important;
        color: #061326 !important;
        font-size: 0.9rem !important;
        font-weight: 800 !important;
        box-shadow: inset 0 -2px 0 0 var(--table-header-bottom) !important;
    }
    [data-testid="stDataFrame"] div[role="gridcell"],
    [data-testid="stDataFrame"] div[role="rowheader"] {
        background: var(--table-body-bg) !important;
        color: #061326 !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
    }
    .header-logo {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--sabi-text);
        margin-bottom: 5px;
    }
    .header-subtitle {
        font-size: 0.9em;
        color: var(--sabi-text);
    }
    .agent-button-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .data-box {
        background-color: #e8f4f8;
        padding: 12px;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 8px 0;
    }
    .alert-card {
        padding: 15px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 5px solid;
    }
    .alert-alta {
        background-color: #ffe6e6;
        border-color: #ff4444;
    }
    .alert-media {
        background-color: #fff8e6;
        border-color: #ffaa00;
    }
    .kpi-counter {
        display: inline-block;
        padding: 8px 12px;
        margin: 5px;
        border-radius: 6px;
        background-color: #f0f0f0;
        font-weight: bold;
    }
    .summary-kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin: 8px 0 18px 0;
    }
    .summary-kpi-card {
        background: #eaf0f7 !important;
        border: 1px solid rgba(11, 31, 59, 0.2) !important;
        border-left: 6px solid #9fb3c8;
        border-radius: 12px;
        padding: 10px 12px;
    }
    .summary-kpi-card.total {
        background: #d9ecff !important;
        border-color: #9fc7ed !important;
        border-left-color: #4f8fc9 !important;
    }
    .summary-kpi-card.negativo {
        background: #f3cfcf !important;
        border-color: #dd8f8f !important;
        border-left-color: #b44747 !important;
    }
    .summary-kpi-card.critico {
        background: #ffe7c2 !important;
        border-color: #d9ae62 !important;
        border-left-color: #aa7623 !important;
    }
    .summary-kpi-title {
        font-size: 0.82rem;
        font-weight: 800;
        color: var(--sabi-text);
        margin-bottom: 4px;
    }
    .summary-kpi-value {
        font-size: 1.45rem;
        font-weight: 900;
        color: var(--sabi-text);
        line-height: 1.1;
        margin-bottom: 5px;
    }
    .summary-kpi-card.negativo .summary-kpi-value {
        color: #872f2f !important;
    }
    .summary-kpi-card.critico .summary-kpi-value {
        color: #7d5316 !important;
    }
    .summary-kpi-card.total .summary-kpi-value {
        color: #356ea3 !important;
    }
    .summary-kpi-desc {
        font-size: 0.79rem;
        font-weight: 600;
        color: var(--sabi-text);
        line-height: 1.25;
    }
    
    
      /* Uploader como botón '+' sin drag&drop (Streamlit 1.36) */
  div[data-testid="stFileUploader"],
  div[data-testid="stFileUploader"] section {
    padding: 0 !important;
    margin: 0 !important;
  }

  /* en algunos builds, el 'Browse files' queda dentro del section: recortamos todo a 42x42 */
  div[data-testid="stFileUploader"] section {
    width: 42px !important;
    height: 42px !important;
    overflow: hidden !important;
  }

  /* fuerza un contenedor pequeño aunque la estructura interna cambie */
  div[data-testid="stFileUploader"] section > div {
    position: relative !important;
    width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(11,31,59,0.25) !important;
    background: #eaf0f7 !important;
    overflow: hidden !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }

  /* oculta textos/íconos del uploader sin romper el click */
  div[data-testid="stFileUploader"] svg,
  div[data-testid="stFileUploader"] p,
  div[data-testid="stFileUploader"] small,
  div[data-testid="stFileUploader"] span {
    display: none !important;
  }

  /* el botón/label debe ocupar todo el cuadrado y ser clickeable */
  div[data-testid="stFileUploader"] label,
  div[data-testid="stFileUploader"] button {
    position: absolute !important;
    inset: 0 !important;
    width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    cursor: pointer !important;
    color: transparent !important;
    font-size: 0 !important;
    z-index: 5 !important;
  }

  /* si existe un <input type=file>, mantenerlo por accesibilidad pero invisible */
  div[data-testid="stFileUploader"] input[type="file"] {
    position: absolute !important;
    inset: 0 !important;
    width: 42px !important;
    height: 42px !important;
    opacity: 0 !important;
    cursor: pointer !important;
    z-index: 6 !important;
  }

  /* pintar el '+' SOBRE el botón real */
  div[data-testid="stFileUploader"] button::before,
  div[data-testid="stFileUploader"] label::before {
    content: "+";
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
    color: var(--sabi-text);
    line-height: 1;
    z-index: 1;
  }

  /* Ajustes para el input y el botón enviar */
  div[data-testid="stTextInput"] input {
    height: 42px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(11,31,59,0.20) !important;
  }
  button[kind="secondary"], button[kind="primary"] {
    height: 42px !important;
    border-radius: 12px !important;
  }
  
  
  .header-container {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0;
    }
    .sticky-brand {
        position: fixed;
        top: 0.72rem;
        left: 0.85rem;
        z-index: 999999;
        display: flex;
        align-items: center;
        min-height: 5rem;
        height: auto;
        padding: 8px 16px;
        border-radius: 10px;
        background: rgba(184, 182, 143, 0.92);
        overflow: visible;
    }
    .sticky-brand .header-logo-img {
        display: block !important;
        width: clamp(52px, 5.5vw, 80px) !important;
        height: clamp(52px, 5.5vw, 80px) !important;
        min-width: clamp(52px, 5.5vw, 80px) !important;
        min-height: clamp(52px, 5.5vw, 80px) !important;
        max-width: none !important;
        max-height: none !important;
        flex: 0 0 auto;
        object-fit: contain;
        transform: scale(1.45) !important;
        transform-origin: center center;
    }
    .header-title {
        font-size: clamp(44px, 4.8vw, 68px);
        font-weight: bold;
        margin: 0;
        line-height: 1;
    }

    @media (max-width: 900px) {
        [data-testid="stHeader"],
        [data-testid="stHeader"] > div {
            min-height: 5.6rem !important;
        }
        .header-container {
            flex-wrap: nowrap;
            gap: 6px;
        }
        .sticky-brand {
            top: 0.52rem;
            left: 0.65rem;
            min-height: 4.3rem;
            height: auto;
            padding: 6px 12px;
        }
        .sticky-brand .header-logo-img {
            width: clamp(46px, 5vw, 62px) !important;
            height: clamp(46px, 5vw, 62px) !important;
            min-width: clamp(46px, 5vw, 62px) !important;
            min-height: clamp(46px, 5vw, 62px) !important;
            transform: scale(1.48) !important;
        }
        .header-title {
            font-size: clamp(38px, 4.2vw, 54px);
        }
        [data-testid="stMetricLabel"] div,
        [data-testid="stMetricValue"] div {
            font-size: 0.95rem !important;
        }
    }

    @media (max-width: 640px) {
        [data-testid="stHeader"],
        [data-testid="stHeader"] > div {
            min-height: 4.9rem !important;
        }
        html {
            font-size: 15px !important;
        }
        body, .stApp {
            font-size: 15px;
        }
        h1, h2, h3 {
            font-size: 1.1rem !important;
        }
        h4, h5, h6 {
            font-size: 1rem !important;
        }
        .sabi-table {
            min-width: 100% !important;
            table-layout: auto;
        }
        .sabi-table-muebles {
            min-width: 680px !important;
        }
        .sabi-table-top5 {
            min-width: 760px !important;
        }
        .sabi-table thead th,
        .sabi-table tbody td {
            font-size: 0.78rem !important;
            padding: 7px 8px;
        }
        [data-testid="stDataFrame"] div[role="columnheader"] {
            font-size: 0.82rem !important;
        }
        [data-testid="stDataFrame"] div[role="gridcell"],
        [data-testid="stDataFrame"] div[role="rowheader"] {
            font-size: 0.8rem !important;
        }
        [data-testid="stTextInput"] input,
        button[kind="secondary"],
        button[kind="primary"] {
            height: 38px !important;
        }
        .summary-kpi-grid {
            grid-template-columns: 1fr;
            gap: 8px;
        }
        .summary-kpi-card {
            padding: 9px 10px;
        }
        .summary-kpi-title {
            font-size: 0.8rem;
        }
        .summary-kpi-value {
            font-size: 1.25rem;
        }
        .summary-kpi-desc {
            font-size: 0.76rem;
        }
        .sticky-brand {
            top: 0.36rem;
            left: 0.42rem;
            min-height: 3.5rem;
            height: auto;
            padding: 5px 10px;
        }
        .sticky-brand .header-logo-img {
            width: clamp(48px, 10vw, 52px) !important;
            height: clamp(48px, 10vw, 52px) !important;
            min-width: clamp(48px, 10vw, 52px) !important;
            min-height: clamp(48px, 10vw, 52px) !important;
            transform: scale(1.52) !important;
        }
        .header-title {
            font-size: clamp(30px, 8vw, 42px);
        }
    }

    @media (max-width: 430px) {
        [data-testid="stHeader"],
        [data-testid="stHeader"] > div {
            min-height: 4.4rem !important;
        }
        .sticky-brand {
            top: 0.3rem;
            left: 0.35rem;
            min-height: 3.05rem;
            height: auto;
            padding: 4px 8px;
        }
        .sticky-brand .header-logo-img {
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            min-height: 36px !important;
            transform: scale(1.58) !important;
        }
        .header-title {
            font-size: 28px;
        }
    }
            
    


/* (bloque duplicado de bordes removido; ya está definido arriba con mayor especificidad) */
    
    </style>
""", unsafe_allow_html=True)

SIM_REPORTS = {
    "panaderia": {
        "executive_report": (
            "Reporte Ejecutivo\n"
            "Resumen del analisis\n\n"
            "Se analizaron 30 productos del catalogo de la Pyme, utilizando el dataset simulado productos.csv, que contiene:\n\n"
            "producto_id\n"
            "nombre_producto\n"
            "categoria\n"
            "precio_venta_actual\n\n"
            "El sistema calcula el margen real estimado por producto (precio - costo total unitario) y genera un ranking de rentabilidad.\n\n"
            "Productos mas rentables (Top 5)\n\n"
            "Estos productos presentan el mayor margen unitario y representan las mejores oportunidades comerciales:\n\n"
            "Ranking  Producto      Precio   Margen estimado  Estado\n"
            "1        Producto 30  $2500    Alto            Priorizar\n"
            "2        Producto 29  $2450    Alto            Priorizar\n"
            "3        Producto 28  $2400    Alto            Priorizar\n"
            "4        Producto 27  $2350    Medio/Alto      Mantener\n"
            "5        Producto 26  $2300    Medio/Alto      Mantener\n\n"
            "Estos productos deberian ser foco de ventas porque generan mayor contribucion por unidad.\n\n"
            "Productos con riesgo (Bottom 5)\n\n"
            "Estos productos muestran margenes bajos o negativos y requieren revision urgente:\n\n"
            "Producto    Precio   Margen estimado  Riesgo\n"
            "Producto 1  $1050    Bajo            Revisar\n"
            "Producto 2  $1100    Bajo            Revisar\n"
            "Producto 3  $1150    Bajo            Revisar\n"
            "Producto 4  $1200    Critico         Ajustar\n"
            "Producto 5  $1250    Critico         Ajustar\n\n"
            "Estos productos pueden estar:\n"
            "subvalorados en precio\n"
            "afectados por insumos caros\n"
            "consumiendo esfuerzo sin retorno suficiente\n\n"
            "Conclusion\n\n"
            "SabIA permite identificar rapidamente:\n"
            "Que productos generan ganancias reales\n"
            "Cuales deben revisarse antes de seguir vendiendolos\n"
            "Donde enfocar decisiones comerciales basadas en datos"
        ),
        "metrics": {
            "total_productos": 30,
            "margen_negativo": 5,
            "margen_critico": 2
        },
        "margin_values": {
            "Producto 30": 950,
            "Producto 29": 920,
            "Producto 28": 880,
            "Producto 27": 740,
            "Producto 26": 700,
            "Producto 25": 620,
            "Producto 24": 600,
            "Producto 23": 540,
            "Producto 22": 520,
            "Producto 21": 480,
            "Producto 20": 450,
            "Producto 19": 420,
            "Producto 18": 380,
            "Producto 17": 360,
            "Producto 16": 340,
            "Producto 15": 300,
            "Producto 14": 260,
            "Producto 13": 220,
            "Producto 12": 180,
            "Producto 11": 140,
            "Producto 10": 100,
            "Producto 9": 80,
            "Producto 8": 60,
            "Producto 7": 40,
            "Producto 6": 20,
            "Producto 5": -40,
            "Producto 4": -80,
            "Producto 3": -120,
            "Producto 2": -180,
            "Producto 1": -220
        },
        "semaforo": [
            {"producto": "Producto 30", "margen": "Positivo", "estado": "Verde"},
            {"producto": "Producto 29", "margen": "Positivo", "estado": "Verde"},
            {"producto": "Producto 28", "margen": "Positivo", "estado": "Verde"},
            {"producto": "Producto 27", "margen": "Critico", "estado": "Amarillo"},
            {"producto": "Producto 26", "margen": "Critico", "estado": "Amarillo"},
            {"producto": "Producto 5", "margen": "Negativo", "estado": "Rojo"},
            {"producto": "Producto 4", "margen": "Negativo", "estado": "Rojo"},
            {"producto": "Producto 3", "margen": "Negativo", "estado": "Rojo"},
            {"producto": "Producto 2", "margen": "Negativo", "estado": "Rojo"},
            {"producto": "Producto 1", "margen": "Negativo", "estado": "Rojo"}
        ],
        "top_contribucion": {
            "Producto 30": 250000,
            "Producto 29": 225000,
            "Producto 28": 210000,
            "Producto 27": 175000,
            "Producto 26": 160000
        },
        "top_perdida": {
            "Producto 5": -22000,
            "Producto 4": -18000,
            "Producto 3": -15000,
            "Producto 2": -12000,
            "Producto 1": -9000
        },
        "alerts": [
            {
                "servicio": "Galletas de mantequilla (Producto 1)",
                "tipo": "MARGEN_NEGATIVO",
                "severidad": "ALTA",
                "explicacion": "El costo de produccion supera el precio de venta actual.",
                "evidencia": "Precio $1050 vs costo $1270 → perdida $220 / unidad",
                "accion_sugerida": [
                    "Ajustar precio a $1400 o",
                    "Reducir cantidad de mantequilla o",
                    "Discontinuar producto"
                ]
            },
            {
                "servicio": "Pan integral (Producto 5)",
                "tipo": "MARGEN_CRITICO",
                "severidad": "MEDIA",
                "explicacion": "Margen muy bajo, apenas cubre costos variables.",
                "evidencia": "Margen unitario: $40 (3.2% del precio)",
                "accion_sugerida": [
                    "Aumentar precio en 15-20%",
                    "Reducir costo de harina integral",
                    "Bundling con productos de mayor margen"
                ]
            },
            {
                "servicio": "Torta especial decorada (Producto 8)",
                "tipo": "ALTO_ESFUERZO_BAJO_RETORNO",
                "severidad": "MEDIA",
                "explicacion": "Requiere muchas horas de trabajo para el margen que genera.",
                "evidencia": "4 horas de trabajo con margen 6% (objetivo: 15%)",
                "accion_sugerida": [
                    "Subir tarifa o cobrar por complejidad",
                    "Estandarizar decoraciones",
                    "Reducir tiempo de produccion"
                ]
            }
        ]
    },
    "muebles": {
        "executive_report": (
            "Reporte Ejecutivo\n"
            "Resumen del analisis\n\n"
            "Se analizaron 30 productos considerando:\n\n"
            "Tiempo total promedio de produccion\n"
            "Margen real unitario\n"
            "Umbral de esfuerzo alto\n"
            "Umbral de margen critico\n\n"
            "Clasificacion detectada\n"
            "Productos eficientes\n\n"
            "Bajo tiempo\n"
            "Buen margen\n\n"
            "Ejemplo:\n\n"
            "Producto  Tiempo (min)  Margen %  Estado\n"
            "Producto 28  30  45%  Eficiente\n"
            "Producto 27  28  42%  Eficiente\n\n"
            "Estos deberian priorizarse en ventas y promocion.\n\n"
            "Productos de alto esfuerzo y bajo retorno\n"
            "Producto  Tiempo (min)  Margen %  Problema\n"
            "Producto 5  120  8%  Mucho tiempo, poco retorno\n"
            "Producto 3  110  6%  Ineficiente\n\n"
            "Requieren:\n"
            "Ajuste de precio\n"
            "Optimizacion de proceso\n"
            "Evaluar si vale la pena mantenerlos\n\n"
            "Productos con margen negativo\n"
            "Producto  Tiempo (min)  Margen  Estado\n"
            "Producto 2  90  -12%  Perdida\n\n"
            "Cada unidad vendida genera perdida y ademas consume tiempo productivo.\n\n"
            "Conclusion\n\n"
            "No todos los productos que se venden mucho son buenos para el negocio.\n\n"
            "Algunos:\n"
            "consumen capacidad productiva\n"
            "reducen eficiencia\n"
            "impiden dedicar tiempo a productos mas rentables\n\n"
            "SabIA permite visualizar esto en segundos."
        ),
        "metrics": {
            "total_productos": 12,
            "margen_negativo": 3,
            "margen_critico": 1
        },
        "margin_values": {
            "Mesa comedor 6 personas": 18000,
            "Estanteria de roble": 14000,
            "Silla de madera": 9000,
            "Mesa auxiliar": 5200,
            "Ropero 2 puertas": 4600,
            "Banqueta auxiliar": -2200,
            "Mesa plegable": -1800,
            "Sillon compacto": -1200
        },
        "semaforo": [
            {"producto": "Mesa comedor 6 personas", "margen": "Positivo", "estado": "Verde"},
            {"producto": "Estanteria de roble", "margen": "Positivo", "estado": "Verde"},
            {"producto": "Silla de madera", "margen": "Positivo", "estado": "Verde"},
            {"producto": "Banqueta auxiliar", "margen": "Negativo", "estado": "Rojo"},
            {"producto": "Mesa plegable", "margen": "Negativo", "estado": "Rojo"}
        ],
        "top_contribucion": {
            "Mesa comedor 6 personas": 342000,
            "Estanteria de roble": 180000,
            "Silla de madera": 150000,
            "Mesa auxiliar": 98000,
            "Ropero 2 puertas": 86000
        },
        "top_perdida": {
            "Banqueta auxiliar": -22000,
            "Mesa plegable": -18000,
            "Sillon compacto": -12000,
            "Mesa de esquina": -9000,
            "Banco de trabajo": -7000
        },
        "alerts": [
            {
                "servicio": "Gestion de redes premium (S11)",
                "tipo": "MARGEN_NEGATIVO",
                "severidad": "ALTA",
                "explicacion": "El costo estimado por horas + herramientas supera la tarifa mensual.",
                "evidencia": "Tarifa $22.500 vs costo $26.800 → perdida $4.300 / mes",
                "accion_sugerida": [
                    "Ajustar tarifa a $30.000 o",
                    "Reducir alcance (cantidad de piezas/horas) o",
                    "Reasignar tareas (automatizacion + plantillas)"
                ]
            },
            {
                "servicio": "Campana Ads + optimizacion (S05)",
                "tipo": "ALTO_ESFUERZO_BAJO_RETORNO",
                "severidad": "MEDIA",
                "explicacion": "Requiere muchas horas para el margen que deja.",
                "evidencia": "18 horas/mes con margen 8% (bajo umbral objetivo 15%)",
                "accion_sugerida": [
                    "Paquetizar entregables (plan fijo)",
                    "Subir tarifa o cobrar extra por iteraciones",
                    "Estandarizar reportes para bajar horas"
                ]
            },
            {
                "servicio": "Diseno + contenido mensual (S03)",
                "tipo": "PRECIO_DESACTUALIZADO",
                "severidad": "MEDIA",
                "explicacion": "Aumento el costo hora y herramientas (SaaS), pero la tarifa quedo igual.",
                "evidencia": "costo/hora +12% y tarifa sin cambios en 2 meses",
                "accion_sugerida": [
                    "Ajustar tarifa segun nuevo costo base",
                    "Aplicar clausula de actualizacion trimestral"
                ]
            }
        ]
    },
    "marketing": {
        "executive_report": (
            "Reporte ejecutivo — Periodo 2026-02\n\n"
            "Durante el análisis del periodo 2026-02, se detectaron:\n\n"
            "2 servicios con margen negativo\n"
            "3 servicios con margen crítico\n"
            "2 servicios con alto esfuerzo y bajo retorno\n"
            "1 servicio con tarifa desactualizada\n"
        ),
        "metrics": {
            "total_productos": 8,
            "margen_negativo": 2,
            "margen_critico": 3
        },
        "alerts": [
            {
                "servicio": "Gestión de redes premium (S11)",
                "tipo": "MARGEN_NEGATIVO",
                "severidad": "ALTA",
                "explicacion": "El costo estimado por horas + herramientas supera la tarifa mensual.",
                "evidencia": "Tarifa $22.500 vs costo $26.800 → pérdida $4.300 / mes",
                "accion_sugerida": [
                    "Ajustar tarifa a $30.000 o",
                    "Reducir alcance (cantidad de piezas/horas) o",
                    "Reasignar tareas (automatización + plantillas)"
                ]
            },
            {
                "servicio": "Campaña Ads + optimización (S05)",
                "tipo": "ALTO_ESFUERZO_BAJO_RETORNO",
                "severidad": "MEDIA",
                "explicacion": "Requiere muchas horas para el margen que deja.",
                "evidencia": "18 horas/mes con margen 8% (bajo umbral objetivo 15%)",
                "accion_sugerida": [
                    "Paquetizar entregables (plan fijo)",
                    "Subir tarifa o cobrar extra por iteraciones",
                    "Estandarizar reportes para bajar horas"
                ]
            },
            {
                "servicio": "Diseño + contenido mensual (S03)",
                "tipo": "PRECIO_DESACTUALIZADO",
                "severidad": "MEDIA",
                "explicacion": "Aumentó el costo hora y herramientas (SaaS), pero la tarifa quedó igual.",
                "evidencia": "costo/hora +12% y tarifa sin cambios en 2 meses",
                "accion_sugerida": [
                    "Ajustar tarifa según nuevo costo base",
                    "Aplicar cláusula de actualización trimestral"
                ]
            },
            {
                "servicio": "Consultoría SEO (S02)",
                "tipo": "MARGEN_CRITICO",
                "severidad": "ALTA",
                "explicacion": "Margen muy bajo debido a competencia de mercado.",
                "evidencia": "Tarifa $8.000 con margen 5% (objetivo 25%)",
                "accion_sugerida": [
                    "Diferenciación de propuesta de valor",
                    "Venta cruzada con otros servicios",
                    "Incremento de tarifa gradual"
                ]
            },
            {
                "servicio": "Email marketing (S04)",
                "tipo": "MARGEN_CRITICO",
                "severidad": "MEDIA",
                "explicacion": "Servicio con bajo posicionamiento en cartera.",
                "evidencia": "Tarifa $4.000 con baja demanda",
                "accion_sugerida": [
                    "Promocionar en propuesta de valor",
                    "Bundizar con otros servicios"
                ]
            },
            {
                "servicio": "Estrategia digital (S07)",
                "tipo": "MARGEN_NEGATIVO",
                "severidad": "ALTA",
                "explicacion": "Requiere mucho análisis sin tarifa proporcional.",
                "evidencia": "Tarifa $15.000 vs costo $18.200 → pérdida $3.200 / mes",
                "accion_sugerida": [
                    "Modular en fases con pricing progresivo",
                    "Aumentar tarifa mínima",
                    "Reducir scope a MVP"
                ]
            },
            {
                "servicio": "Gestión de comunidades (S06)",
                "tipo": "MARGEN_CRITICO",
                "severidad": "MEDIA",
                "explicacion": "Margen bajo por falta de automatización.",
                "evidencia": "Tarifa $6.500 con margen 9%",
                "accion_sugerida": [
                    "Implementar herramientas de automatización",
                    "Plantillas de contenido reutilizables",
                    "Aumentar tarifa"
                ]
            },
            {
                "servicio": "Capacitación en redes (S08)",
                "tipo": "ALTO_ESFUERZO_BAJO_RETORNO",
                "severidad": "MEDIA",
                "explicacion": "Servicio puntual con baja recurrencia.",
                "evidencia": "20 horas de preparación vs $5.000 de tarifa",
                "accion_sugerida": [
                    "Iterar hacia curso online (licencia)",
                    "Aumentar tarifa por sesión",
                    "Crear paquetes de capacitación recurrentes"
                ]
            }
        ]
    },
    "mecanico": {
        "executive_report": (
            "🔧 Reporte Ejecutivo - Análisis de Costos del Taller\n\n"
            "Período analizado: 2026-02\n"
            "Servicios analizados: 30\n\n"
            "🔧 Repuestos que más impactan el costo total\n\n"
            "Top 3 drivers detectados:\n"
            "• Kit de embrague: $480.000 (+22%)\n"
            "• Pastillas de freno: $210.000 (+15%)\n"
            "• Filtros importados: $165.000 (+18%)\n\n"
            "📌 El aumento del kit de embrague explica gran parte de la reducción de margen "
            "en servicios complejos.\n\n"
            "🏭 Gastos indirectos con mayor peso mensual:\n"
            "• Alquiler del galpón: $350.000\n"
            "• Energía eléctrica: $180.000\n"
            "• Herramientas/mantenimiento: $95.000\n\n"
            "📌 Aunque no son repuestos, estos gastos afectan el costo real por hora de trabajo.\n\n"
            "🎯 Conclusión: El aumento del kit de embrague está erosionando el margen. "
            "Algunos servicios complejos están subvalorados."
        ),
        "metrics": {
            "servicios_analizados": 30,
            "repuestos_criticos": 3,
            "margen_promedio": 8.5
        },
        "top_repuestos": [
            {
                "nombre": "Kit de embrague",
                "monto": 480000,
                "variacion": 22.0
            },
            {
                "nombre": "Pastillas de freno",
                "monto": 210000,
                "variacion": 15.0
            },
            {
                "nombre": "Filtros importados",
                "monto": 165000,
                "variacion": 18.0
            }
        ],
        "gastos_indirectos": [
            {
                "nombre": "Alquiler del galpón",
                "monto": 350000
            },
            {
                "nombre": "Energía eléctrica",
                "monto": 180000
            },
            {
                "nombre": "Herramientas/Mantenimiento",
                "monto": 95000
            }
        ],
        "servicios_sensibles": {
            "Cambio de embrague (T07)": {
                "drivers": [
                    {"nombre": "Kit de embrague", "monto": 185000},
                    {"nombre": "Mano de obra (7h)", "monto": 70000},
                    {"nombre": "Gastos indirectos prorrateados", "monto": 25000}
                ],
                "costo_total": 280000,
                "precio_cobrado": 295000,
                "margen": 5,
                "margen_estado": "CRÍTICO"
            },
            "Reparación de motor": {
                "drivers": [
                    {"nombre": "Repuestos varios", "monto": 250000},
                    {"nombre": "Mano de obra (12h)", "monto": 120000},
                    {"nombre": "Gastos indirectos prorrateados", "monto": 40000}
                ],
                "costo_total": 410000,
                "precio_cobrado": 495000,
                "margen": 20,
                "margen_estado": "SALUDABLE"
            },
            "Alineación dirección": {
                "drivers": [
                    {"nombre": "Fluido alineador", "monto": 25000},
                    {"nombre": "Mano de obra (2h)", "monto": 20000},
                    {"nombre": "Gastos indirectos prorrateados", "monto": 8000}
                ],
                "costo_total": 53000,
                "precio_cobrado": 55000,
                "margen": 3.8,
                "margen_estado": "CRÍTICO"
            }
        },
        "sensibilidad": {
            "escenario": "Si el kit de embrague aumenta 10%",
            "impacto": "El margen del servicio baja a 2%",
            "recomendaciones": [
                "Ajustar precios en servicios sensibles",
                "Negociar proveedor de repuestos",
                "Revisar estructura de costo hora"
            ]
        }
    }
}

def detect_business(filenames: list) -> str:
    joined = " ".join([name.lower() for name in filenames])
    if "mueble" in joined or "furniture" in joined:
        return "muebles"
    elif "mecanico" in joined or "mecánico" in joined:
        return "mecanico"
    elif "marketing" in joined or "agencia" in joined or "marketing_" in joined:
        return "marketing"
    return "panaderia"

def get_image_base64(path):
    # Safely read and encode the image file
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        # If the file is not found, we'll just not show the image.
        return None

# Construct the full path to the image
logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.png")
logo_base64 = get_image_base64(logo_path)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    # Build the image tag only if the image was successfully loaded
    image_html = ""
    if logo_base64:
        image_html = f'<img src="data:image/png;base64,{logo_base64}" class="header-logo-img">'
    
    # Use an f-string to dynamically insert the image tag into the markdown
    st.markdown(f"""
    <div class="sticky-brand">
        <div class="header-container">
            <span class="header-title">🤖</span>
            {image_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Inicializar session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "current_business" not in st.session_state:
    st.session_state.current_business = None

# Main layout - Full Width
# The two-column layout has been removed to allow the content to span the full width of the page.
st.subheader("💬 Chat con el Agente")

chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

st.divider()

col_upload, col_info = st.columns([1, 2])
with col_upload:
        st.markdown("**Sube los Archivos de tu Pyme**")
        uploaded_files = st.file_uploader(
            "Sube tus archivos de Excel o CSV",
            type=["csv", "xlsx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if uploaded_files:
            st.session_state.uploaded_files = [f.name for f in uploaded_files]

with col_info:
        if st.session_state.uploaded_files:
            st.caption("Archivos cargados: " + ", ".join(st.session_state.uploaded_files))
        else:
            st.caption("Sube tus archivos de 'productos' y 'tiempos' (Excel o CSV).")
st.divider()

# --- MOVED BUTTONS ---
st.markdown("##### Análisis Rápido")
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💰 COSTOS**")
    if st.button("📊 Analizar", use_container_width=True, key="costos_btn"):
        # Si no hay reporte pero hay archivos subi      genéralo automáticamente
        if not st.session_state.last_report and st.session_state.uploaded_files:
            filenames = st.session_state.uploaded_files
            
            # Detectar mecanico
            has_mecanico = any("mecanico" in name.lower() or "mecánico" in name.lower() for name in filenames)
            
            # Validar que tenga los archivos correctos
            valid_mecanico = has_mecanico and len(filenames) >= 2
            
            if valid_mecanico:
                # Generar reporte automáticamente
                business = detect_business(filenames)
                if business in SIM_REPORTS:
                    report = SIM_REPORTS[business]
                    st.session_state.last_report = report
                    st.session_state.current_business = business
                
                # Ahora mostrar el reporte de costos
                if st.session_state.last_report and st.session_state.get("current_business") == "mecanico":
                    report = st.session_state.last_report
                    
                    # Título y resumen ejecutivo
                    st.markdown("**📋 Resumen Ejecutivo**")
                    st.write(report.get("executive_report", ""))
                    
                    # Métricas clave
                    st.markdown("\n**📊 Métricas Clave**")
                    metrics = report.get("metrics", {})
                    m_col1, m_col2, m_col3 = st.columns(3)
                    with m_col1:
                        st.metric("Servicios Analizados", metrics.get('servicios_analizados', 0))
                        st.caption("Cantidad de servicios evaluados en el análisis.")
                    with m_col2:
                        st.metric("Repuestos Críticos", metrics.get('repuestos_criticos', 0))
                        st.caption("Los insumos que más impactan tus costos totales.")
                    with m_col3:
                        st.metric("Margen Promedio", f"{metrics.get('margen_promedio', 0):.1f}%")
                        st.caption("El porcentaje de ganancia promedio de tus servicios.")
    
                    # === GRÁFICOS ===
                    st.markdown("\n**📈 Visualizaciones**")
                    
                    # 1️⃣ Bar Chart - Top repuestos por impacto
                    st.markdown("**1️⃣ Top Repuestos (Mayor Impacto)**")
                    top_repuestos = report.get("top_repuestos", [])
                    if top_repuestos:
                        df_repuestos = pd.DataFrame([
                            {"Repuesto": r['nombre'], "Impacto ($)": r['monto'], "Variación (%)": r['variacion']}
                            for r in top_repuestos
                        ])
                        
                        fig_bar = px.bar(
                            df_repuestos, 
                            x="Repuesto", 
                            y="Impacto ($)",
                            color="Variación (%)",
                            text="Impacto ($)",
                            color_continuous_scale=["#E76F51", "#F4A261", "#2A9D8F"],
                            title="¿Qué me está encareciendo más?"
                        )
                        fig_bar.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
                        style_plotly(fig_bar)
                        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": True})
                    
                    # 2️⃣ Bar Chart - Gastos indirectos (ranking)
                    st.markdown("**2️⃣ Gastos Indirectos (Ranking)**")
                    gastos = report.get("gastos_indirectos", [])
                    if gastos:
                        df_gastos = pd.DataFrame([
                            {"Gasto": g['nombre'], "Monto": g['monto']}
                            for g in gastos
                        ]).sort_values("Monto", ascending=True)
                        
                        fig_gastos_bar = px.bar(
                            df_gastos,
                            x="Monto",
                            y="Gasto",
                            orientation="h",
                            text="Monto",
                            title="Gastos Indirectos Mensuales",
                            color="Monto",
                            color_continuous_scale=["#B8E1FF", "#80B1D3", "#5A8FB3", "#1D4ED8"]
                        )
                        fig_gastos_bar.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
                        fig_gastos_bar.update_layout(xaxis_title="Monto ($)")
                        style_plotly(fig_gastos_bar)
                        st.plotly_chart(fig_gastos_bar, use_container_width=True, config={"displayModeBar": True})
                    
                    # 3️⃣ Drill-down por servicio
                    st.markdown("**3️⃣ Análisis Detallado de Servicios**")
                    servicios = report.get("servicios_sensibles", {})
                    servicio_names = list(servicios.keys())
                    
                    if servicio_names:
                        selected_servicio = st.selectbox("Selecciona un servicio:", servicio_names, key="servicio_select")
                        
                        if selected_servicio:
                            servicio_data = servicios[selected_servicio]
                            
                            # Mostrar desglose en dos columnas
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("📊 Desglose de Costos")
                                df_drivers = pd.DataFrame([
                                    {"Concepto": d['nombre'], "Costo ($)": d['monto']}
                                    for d in servicio_data["drivers"]
                                ])
                                
                                # Agregar porcentaje
                                total = servicio_data["costo_total"]
                                df_drivers["% del Costo"] = (df_drivers["Costo ($)"] / total * 100).round(1)
                                
                                st.dataframe(df_drivers, use_container_width=True, hide_index=True)
                                
                                # Totales
                                st.divider()
                                st.write(f"**Costo Total: ${servicio_data['costo_total']:,.0f}**")
                                st.write(f"**Precio Cobrado: ${servicio_data['precio_cobrado']:,.0f}**")
                                
                                # Margen con color
                                margen = servicio_data['margen']
                                margen_color = "🔴" if margen <= 5 else "🟡" if margen <= 15 else "🟢"
                                st.write(f"**Margen: {margen_color} {margen:.1f}%** ({servicio_data['margen_estado']})")
                            
                            with col2:
                                st.subheader("📈 Distribución Visual")
                                fig_servicio_pie = px.pie(
                                    df_drivers,
                                    names="Concepto",
                                    values="Costo ($)",
                                    title=f"Composición - {selected_servicio}",
                                    color_discrete_sequence=["#2A9D8F", "#8ECAE6", "#F4A261", "#E76F51", "#667eea"]
                                )
                                style_plotly(fig_servicio_pie)
                                st.plotly_chart(fig_servicio_pie, use_container_width=True, config={"displayModeBar": True})
                    
                    # 4️⃣ Indicador de sensibilidad (Pro)
                    st.markdown("**4️⃣ Indicador de Sensibilidad**")
                    sensibilidad = report.get("sensibilidad", {})
                    
                    escenario = sensibilidad.get("escenario", "")
                    impacto = sensibilidad.get("impacto", "")
                    recomendaciones = sensibilidad.get("recomendaciones", [])
                    
                    col1, col2 = st.columns([1.5, 1])
                    
                    with col1:
                        st.warning(f"⚠️ **{escenario}**\n\n{impacto}")
                    
                    with col2:
                        st.info("**Recomendaciones:**")
                        for rec in recomendaciones:
                            st.write(f"• {rec}")
                else:
                    st.info("📌 Sube 2 archivos CSV de mecanico y haz clic para analizar costos")    
                    st.markdown('</div>', unsafe_allow_html=True)

with btn_col2:
    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💡 ESTRATEGIA**")
    if st.button("🚨 Analizar", use_container_width=True, key="estrategia_btn"):
        # Si no hay reporte pero hay archivos subidos, genéralo automáticamente
        if not st.session_state.last_report and st.session_state.uploaded_files:
            filenames = st.session_state.uploaded_files
            
            has_productos = any("producto" in name.lower() for name in filenames)
            has_tiempos = any("tiempo" in name.lower() for name in filenames)
            has_marketing = any("marketing" in name.lower() for name in filenames)
            
            valid_panaderia = has_productos and has_tiempos
            valid_marketing = has_marketing and len(filenames) >= 2
            
            if valid_panaderia or valid_marketing:
                business = detect_business(filenames)
                report = SIM_REPORTS[business]
                st.session_state.last_report = report
                st.session_state.current_business = business
        
        # Ahora mostrar las alertas
        if st.session_state.last_report and "alerts" in st.session_state.last_report:
            alerts = st.session_state.last_report["alerts"]
            
            # Contadores KPI
            st.markdown("**📊 Resumen de Alertas**")
            negativos = sum(1 for a in alerts if a["tipo"] == "MARGEN_NEGATIVO")
            criticos = sum(1 for a in alerts if a["tipo"] == "MARGEN_CRITICO")
            esfuerzo = sum(1 for a in alerts if a["tipo"] == "ALTO_ESFUERZO_BAJO_RETORNO")
            desactualizados = sum(1 for a in alerts if a["tipo"] == "PRECIO_DESACTUALIZADO")
            
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.markdown(f'<div class="kpi-counter">🔴 {negativos}</div>', unsafe_allow_html=True)
                st.caption("Servicios que generan pérdidas.")
            with kpi_col2:
                st.markdown(f'<div class="kpi-counter">🟡 {criticos}</div>', unsafe_allow_html=True)
                st.caption("Servicios con ganancia en riesgo.")
            with kpi_col3:
                st.markdown(f'<div class="kpi-counter">⏱ {esfuerzo}</div>', unsafe_allow_html=True)
                st.caption("Alto esfuerzo, bajo retorno.")
            with kpi_col4:
                st.markdown(f'<div class="kpi-counter">🟠 {desactualizados}</div>', unsafe_allow_html=True)
                st.caption("Precios desactualizados.")
            
            st.divider()
            
            # Filtros
            st.markdown("**🔍 Filtros**")
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                tipo_filter = st.multiselect(
                    "Tipo de alerta",
                    ["MARGEN_NEGATIVO", "MARGEN_CRITICO", "ALTO_ESFUERZO_BAJO_RETORNO", "PRECIO_DESACTUALIZADO"],
                    default=[],
                    key="tipo_filter"
                )
            with filter_col2:
                severidad_filter = st.multiselect(
                    "Severidad",
                    ["ALTA", "MEDIA"],
                    default=[],
                    key="severidad_filter"
                )
            
            # Filtrar alertas
            filtered_alerts = alerts
            if tipo_filter:
                filtered_alerts = [a for a in filtered_alerts if a["tipo"] in tipo_filter]
            if severidad_filter:
                filtered_alerts = [a for a in filtered_alerts if a["severidad"] in severidad_filter]
            
            st.divider()
            st.markdown("**🚨 Alertas Detectadas**")
            
            # Mostrar alertas como cards
            for idx, alert in enumerate(filtered_alerts, 1):
                card_class = "alert-alta" if alert["severidad"] == "ALTA" else "alert-media"
                emoji = "🔴" if alert["severidad"] == "ALTA" else "🟡" if alert["tipo"] == "MARGEN_CRITICO" else "🟠"
                
                st.markdown(f'<div class="alert-card {card_class}">', unsafe_allow_html=True)
                st.markdown(f"**{emoji} Alerta {idx} — {alert['tipo'].replace('_', ' ').title()} ({alert['severidad']})**")
                st.markdown(f"**Servicio:** {alert['servicio']}")
                st.markdown(f"**Explicación:** {alert['explicacion']}")
                st.markdown(f"**Evidencia:** {alert['evidencia']}")
                st.markdown("**Acción sugerida:**")
                for accion in alert["accion_sugerida"]:
                    st.write(f"  • {accion}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if not filtered_alerts:
                st.info("No hay alertas que coincidan con los filtros seleccionados.")
        else:
            st.info("Sube 2 archivos CSV para generar el análisis de alertas.")
    st.markdown('</div>', unsafe_allow_html=True)
# --- END MOVED BUTTONS ---

st.divider()

user_input = st.chat_input("Escribe tu pregunta...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    filenames = st.session_state.uploaded_files
    
    # Detectar panadería
    has_productos = any("producto" in name.lower() for name in filenames)
    has_tiempos = any("tiempo" in name.lower() for name in filenames)
    
    # Detectar marketing (cualquier combinación con "marketing")
    has_marketing = any("marketing" in name.lower() for name in filenames)
    
    # Validar que tenga los archivos correctos
    valid_panaderia = has_productos and has_tiempos
    valid_marketing = has_marketing and len(filenames) >= 2
    
    if valid_panaderia or valid_marketing:
        business = detect_business(filenames)
        report = SIM_REPORTS[business]
        st.session_state.last_report = report
        st.session_state.current_business = business

        respuesta = f"Reporte {business.upper()} generado. ✅"
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.chat_message("assistant").write(respuesta)
    else:
        respuesta = "Necesito 2 archivos: productos+tiempos (panadería) O 2 archivos marketing_* para generar el reporte."
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.chat_message("assistant").write(respuesta)

if st.session_state.last_report:
    # This part of the code could be refactored to show different reports
    # based on which button was clicked, but for now it shows the main one.
    st.subheader("Reporte ejecutivo")
    current_business = st.session_state.get("current_business")

    if current_business not in ["panaderia", "muebles"]:
        st.markdown(st.session_state.last_report["executive_report"])
    elif current_business == "panaderia":
        st.markdown("**Resumen del análisis**")
        st.write("Se analizaron 30 productos del catálogo para identificar rentabilidad y riesgos de margen por producto.")
    elif current_business == "muebles":
        st.markdown("**Resumen del análisis**")
        st.write("Se evaluaron productos por tiempo de producción y margen real para detectar eficiencia, esfuerzo y riesgo de pérdida.")

    if current_business == "panaderia":
        st.markdown('<p class="table-section-title">Productos más rentables (Top 5)</p>', unsafe_allow_html=True)
        tabla_top = pd.DataFrame([
            {"Ranking": 1, "Producto": "Producto 30", "Precio": "$2500", "Margen estimado": "Alto", "Estado": "Priorizar"},
            {"Ranking": 2, "Producto": "Producto 29", "Precio": "$2450", "Margen estimado": "Alto", "Estado": "Priorizar"},
            {"Ranking": 3, "Producto": "Producto 28", "Precio": "$2400", "Margen estimado": "Alto", "Estado": "Priorizar"},
            {"Ranking": 4, "Producto": "Producto 27", "Precio": "$2350", "Margen estimado": "Medio/Alto", "Estado": "Mantener"},
            {"Ranking": 5, "Producto": "Producto 26", "Precio": "$2300", "Margen estimado": "Medio/Alto", "Estado": "Mantener"},
        ])
        render_sabi_table(tabla_top, "sabi-table-top5")
        st.info("Conclusión: estos productos aportan el mayor margen unitario y deben priorizarse en la estrategia comercial y de promoción.")

        st.markdown('<p class="table-section-title">Productos con riesgo (Bottom 5)</p>', unsafe_allow_html=True)
        tabla_riesgo = pd.DataFrame([
            {"Producto": "Producto 1", "Precio": "$1050", "Margen estimado": "Bajo", "Riesgo": "Revisar"},
            {"Producto": "Producto 2", "Precio": "$1100", "Margen estimado": "Bajo", "Riesgo": "Revisar"},
            {"Producto": "Producto 3", "Precio": "$1150", "Margen estimado": "Bajo", "Riesgo": "Revisar"},
            {"Producto": "Producto 4", "Precio": "$1200", "Margen estimado": "Crítico", "Riesgo": "Ajustar"},
            {"Producto": "Producto 5", "Precio": "$1250", "Margen estimado": "Crítico", "Riesgo": "Ajustar"},
        ])
        render_sabi_table(tabla_riesgo)
        st.info("Conclusión: estos productos presentan margen bajo o crítico; conviene ajustar precio, reducir costo o reevaluar su continuidad.")

    if current_business == "muebles":
        st.markdown('<p class="table-section-title">Productos eficientes</p>', unsafe_allow_html=True)
        tabla_eficientes = pd.DataFrame([
            {"Producto": "Producto 28", "Tiempo (min)": 30, "Margen %": "45%", "Estado": "Eficiente"},
            {"Producto": "Producto 27", "Tiempo (min)": 28, "Margen %": "42%", "Estado": "Eficiente"},
        ])
        render_sabi_table(tabla_eficientes, "sabi-table-muebles")
        st.info("Conclusión: estos productos combinan bajo tiempo y buen margen; son candidatos para priorizar ventas y promoción.")

        st.markdown('<p class="table-section-title">Alto esfuerzo y bajo retorno</p>', unsafe_allow_html=True)
        tabla_ineficientes = pd.DataFrame([
            {"Producto": "Producto 5", "Tiempo (min)": 120, "Margen %": "8%", "Problema": "Mucho tiempo, poco retorno"},
            {"Producto": "Producto 3", "Tiempo (min)": 110, "Margen %": "6%", "Problema": "Ineficiente"},
        ])
        render_sabi_table(tabla_ineficientes, "sabi-table-muebles")
        st.info("Conclusión: estos productos consumen mucha capacidad productiva con baja rentabilidad; requieren ajuste de precio u optimización operativa.")

        st.markdown('<p class="table-section-title">Productos con margen negativo</p>', unsafe_allow_html=True)
        tabla_perdida = pd.DataFrame([
            {"Producto": "Producto 2", "Tiempo (min)": 90, "Margen": "-12%", "Estado": "Pérdida"},
        ])
        render_sabi_table(tabla_perdida, "sabi-table-muebles")
        st.info("Conclusión: cada venta de este producto genera pérdida y además ocupa tiempo que podría destinarse a productos rentables.")

    if current_business != "mecanico":
        metrics = st.session_state.last_report["metrics"]
        st.markdown(
            f"""
            <div class=\"summary-kpi-grid\">
                <div class=\"summary-kpi-card total\">
                    <div class=\"summary-kpi-title\">Total de productos</div>
                    <div class=\"summary-kpi-value\">{metrics['total_productos']}</div>
                    <div class=\"summary-kpi-desc\">Cantidad total de productos o servicios analizados.</div>
                </div>
                <div class=\"summary-kpi-card negativo\">
                    <div class=\"summary-kpi-title\">Margen negativo</div>
                    <div class=\"summary-kpi-value\">{metrics['margen_negativo']}</div>
                    <div class=\"summary-kpi-desc\">Productos que cuestan más de lo que valen (generan pérdida).</div>
                </div>
                <div class=\"summary-kpi-card critico\">
                    <div class=\"summary-kpi-title\">Margen crítico</div>
                    <div class=\"summary-kpi-value\">{metrics['margen_critico']}</div>
                    <div class=\"summary-kpi-desc\">Productos con una ganancia muy baja, en riesgo de generar pérdidas.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        margin_values = st.session_state.last_report.get("margin_values")
        if margin_values:
            st.markdown("**Ranking de ganancia por producto**")
            st.caption("Muestra la ganancia neta (precio de venta - costos) que deja cada producto. Te permite ver rápidamente cuáles son tus productos estrella y cuáles no son rentables.")
            margin_df = pd.DataFrame(
                list(margin_values.items()),
                columns=["Producto", "Ganancia ($)"]
            ).set_index("Producto")
            margin_chart_df = margin_df.reset_index()
            margin_chart_df["Estado"] = margin_chart_df["Ganancia ($)"].apply(
                lambda value: "Ganancia" if value >= 0 else "Pérdida"
            )
            fig_margin = px.bar(
                margin_chart_df,
                x="Producto",
                y="Ganancia ($)",
                color="Estado",
                color_discrete_map={
                    "Ganancia": CHART_COLORS["positive"],
                    "Pérdida": CHART_COLORS["negative"],
                },
                title="Ganancia por producto",
            )
            fig_margin.update_layout(
                xaxis_title="Producto",
                yaxis_title="Ganancia ($)",
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=10, color="#061326"),
                    title_font=dict(size=13, color="#061326"),
                    automargin=True,
                ),
                yaxis=dict(
                    tickfont=dict(size=11, color="#061326"),
                    title_font=dict(size=13, color="#061326"),
                    automargin=True,
                ),
                title_font=dict(size=16, color="#061326"),
                legend=dict(font=dict(size=11, color="#061326"), title_font=dict(color="#061326")),
            )
            style_plotly(fig_margin)
            st.plotly_chart(fig_margin, use_container_width=True, config={"displayModeBar": True})

            semaforo = st.session_state.last_report.get("semaforo")
            if semaforo:
                st.markdown("**Semáforo de Rentabilidad**")
                st.caption("Clasifica cada producto según su estado de rentabilidad para priorizar decisiones rápidas.")
                semaforo_df = pd.DataFrame(semaforo)
                semaforo_df["estado"] = semaforo_df["estado"].map(
                    {
                        "Verde": '<span class="estado-pill estado-verde">Verde</span>',
                        "Amarillo": '<span class="estado-pill estado-amarillo">Amarillo</span>',
                        "Rojo": '<span class="estado-pill estado-rojo">Rojo</span>',
                    }
                ).fillna(semaforo_df["estado"])
                render_sabi_table(semaforo_df, "sabi-table-semaforo", escape_html=False)

            st.markdown("**Distribución de ganancias**")
            st.caption("Muestra cuántos productos caen en cada nivel de ganancia para entender la salud del portafolio.")
            st.markdown('<div class="dist-ganancias-anchor"></div>', unsafe_allow_html=True)
            st.bar_chart(margin_df["Ganancia ($)"].value_counts().sort_index(), color="#0377E4")

            top_contribucion = st.session_state.last_report.get("top_contribucion")
            top_perdida = st.session_state.last_report.get("top_perdida")
            if top_contribucion and top_perdida:
                st.markdown("**Top vs bottom (comparación rápida)**")
                st.caption("Compara de forma directa los productos que más aportan frente a los que más pérdidas generan.")
                top_col, bottom_col = st.columns(2)
                with top_col:
                    st.markdown("**Top 5 de contribución positiva**")
                    top_df = pd.DataFrame(
                        list(top_contribucion.items()),
                        columns=["Producto", "Contribución"]
                    )
                    render_sabi_table(top_df, "sabi-table-resumen")
                with bottom_col:
                    st.markdown("**Bottom 5 de pérdidas**")
                    bottom_df = pd.DataFrame(
                        list(top_perdida.items()),
                        columns=["Producto", "Pérdida"]
                    )
                    render_sabi_table(bottom_df, "sabi-table-resumen")
    st.caption("SabIA protege tus datos: el análisis se realiza de forma local y solo se usa para esta demo.")

