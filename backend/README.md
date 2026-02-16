🚀 SabIA Agente
Hackathon 2026 — ADL NODO

Un copiloto inteligente que transforma datos dispersos de una Pyme en decisiones claras, explicables y accionables.

¿Qué es SabIA?

SabIA es un motor de análisis de rentabilidad para Pymes que:

Integra datos operativos simples (CSV)

Calcula costos reales por producto

Detecta problemas de margen y eficiencia

Genera alertas explicables

Entrega recomendaciones claras

Produce un output listo para visualización

No reemplaza decisiones.
Las mejora.

⚙️ Stack Tecnológico
Backend

Python 3.10+

FastAPI → API REST

Pandas → Motor de cálculo

SQLite → Persistencia ligera por corrida

APScheduler → Automatización (opcional MVP)

Arquitectura modular y escalable

IA (Opcional)

Adapter pattern listo para:

OpenAI (GPT)

Google Gemini

La IA solo redacta reportes.
Los números son determinísticos.

Frontend (externo)

Streamlit

Consume GET /runs/latest

No realiza cálculos

🔄 Flujo del Sistema
CSV → Ingesta → Cálculo de costos → KPIs → Alertas → (IA) → Output JSON → Streamlit


Más detallado:

📥 Carga CSV

🧮 Calcula costo total unitario

📊 Calcula margen e impacto económico

🚨 Aplica reglas explícitas

📝 (Opcional) Genera reporte ejecutivo

💾 Guarda corrida con run_id

📡 Streamlit consume resultados

📂 Inputs Esperados

Ubicados en /data:

productos.csv

ventas.csv

insumos.csv

recetas.csv

tiempos_produccion.csv

gastos_generales.csv

Diseñado para rubros productivos, pero arquitectura extensible a múltiples industrias.

📤 Output (Contrato Estable)

GET /runs/latest devuelve:

run_id

periodo

executive_report_md

kpis

alerts[] (con evidencia y drivers)

Esto permite:

Cambiar la UI sin tocar el backend

Escalar a múltiples clientes

Versionar análisis

Qué Calcula el Motor
Costo Total Unitario

Costo insumos

Costo esfuerzo (tiempo × valor_minuto)

Prorrateo gastos generales

KPIs

Margen absoluto y %

Contribución total

Pérdida por margen negativo

Eficiencia productiva

Top productos por impacto

Alertas

Margen negativo

Margen crítico

Precio desactualizado

Alto esfuerzo / bajo retorno

Insumo dominante

Todas explicables. Sin caja negra.

▶️ Cómo Ejecutarlo
uvicorn app.main:app --reload --port 8000


Ejecutar pipeline:

POST /run
{
  "periodo": "2026-02",
  "llm": null
}


Ver resultados:

GET /runs/latest

🎯 Problema que Resuelve

Las Pymes:

Tienen datos

No tienen interpretación

Deciden por intuición

No integran costos reales

SabIA convierte:

Datos dispersos → Diagnóstico claro → Acción concreta

🧱 Arquitectura Escalable
Raw Data
   ↓
Industry Adapter
   ↓
KPIs + Alertas + IA
   ↓
API
   ↓
Cualquier UI


Streamlit hoy.
Web app mañana.
SaaS multi-Pyme después.

🏁 Criterio de Éxito (Hackathon)

✔ Detecta al menos 1 producto problemático
✔ Explica claramente el origen del problema
✔ Entrega una recomendación accionable
✔ Genera impacto económico estimado

🔮 Próximos Pasos (Post Hackathon)

Multi-tenant real (pyme_id)

Conectores automáticos (POS / Sheets / ERP)

Histórico comparativo mensual

Notificaciones automáticas

Dashboard SaaS

🧩 Filosofía del Proyecto

No más “creo que gano plata”.

SabIA responde:

“Este producto pierde $12.000 este mes por X motivo.
Si ajustás el precio a $1.715, el impacto estimado es +$42.900.”

Decisiones con evidencia.