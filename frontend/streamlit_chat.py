import pandas as pd
import requests
import streamlit as st
from datetime import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="SabIA - Chat Agente", layout="wide")

# CSS personalizado para mejor diseño
st.markdown("""
    <style>
    .header-section {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .agent-button {
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }
    .story-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
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
if "current_story" not in st.session_state:
    st.session_state.current_story = None
if "mode" not in st.session_state:
    st.session_state.mode = "demo"  # "demo" o "real"

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Toggle entre modo demo y real
    st.subheader("Modo de funcionamiento")
    mode = st.radio("Selecciona modo:", ["📊 Demo", "🔄 Real"], 
                    help="Demo = datos simulados | Real = ejecuta pipeline completo")
    st.session_state.mode = "demo" if mode == "📊 Demo" else "real"
    
    # Subida de archivos
    st.subheader("📁 Subir datos")
    uploaded_file = st.file_uploader("Sube tu CSV", type="csv")
    if uploaded_file:
        st.success(f"✅ Archivo cargado: {uploaded_file.name}")
    
    st.divider()
    
    # Selección de período (solo para modo real)
    if st.session_state.mode == "real":
        st.subheader("Parámetros")
        periodo = st.selectbox(
            "Período",
            [f"2024-{i:02d}" for i in range(1, 13)],
            index=1
        )
        llm = st.selectbox("LLM", ["gemini", "openai", "none"], index=0)
    
    st.divider()
    st.caption("SabIA v0.1 | Hackathon 2026")

# Main area
col_left, col_right = st.columns([2, 1])

with col_right:
    st.subheader("🤝 Agentes")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Agente Q", use_container_width=True, key="agent_q"):
            st.session_state.current_story = 1
            st.session_state.chat_history = []
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Hola, soy Agente Q. Te ayudaré a identificar qué productos realmente te dejan dinero. 💰",
                "story": 1
            })
    
    with col2:
        if st.button("⚡ Agente 2", use_container_width=True, key="agent_2"):
            st.session_state.current_story = 2
            st.session_state.chat_history = []
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Hola, soy Agente 2. Te ayudaré a identificar qué productos te quitan mucho tiempo con poco retorno. ⏱️",
                "story": 2
            })

with col_left:
    st.subheader("💬 Conversación")
    
    # Mostrar historial de chat
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])
    
    # Input del usuario
    st.divider()
    user_input = st.chat_input("Escribe tu pregunta aquí...", key="chat_input")
    
    if user_input:
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        st.chat_message("user").write(user_input)
        
        # Procesar según el agente seleccionado
        if st.session_state.current_story:
            story_id = st.session_state.current_story
            
            try:
                # Obtener datos del endpoint demo
                response = requests.get(
                    f"{BASE_URL}/demo/story/{story_id}",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                # Respuesta del asistente basada en el story
                if story_id == 1:
                    respuesta = f"""
                    📊 **Ranking de productos por margen real**
                    
                    **TOP 3 productos rentables:**
                    """
                    for prod in data.get("ranking", [])[:3]:
                        respuesta += f"\n- **{prod['nombre_producto']}**: {prod['margen_pct']*100:.1f}% margen ({prod['contribucion_total']:,.0f} contribución total)"
                    
                    respuesta += f"\n\n⚠️ **Productos con riesgo:**"
                    for prod in data.get("bottom_risk", []):
                        respuesta += f"\n- **{prod['nombre_producto']}**: {prod['margen_pct']*100:.1f}% margen (PÉRDIDA: {prod['perdida_total']:,.0f})"
                
                elif story_id == 2:
                    respuesta = f"""
                    ⏱️ **Análisis: Tiempo vs Margen**
                    
                    **Productos eficientes (poco tiempo, buen margen):**
                    """
                    for item in data.get("items", []):
                        if item["categoria"] == "eficiente":
                            respuesta += f"\n- **{item['nombre_servicio']}**: {item['minutos_trabajo']} min, {item['margen_pct']*100:.1f}% margen ✅"
                    
                    respuesta += f"\n\n⚠️ **Alto esfuerzo, bajo retorno:**"
                    for item in data.get("items", []):
                        if item["categoria"] == "alto_esfuerzo_bajo_retorno":
                            respuesta += f"\n- **{item['nombre_servicio']}**: {item['minutos_trabajo']} min, {item['margen_pct']*100:.1f}% margen ❌"
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": respuesta,
                    "story": story_id,
                    "data": data
                })
                st.chat_message("assistant").write(respuesta)
                
            except requests.RequestException as e:
                error_msg = f"Error al consultar el backend: {str(e)}"
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.error(error_msg)
        else:
            msg = "Por favor, selecciona un Agente primero (Agente Q o Agente 2)"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": msg
            })
            st.chat_message("assistant").write(msg)

# Footer
st.divider()
st.markdown("""
    **📌 Historias disponibles:**
    - **Historia 1 (Agente Q)**: ¿Qué productos realmente me dejan dinero?
    - **Historia 2 (Agente 2)**: ¿Qué productos me quitan mucho tiempo con poco retorno?
    - *Historia 3 & 4 próximamente en el chat*
""")
