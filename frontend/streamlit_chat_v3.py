import pandas as pd
import requests
import streamlit as st
from datetime import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="SabIA - Chat Agente", layout="wide")

# CSS personalizado
st.markdown("""
    <style>
    .header-section {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .agent-section {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .story-data {
        background-color: #e8f4f8;
        padding: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <h1>🤖 SabIA - Asistente Inteligente</h1>
        <p>Transforma tus datos en decisiones claras y explicables</p>
    </div>
""", unsafe_allow_html=True)

# Inicializar session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "modo" not in st.session_state:
    st.session_state.modo = "demo"
if "periodo" not in st.session_state:
    st.session_state.periodo = "2024-01"

# Main layout
col_chat, col_agents = st.columns([2.5, 1])

# COLUMN LEFT: Chat with Agente Core
with col_chat:
    st.subheader("💬 Agente Core (Chat directo)")
    st.caption("Pregúntame sobre rentabilidad, tiempos, alertas o costos")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])
    
    st.divider()
    
    # Input
    user_input = st.chat_input("Escribe tu pregunta...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Ejecutar pipeline real y generar respuesta
        try:
            periodo = st.session_state.periodo
            
            # Ejecutar POST /run para obtener el pipeline
            run_response = requests.post(
                f"{BASE_URL}/run",
                json={"periodo": periodo, "llm": None},
                timeout=60
            )
            run_response.raise_for_status()
            run_output = run_response.json()
            
            # Construir respuesta contextual
            respuesta = "📊 **Análisis del Agente Core:**\n\n"
            
            # H1: Ranking margen
            respuesta += "**1️⃣ Ranking por Margen Real:**\n"
            if "kpis" in run_output and "top_5_productos_por_contribucion" in run_output["kpis"]:
                top_prods = run_output["kpis"].get("top_5_productos_por_contribucion", [])
                if top_prods:
                    respuesta += f"✅ **TOP**: {top_prods[0].get('nombre_producto', '?')} - {top_prods[0].get('margen_pct', 0)*100:.1f}% margen\n"
            
            if "kpis" in run_output and "top_5_productos_por_perdida" in run_output["kpis"]:
                loss_prods = run_output["kpis"].get("top_5_productos_por_perdida", [])
                if loss_prods:
                    respuesta += f"⚠️ **CRÍTICO**: {loss_prods[0].get('nombre_producto', '?')} genera pérdidas\n"
            
            respuesta += "\n**2️⃣ Alertas generadas:**\n"
            alerts = run_output.get("alerts", [])
            if alerts:
                respuesta += f"🔔 {len(alerts)} alertas detectadas\n"
                for alert in alerts[:2]:
                    respuesta += f"   • {alert.get('nombre_producto', '?')}: {alert.get('tipo', '?')}\n"
            else:
                respuesta += "✅ Sin alertas críticas\n"
            
            respuesta += "\n💡 *Usa los botones 'ESTRATEGIA' y 'COSTOS' para análisis detallados*"
            
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.chat_message("assistant").write(respuesta)
            
        except Exception as e:
            error = f"❌ Error al consultar: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error})
            st.error(error)

# COLUMN RIGHT: Specialized Agents & Config
with col_agents:
    st.subheader("🎯 Agentes Especializados")
    
    # Configuration
    with st.expander("⚙️ Configuración"):
        st.session_state.modo = st.radio("Tipo:", ["📊 Demo", "🔄 Real"])
        
        if st.session_state.modo == "🔄 Real":
            st.session_state.periodo = st.selectbox(
                "Período",
                [f"2024-{i:02d}" for i in range(1, 13)],
                index=int(st.session_state.periodo.split("-")[1]) - 1
            )
    
    st.divider()
    
    # AGENTE A - COSTOS (H4)
    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
    st.markdown("**💰 COSTOS**")
    st.caption("Drivers de insumos y gastos")
    
    if st.button("📊 Ver Análisis de Costos", use_container_width=True, key="costos_btn"):
        try:
            periodo = st.session_state.periodo if st.session_state.modo == "🔄 Real" else "2024-01"
            
            # H4: Drivers de costos
            resp = requests.get(
                f"{BASE_URL}/demo/real/story/4",
                params={"periodo": periodo},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            
            st.markdown('<div class="story-data">', unsafe_allow_html=True)
            st.markdown("**📈 Top Insumos (Impacto Total):**")
            for ins in data.get('top_insumos', [])[:3]:
                st.write(f"• **{ins['insumo']}**: ${ins['impacto_total']:,.0f} ({ins.get('variacion_pct', 0)*100:.1f}% volatilidad)")
            
            st.markdown("\n**💰 Gastos Indirectos:**")
            for gasto in data.get('top_gastos_indirectos', [])[:2]:
                if isinstance(gasto, dict):
                    monto = gasto.get('monto_mensual', 0) or gasto.get('impacto_total', 0)
                    st.write(f"• {gasto.get('gasto', '?')}: ${monto:,.0f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # AGENTE 2 - ESTRATEGIA (H3)
    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
    st.markdown("**💡 ESTRATEGIA**")
    st.caption("Alertas y recomendaciones")
    
    if st.button("🚨 Ver Alertas & Estrategia", use_container_width=True, key="estrategia_btn"):
        try:
            periodo = st.session_state.periodo if st.session_state.modo == "🔄 Real" else "2024-01"
            
            # H3: Alertas
            resp = requests.get(
                f"{BASE_URL}/demo/real/story/3",
                params={"periodo": periodo},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            
            st.markdown('<div class="story-data">', unsafe_allow_html=True)
            st.markdown("**🔔 Alertas de Rentabilidad:**")
            
            for alert in data.get('alerts', [])[:3]:
                severidad_emoji = "🔴" if alert.get('severidad') == 'CRITICA' else "🟠" if alert.get('severidad') == 'ALTA' else "🟡"
                st.write(f"{severidad_emoji} **{alert.get('nombre_servicio', '?')}**")
                st.write(f"   └─ {alert.get('tipo', '?')}")
                st.write(f"   └─ Acción: {alert.get('accion_sugerida', '?')}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    **📌 Modo de Operación:**
    - **Chat**: Agente Core analiza tus datos en tiempo real
    - **Botones**: Análisis profundos de Costos y Estrategia
    - Todos los datos vienen de tu pipeline ejecutado
""")
