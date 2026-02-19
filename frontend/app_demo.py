import requests
import streamlit as st

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
    
    # File uploader con procesamiento simul ado
    col_upload, col_info = st.columns([1, 2])
    with col_upload:
        st.markdown("**➕ Subir CSV**")
        uploaded_file = st.file_uploader(
            "Ej: panaderia_productos.csv o mueble_productos.csv",
            type="csv",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            filename_lower = uploaded_file.name.lower()
            
            if "producto" in filename_lower or "product" in filename_lower:
                # H1: Ranking margen - SIMULADA
                try:
                    files = {"file": uploaded_file}
                    resp = requests.post(f"{BASE_URL}/demo/upload/productos", files=files, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    
                    # Agregar a chat
                    msg_user = f"📊 Subí: {uploaded_file.name}"
                    st.session_state.chat_history.append({"role": "user", "content": msg_user})
                    st.chat_message("user").write(msg_user)
                    
                    # Respuesta H1
                    respuesta = f"📊 **Ranking de Productos - {data.get('tipo_negocio', 'Negocio')}**\n\n"
                    respuesta += "**✅ TOP 3:**\n"
                    for prod in data.get('ranking', [])[:3]:
                        respuesta += f"• **{prod.get('nombre_producto')}** - {prod.get('margen_pct')*100:.1f}% margen\n"
                    
                    if data.get('bottom_risk'):
                        respuesta += "\n**⚠️ PRODUCTOS EN RIESGO:**\n"
                        for prod in data.get('bottom_risk', []):
                            respuesta += f"• **{prod.get('nombre_producto')}** - {prod.get('margen_pct')*100:.1f}% margen (⚠️ Revisar)\n"
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                    st.chat_message("assistant").write(respuesta)
                    st.success(f"✅ Analizado")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            elif "tiempo" in filename_lower or "time" in filename_lower:
                # H2: Tiempo vs margen - SIMULADA
                try:
                    files = {"file": uploaded_file}
                    resp = requests.post(f"{BASE_URL}/demo/upload/tiempos", files=files, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    
                    # Agregar a chat
                    msg_user = f"⏱️ Subí: {uploaded_file.name}"
                    st.session_state.chat_history.append({"role": "user", "content": msg_user})
                    st.chat_message("user").write(msg_user)
                    
                    # Respuesta H2
                    respuesta = f"⏱️ **Análisis Tiempo vs Margen - {data.get('tipo_negocio', 'Negocio')}**\n\n"
                    
                    efficient = [i for i in data.get('items', []) if i.get('categoria') == 'eficiente']
                    inefficient = [i for i in data.get('items', []) if i.get('categoria') == 'alto_esfuerzo_bajo_retorno']
                    
                    if efficient:
                        respuesta += "**✅ EFICIENTES (poco tiempo, buen margen):**\n"
                        for item in efficient[:2]:
                            respuesta += f"• **{item.get('nombre_producto')}** - {item.get('minutos_trabajo')} min, {item.get('margen_pct')*100:.1f}% margen\n"
                    
                    if inefficient:
                        respuesta += "\n**❌ ALTO ESFUERZO, BAJO RETORNO:**\n"
                        for item in inefficient[:2]:
                            respuesta += f"• **{item.get('nombre_producto')}** - {item.get('minutos_trabajo')} min, {item.get('margen_pct')*100:.1f}% margen\n"
                            respuesta += "   → Considera aumentar precio o reducir volumen\n"
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                    st.chat_message("assistant").write(respuesta)
                    st.success(f"✅ Analizado")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col_info:
        st.caption("*Detecta automáticamente el tipo de negocio*")
    
    st.divider()
    
    # Chat input
    user_input = st.chat_input("Escribe una pregunta...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Respuesta contextual simple
        respuesta = "💡 Para análisis detallados, usa los botones **COSTOS** y **ESTRATEGIA** →"
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.chat_message("assistant").write(respuesta)

# ===== RIGHT: Action Buttons =====
with col_buttons:
    st.subheader("🎯 Análisis")
    
    # Período selector
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
        st.markdown('<div class="data-box">', unsafe_allow_html=True)
        st.markdown("**📈 Top Insumos:**")
        st.write("• Harina: $145,000")
        st.write("• Mantequilla: $76,000")
        st.write("• Azúcar: $98,000")
        
        st.markdown("\n**💰 Gastos Indirectos:**")
        st.write("• Alquiler: $150,000")
        st.write("• Mano de obra: $200,000")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # ESTRATEGIA Button
    st.markdown('<div class="agent-button-section">', unsafe_allow_html=True)
    st.markdown("**💡 ESTRATEGIA**")
    
    if st.button("🚨 Analizar", use_container_width=True, key="estrategia_btn"):
        st.markdown('<div class="data-box">', unsafe_allow_html=True)
        st.markdown("**🔔 Alertas Críticas:**")
        st.write("🔴 **Galletas** - Margen negativo (-20%)")
        st.write("   → Aumentar precio o descontinuar")
        st.write("")
        st.write("🟠 **Pan integral** - Margen bajo (2.5%)")
        st.write("   → Renegociar precio")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
