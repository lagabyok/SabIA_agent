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
if "mode" not in st.session_state:
    st.session_state.mode = "demo"

# Main layout
col_chat, col_agents = st.columns([2.5, 1])

# COLUMN LEFT: Chat
with col_chat:
    st.subheader("💬 Conversación con Agente Core")
    
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
    user_input = st.chat_input("Pregúntale al Agente Core sobre rentabilidad, tiempos o alertas...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Generar respuesta del Agente Core (H1, H2, H3)
        try:
            # Obtener los 3 stories
            resp1 = requests.get(f"{BASE_URL}/demo/story/1", timeout=10)
            resp2 = requests.get(f"{BASE_URL}/demo/story/2", timeout=10)
            resp3 = requests.get(f"{BASE_URL}/demo/story/3", timeout=10)
            
            resp1.raise_for_status()
            resp2.raise_for_status()
            resp3.raise_for_status()
            
            data1 = resp1.json()
            data2 = resp2.json()
            data3 = resp3.json()
            
            # Construir respuesta contextual
            respuesta = "📊 **Análisis del Agente Core:**\n\n"
            
            # Ranking margen
            respuesta += "**1️⃣ Ranking por Margen Real:**\n"
            respuesta += f"✅ TOP: **{data1['ranking'][0]['nombre_producto']}** - {data1['ranking'][0]['margen_pct']*100:.1f}% margen\n"
            respuesta += f"⚠️ RIESGO: **{data1['bottom_risk'][0]['nombre_producto']}** - {data1['bottom_risk'][0]['margen_pct']*100:.1f}% margen\n\n"
            
            # Tiempo vs margen
            respuesta += "**2️⃣ Eficiencia (Tiempo vs Margen):**\n"
            efficient = [i for i in data2['items'] if i['categoria'] == 'eficiente']
            inefficient = [i for i in data2['items'] if i['categoria'] == 'alto_esfuerzo_bajo_retorno']
            respuesta += f"✅ Eficientes: {len(efficient)} productos\n"
            respuesta += f"❌ Ineficientes: {len(inefficient)} productos\n\n"
            
            # Alertas
            respuesta += "**3️⃣ Alertas de Rentabilidad:**\n"
            for alert in data3['alerts'][:2]:
                respuesta += f"🔔 **{alert['nombre_servicio']}** - {alert['tipo']}\n"
            
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.chat_message("assistant").write(respuesta)
            
        except Exception as e:
            error = f"❌ Error al consultar: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error})
            st.error(error)

# COLUMN RIGHT: Agents & Sidebar
with col_agents:
    st.subheader("🤖 Agentes Especializados")
    
    # Sidebar config
    with st.expander("⚙️ Configuración"):
        mode = st.radio("Modo:", ["📊 Demo", "🔄 Real"])
        st.session_state.mode = "demo" if mode == "📊 Demo" else "real"
        
        if st.session_state.mode == "real":
            periodo = st.selectbox("Período", [f"2024-{i:02d}" for i in range(1, 13)], index=1)
            llm = st.selectbox("LLM", ["gemini", "openai", "none"])
    
    st.divider()
    
    # AGENTE A - COSTOS
    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
    st.markdown("**🔍 AGENTE A - Costos**")
    st.caption("Drivers de costos e insumos")
    
    if st.button("📊 Analizar Costos", use_container_width=True, key="agente_a"):
        try:
            resp = requests.get(f"{BASE_URL}/demo/story/5", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            st.markdown('<div class="story-data">', unsafe_allow_html=True)
            st.markdown("**📈 Top Insumos (Impacto Total):**")
            for ins in data['top_insumos'][:3]:
                st.write(f"• **{ins['insumo']}**: ${ins['impacto_total']:,.0f} ({ins['variacion_pct']*100:.1f}% volatilidad)")
            
            st.markdown("\n**💰 Gastos Indirectos:**")
            for gasto in data['top_gastos_indirectos'][:2]:
                st.write(f"• {gasto['gasto']}: ${gasto['monto_mensual']:,.0f}")
            
            st.markdown("\n**⚡ Sensibilidad Crítica:**")
            for prod in data['sensibilidad_productos'][:2]:
                st.write(f"✨ **{prod['nombre_producto']}** - Si harina sube 10%: -{prod['sensibilidades'][0]['impacto_si_sube_10pct']['impacto_contribucion_500u']:,.0f} (impacto potencial)")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # AGENTE 2 - PRICING
    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
    st.markdown("**💡 AGENTE 2 - Pricing & Estrategia**")
    st.caption("Recomendaciones de precio e impacto")
    
    if st.button("💰 Optimizar Precios", use_container_width=True, key="agente_2"):
        try:
            resp = requests.get(f"{BASE_URL}/demo/story/6", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            st.markdown('<div class="story-data">', unsafe_allow_html=True)
            st.markdown("**🎯 Prioridades de Acción:**")
            
            for rec in data['recomendaciones'][:3]:
                urgencia_emoji = "🔴" if rec['prioridad'] == 1 else "🟠" if rec['prioridad'] == 2 else "🟡"
                st.write(f"{urgencia_emoji} **P{rec['prioridad']}: {rec['nombre_producto']}**")
                st.write(f"   └─ {rec['estrategia']}")
                st.write(f"   └─ Impacto: ${rec['impacto_economico']:,.0f}")
            
            st.markdown("\n**📋 Resumen Ejecutivo:**")
            for item in data['resumen_prioridades']:
                st.write(f"**{item['rango']}. {item['accion']}** ({item['urgencia']})")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    **📌 Agentes disponibles:**
    - **Agente Core**: Chat directo (H1, H2, H3)
    - **Agente A**: Análisis de costos e insumos
    - **Agente 2**: Pricing y estrategia
""")
