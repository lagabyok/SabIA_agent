import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SabIA - Copiloto Inteligente", layout="wide", initial_sidebar_state="collapsed")

# CSS minimalista
st.markdown("""
    <style>
    body, .stApp {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 18px;
    }
    .header-logo {
        font-size: 2.5em;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 5px;
    }
    .header-subtitle {
        font-size: 0.9em;
        color: #666;
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


# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header-logo">🤖 SabIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Copiloto inteligente para tu pyme</div>', unsafe_allow_html=True)

# Inicializar session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "current_business" not in st.session_state:
    st.session_state.current_business = None

# Main layout
col_chat, col_buttons = st.columns([2, 1], gap="medium")

# ===== LEFT: Chat Area =====
with col_chat:
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
        st.markdown("**➕ Subir CSV**")
        uploaded_files = st.file_uploader(
            "Sube tus archivos",
            type="csv",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if uploaded_files:
            st.session_state.uploaded_files = [f.name for f in uploaded_files]

    with col_info:
        if st.session_state.uploaded_files:
            st.caption("Archivos cargados: " + ", ".join(st.session_state.uploaded_files))
        else:
            st.caption("Carga panaderia_productos.csv y panaderia_tiempos.csv (o mueble_...)")

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
        st.subheader("Reporte Ejecutivo")
        st.markdown(st.session_state.last_report["executive_report"])

        metrics = st.session_state.last_report["metrics"]
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total productos", metrics["total_productos"])
        col_b.metric("Margen negativo", metrics["margen_negativo"])
        col_c.metric("Margen critico", metrics["margen_critico"])

        st.markdown("**Ranking de Margen por Producto (Bar Chart)**")
        margin_df = pd.DataFrame(
            list(st.session_state.last_report["margin_values"].items()),
            columns=["Producto", "Margen"]
        ).set_index("Producto")
        st.bar_chart(margin_df)

        st.markdown("**Semaforo de Rentabilidad**")
        semaforo_df = pd.DataFrame(st.session_state.last_report["semaforo"])
        def _color_estado(val):
            if val == "Verde":
                return "background-color: #d4edda"
            if val == "Amarillo":
                return "background-color: #fff3cd"
            if val == "Rojo":
                return "background-color: #f8d7da"
            return ""
        st.dataframe(semaforo_df.style.applymap(_color_estado, subset=["estado"]))

        st.markdown("**Distribucion de Margenes (Histogram)**")
        st.bar_chart(margin_df["Margen"].value_counts().sort_index())

        st.markdown("**Top vs Bottom (Comparacion rapida)**")
        top_col, bottom_col = st.columns(2)
        with top_col:
            st.markdown("**Top 5 contribucion positiva**")
            top_df = pd.DataFrame(
                list(st.session_state.last_report["top_contribucion"].items()),
                columns=["Producto", "Contribucion"]
            ).set_index("Producto")
            st.dataframe(top_df)
        with bottom_col:
            st.markdown("**Bottom 5 perdidas**")
            bottom_df = pd.DataFrame(
                list(st.session_state.last_report["top_perdida"].items()),
                columns=["Producto", "Perdida"]
            ).set_index("Producto")
            st.dataframe(bottom_df)

        st.caption("SabIA protege tus datos: el analisis se realiza de forma local y solo se usa para esta demo.")

# ===== RIGHT: Action Buttons =====
with col_buttons:
    st.subheader("🎯 Analisis")

    st.divider()

    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💰 COSTOS**")
    if st.button("📊 Analizar", use_container_width=True, key="costos_btn"):
        # Si no hay reporte pero hay archivos subidos, genéralo automáticamente
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
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Servicios Analizados", metrics.get('servicios_analizados', 0))
            with col2:
                st.metric("Repuestos Críticos", metrics.get('repuestos_criticos', 0))
            with col3:
                st.metric("Margen Promedio", f"{metrics.get('margen_promedio', 0):.1f}%")
            
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
                    color_continuous_scale="RdYlGn_r",
                    title="¿Qué me está encareciendo más?"
                )
                fig_bar.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
                st.plotly_chart(fig_bar, use_container_width=True)
            
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
                    color_continuous_scale="Blues"
                )
                fig_gastos_bar.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
                st.plotly_chart(fig_gastos_bar, use_container_width=True)
            
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
                            title=f"Composición - {selected_servicio}"
                        )
                        st.plotly_chart(fig_servicio_pie, use_container_width=True)
            
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


    st.divider()

    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💡 ESTRATEGIA**")
    if st.button("🚨 Analizar", use_container_width=True, key="estrategia_btn"):
        # Si no hay reporte pero hay archivos subidos, genéralo automáticamente
        if not st.session_state.last_report and st.session_state.uploaded_files:
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
                # Generar reporte automáticamente
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
                st.caption("Negativos")
            with kpi_col2:
                st.markdown(f'<div class="kpi-counter">🟡 {criticos}</div>', unsafe_allow_html=True)
                st.caption("Críticos")
            with kpi_col3:
                st.markdown(f'<div class="kpi-counter">⏱ {esfuerzo}</div>', unsafe_allow_html=True)
                st.caption("Alto esfuerzo")
            with kpi_col4:
                st.markdown(f'<div class="kpi-counter">🟠 {desactualizados}</div>', unsafe_allow_html=True)
                st.caption("Desactualizados")
            
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
            st.markdown('<div class="data-box">', unsafe_allow_html=True)
            st.markdown("**🔔 Alertas Criticas:**")
            st.info("Sube 2 archivos CSV para generar el análisis de alertas.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)