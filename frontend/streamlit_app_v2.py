import requests
import streamlit as st
from datetime import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="SabIA - Copiloto Inteligente", layout="wide", initial_sidebar_state="collapsed")

# CSS minimalista
st.markdown("""
    <style>
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
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header-logo">🤖 SabIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Copiloto inteligente para tu pyme</div>', unsafe_allow_html=True)

# Inicializar session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "periodo" not in st.session_state:
    st.session_state.periodo = "2024-01"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Main layout
col_chat, col_buttons = st.columns([2, 1], gap="medium")

# ===== LEFT: Chat Area =====
with col_chat:
    st.subheader("💬 Chat con el Agente")
    
    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])
    
    st.divider()
    
    # File uploader
    col_upload, col_info = st.columns([1, 2])
    with col_upload:
        st.markdown("**➕ Subir CSV**")
        uploaded_file = st.file_uploader(
            "Sube tu archivo de datos",
            type="csv",
            label_visibility="collapsed"
        )
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file.name
            st.success(f"✅ {uploaded_file.name}")
    
    with col_info:
        st.caption("*Carga tus datos para análisis personalizados*")
    
    st.divider()
    
    # Chat input
    user_input = st.chat_input("Pregúntale al Agente sobre rentabilidad, costos, alertas...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        try:
            # Ejecutar pipeline real
            run_response = requests.post(
                f"{BASE_URL}/run",
                json={"periodo": st.session_state.periodo, "llm": None},
                timeout=60
            )
            run_response.raise_for_status()
            run_output = run_response.json()
            
            # Respuesta contextual
            respuesta = "📊 **Análisis completado**\n\n"
            
            # Extraer data
            kpis = run_output.get("kpis", {})
            alerts = run_output.get("alerts", [])
            
            respuesta += f"**Total productos:** {kpis.get('total_productos', 0)}\n"
            respuesta += f"**Alertas:** {len(alerts)} detectadas\n\n"
            
            if alerts:
                respuesta += "🔔 **Principales alertas:**\n"
                for alert in alerts[:3]:
                    respuesta += f"• {alert.get('nombre_producto', '?')}\n"
            
            respuesta += "\n💡 Usa los botones **COSTOS** y **ESTRATEGIA** para análisis detallados"
            
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.chat_message("assistant").write(respuesta)
            
        except Exception as e:
            error = f"❌ {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error})
            st.error(error)

# ===== RIGHT: Action Buttons =====
with col_buttons:
    st.subheader("🎯 Análisis")
    
    # Período selector (compacto)
    st.session_state.periodo = st.selectbox(
        "Período",
        [f"2024-{i:02d}" for i in range(1, 13)],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # COSTOS Button
    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💰 COSTOS**")
    
    if st.button("📊 Analizar", use_container_width=True, key="costos_btn"):
        try:
            resp = requests.get(
                f"{BASE_URL}/demo/real/story/4",
                params={"periodo": st.session_state.periodo},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            
            st.markdown('<div class="data-box">', unsafe_allow_html=True)
            st.markdown("**📈 Top Insumos:**")
            for ins in data.get('top_insumos', [])[:3]:
                st.write(f"• {ins['insumo']}: ${ins['impacto_total']:,.0f}")
            
            st.markdown("\n**💰 Gastos:**")
            for gasto in data.get('top_gastos_indirectos', [])[:2]:
                if isinstance(gasto, dict):
                    monto = gasto.get('monto_mensual', 0) or gasto.get('impacto_total', 0)
                    st.write(f"• {gasto.get('gasto', '?')}: ${monto:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # ESTRATEGIA Button
    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💡 ESTRATEGIA**")
    
    if st.button("🚨 Analizar", use_container_width=True, key="estrategia_btn"):
        try:
            resp = requests.get(
                f"{BASE_URL}/demo/real/story/3",
                params={"periodo": st.session_state.periodo},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            
            st.markdown('<div class="data-box">', unsafe_allow_html=True)
            st.markdown("**🔔 Alertas:**")
            
            for alert in data.get('alerts', [])[:3]:
                severidad_emoji = "🔴" if alert.get('severidad') == 'CRITICA' else "🟠"
                st.write(f"{severidad_emoji} **{alert.get('nombre_servicio', '?')}**")
                st.write(f"→ {alert.get('accion_sugerida', '?')}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
