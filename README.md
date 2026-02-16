# 🚀 SabIA Agente — Hackathon 2026 (ADL NODO)

SabIA es un copiloto inteligente que transforma datos dispersos de una Pyme en **decisiones claras, explicables y accionables**.

## 🧠 ¿Qué hace?
- Integra datos operativos simples (CSV)
- Calcula costos reales y márgenes por producto
- Detecta problemas de rentabilidad y eficiencia
- Genera alertas explicables con evidencia y drivers de costo
- Produce un output listo para visualizar en Streamlit

No reemplaza decisiones: **las mejora con datos**.

---

## ⚙️ Stack Tecnológico
**Backend**
- Python 3.10+
- FastAPI (API REST)
- Pandas (motor de cálculo)
- SQLite (persistencia por corrida `run_id`)
- APScheduler (automatización opcional)

**IA (opcional)**
- OpenAI GPT / Google Gemini (solo redacción de reportes, no cálculos)

**Frontend (externo)**
- Streamlit consume `GET /runs/latest`

---

## 🔄 Flujo del Sistema
CSV → Costos → KPIs → Alertas → (IA) → Output JSON → Streamlit

---

## 📂 Inputs esperados (`/data`)
- productos.csv  
- ventas.csv  
- insumos.csv  
- recetas.csv  
- tiempos_produccion.csv  
- gastos_generales.csv  

---

## 📤 Output estable
`GET /runs/latest` devuelve:

- `run_id`, `periodo`
- Reporte ejecutivo (MD)
- JSON KPIs
- Alertas explicables

---

## ▶️ Ejecutar demo
```bash
uvicorn app.main:app --reload --port 8000
Run pipeline:
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"periodo":"2026-02","llm":null}'

Ver resultados:

curl http://localhost:8000/runs/latest
```


🏁 Éxito Hackathon
✔ Identifica productos problemáticos
✔ Explica el origen del problema
✔ Recomienda acciones concretas
✔ Estima impacto económico

SabIA convierte:

Datos dispersos → Diagnóstico claro → Acción concreta


## 👩‍💻 Backend & Automatizaciones (Mi aporte)

Diseñé e implementé el backend y las automatizaciones del copiloto **SabIA**, incluyendo:

- Ingestión y validación de datasets operativos (CSV)
- Motor de cálculo de costos reales (insumos, indirectos y esfuerzo)
- Cálculo de KPIs clave de rentabilidad y eficiencia
- Motor de alertas explicables con evidencia numérica y drivers de costo
- Persistencia de resultados por corrida (`run_id`) y período
- API REST lista para consumo desde la interfaz en **Streamlit**

Además, dejé preparada la capa opcional de IA (**OpenAI / Gemini**) para generar reportes ejecutivos y recomendaciones en lenguaje natural, sin afectar el cálculo determinístico ni la trazabilidad del sistema.

---

## 📄 Copyright

© 2026 Gabriela Coronel. Todos los derechos reservados sobre el diseño técnico, arquitectura, automatizaciones y desarrollo del backend del copiloto SabIA descritos anteriormente.

Este proyecto fue desarrollado en el marco del Hackathon 2026 ADL - NODO.

Integrantes : 
Gabriela Coronel (backend-automatizaciones-integraciones)

pedro contreras (visualizacion)

occe Javiera Gonzalez (Data product) 

